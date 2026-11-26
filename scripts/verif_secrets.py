#!/usr/bin/env python3
"""Contrôle des secrets d'un dépôt client DIGICAP'S (stack B).
Usage : python3 scripts/verif_secrets.py [dossier] [--historique]   (code de sortie 1 si un secret est trouvé)
Cherche dans les fichiers suivis par git : clé Supabase service_role (JWT décodé), jetons Airtable,
Resend, Stripe, OpenAI, Anthropic, clés privées, mots de passe en clair, et tout fichier .env versionné.
"""
import base64, json, re, subprocess, sys, os

args = [a for a in sys.argv[1:] if not a.startswith("--")]
racine = args[0] if args else "."
HISTORIQUE = "--historique" in sys.argv
fichiers = subprocess.run(["git", "-C", racine, "ls-files"], capture_output=True, text=True).stdout.split()

MOTIFS = {
    "Jeton Airtable": r"\bpat[A-Za-z0-9]{14}\.[a-f0-9]{64}\b",
    "Clé Resend": r"\bre_[A-Za-z0-9_]{20,}\b",
    "Clé Stripe": r"\b(sk|rk)_(live|test)_[A-Za-z0-9]{16,}\b",
    "Clé OpenAI": r"\bsk-(proj-)?[A-Za-z0-9_-]{32,}\b",
    "Clé Anthropic": r"\bsk-ant-[A-Za-z0-9_-]{20,}\b",
    "Clé privée": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Mot de passe en clair": r"(?i)\b(password|passwd|mot_de_passe|mdp)\s*[:=]\s*[\"'][^\"']{6,}[\"']",
    "Chaîne de connexion Postgres": r"postgres(ql)?://[^:\s]+:[^@\s]+@",
}
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.(eyJ[A-Za-z0-9_-]{10,})\.[A-Za-z0-9_-]{10,}\b")

def role_jwt(charge):
    try:
        d = json.loads(base64.urlsafe_b64decode(charge + "=" * (-len(charge) % 4)))
        return d.get("role")
    except Exception:
        return None

alertes = []
for f in fichiers:
    nom = os.path.basename(f)
    if nom.startswith(".env") and nom not in (".env.example", ".env.exemple"):
        alertes.append((f, 0, "Fichier .env versionné"))
    chemin = os.path.join(racine, f)
    try:
        texte = open(chemin, encoding="utf-8", errors="ignore").read()
    except (IsADirectoryError, FileNotFoundError):
        continue
    for n, ligne in enumerate(texte.splitlines(), 1):
        for m in JWT.finditer(ligne):
            if role_jwt(m.group(1)) == "service_role":
                alertes.append((f, n, "Clé Supabase service_role"))
        for libelle, motif in MOTIFS.items():
            if re.search(motif, ligne):
                alertes.append((f, n, libelle))

if HISTORIQUE:
    journal = subprocess.run(["git", "-C", racine, "log", "-p", "--all", "--no-color"], capture_output=True, text=True, errors="ignore").stdout
    commit = "?"
    for ligne in journal.splitlines():
        if ligne.startswith("commit "):
            commit = ligne.split()[1][:8]
        if not ligne.startswith("+") or ligne.startswith("+++"):
            continue
        for m in JWT.finditer(ligne):
            if role_jwt(m.group(1)) == "service_role":
                alertes.append((f"historique {commit}", 0, "Clé Supabase service_role"))
        for libelle, motif in MOTIFS.items():
            if re.search(motif, ligne):
                alertes.append((f"historique {commit}", 0, libelle))

for f, n, libelle in alertes:
    print(f"SECRET  {f}:{n}  {libelle}")
print(f"{len(alertes)} alerte(s) sur {len(fichiers)} fichier(s) suivis.")
sys.exit(1 if alertes else 0)

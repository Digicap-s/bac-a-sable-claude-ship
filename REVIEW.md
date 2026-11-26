# Règles de relecture du bac à sable

Signaler en Important tout écart ci-dessous.

## Données et accès
- Chaque table créée par une migration a la RLS activée et au moins une politique. Une table sans RLS est un défaut Important.
- La clé service_role n'apparaît jamais dans `src/` ni dans un fichier versionné.
- Une colonne sensible (coût, marge, jeton) ne sort jamais vers le front.

## Calculs
- TTC = HT x (1 + taux de TVA), arrondi au centime à la fin du calcul, pas à chaque étape.
- Acompte : 30 % par défaut, calculé sur le TTC.
- Restant dû = marché TTC moins le déjà réglé, jamais négatif.

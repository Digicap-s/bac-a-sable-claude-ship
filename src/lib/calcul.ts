// Calculs fictifs du bac à sable. Arrondi au centime à la fin seulement.
const arrondi = (x: number) => Math.round(x * 100) / 100;

export function ttc(ht: number, tauxTva: number): number {
  return arrondi(ht * (1 + tauxTva));
}

export function acompte(ht: number, tauxTva: number, taux = 0.3): number {
  return arrondi(ht * (1 + tauxTva) * taux);
}

export function restantDu(ht: number, tauxTva: number, dejaRegle: number): number {
  return Math.max(0, arrondi(ht * (1 + tauxTva) - dejaRegle));
}

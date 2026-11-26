// Calculs fictifs du bac à sable.
const arrondi = (x: number) => Math.round(x * 100) / 100;

export function ttc(ht: number, tauxTva: number): number {
  return arrondi(arrondi(ht) * arrondi(1 + tauxTva));
}

export function acompte(ht: number, tauxTva: number, taux = 0.3): number {
  return arrondi(ht * taux);
}

export function restantDu(ht: number, tauxTva: number, dejaRegle: number): number {
  return arrondi(ttc(ht, tauxTva) - dejaRegle);
}

const MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
const MOIS_COURTS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];
const JOURS_COURTS = ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."];

/** Les dates ISO « AAAA-MM-JJ » sont des jours civils d'Abidjan (UTC+0) : aucun décalage de fuseau. */
function parties(iso: string) {
  const [a, m, j] = iso.split("-").map(Number);
  const jourSemaine = new Date(Date.UTC(a, m - 1, j)).getUTCDay();
  return { a, m, j, jourSemaine };
}

export function dateLongue(iso: string): string {
  const { a, m, j } = parties(iso);
  return `${j === 1 ? "1er" : j} ${MOIS[m - 1]} ${a}`;
}

export function dateCourte(iso: string): string {
  const { m, j, a } = parties(iso);
  return `${j} ${MOIS_COURTS[m - 1]} ${a}`;
}

export function blocDate(iso: string) {
  const { m, j, jourSemaine } = parties(iso);
  return { jour: JOURS_COURTS[jourSemaine].toUpperCase(), numero: String(j), mois: MOIS_COURTS[m - 1].toUpperCase() };
}

export function periode(debut: string, fin: string | null): string {
  if (!fin || fin === debut) return dateLongue(debut);
  const d = parties(debut), f = parties(fin);
  if (d.a === f.a && d.m === f.m) return `du ${d.j} au ${f.j} ${MOIS[f.m - 1]} ${f.a}`;
  return `du ${dateLongue(debut)} au ${dateLongue(fin)}`;
}

/** Aujourd'hui à Abidjan (UTC+0), au format ISO. */
export function aujourdhui(maintenant: Date = new Date()): string {
  return maintenant.toISOString().slice(0, 10);
}

export function lienWhatsApp(numero: string, texte?: string): string {
  const n = numero.replace(/[^\d]/g, "");
  return `https://wa.me/${n}${texte ? `?text=${encodeURIComponent(texte)}` : ""}`;
}

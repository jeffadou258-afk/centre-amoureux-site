import { getEvenementsAVenir, getSite } from "@/lib/donnees";

/** Fichier calendrier (.ics) d'un événement : ajout à l'agenda du téléphone. */
export async function GET(_req: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const [evenements, site] = await Promise.all([getEvenementsAVenir("0000-00-00"), getSite()]);
  const e = evenements.find((x) => x.slug === slug);
  if (!e) return new Response("Événement introuvable", { status: 404 });
  const jour = (iso: string) => iso.replace(/-/g, "");
  const lendemain = (iso: string) => {
    const d = new Date(`${iso}T00:00:00Z`);
    d.setUTCDate(d.getUTCDate() + 1);
    return d.toISOString().slice(0, 10).replace(/-/g, "");
  };
  const echapper = (t: string) => t.replace(/[\\,;]/g, (c) => `\\${c}`).replace(/\n/g, "\\n");
  const ics = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Centre des Amoureux de Dieu//Site//FR", "BEGIN:VEVENT",
    `UID:${e.slug}@centre-des-amoureux`,
    `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").slice(0, 15)}Z`,
    `DTSTART;VALUE=DATE:${jour(e.debut)}`,
    `DTEND;VALUE=DATE:${lendemain(e.fin ?? e.debut)}`,
    `SUMMARY:${echapper(e.titre)}`,
    `LOCATION:${echapper(`${e.lieu} — ${site.adresse}`)}`,
    `DESCRIPTION:${echapper([e.heure, e.details, e.a_confirmer].filter(Boolean).join(" · "))}`,
    "END:VEVENT", "END:VCALENDAR",
  ].join("\r\n");
  return new Response(ics, {
    headers: { "Content-Type": "text/calendar; charset=utf-8", "Content-Disposition": `attachment; filename="${e.slug}.ics"` },
  });
}

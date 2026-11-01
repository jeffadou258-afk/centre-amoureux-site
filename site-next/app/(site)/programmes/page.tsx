import type { Metadata } from "next";
import Image from "next/image";
import { AConfirmer, Conteneur, Surtitre } from "@/components/ui";
import { getEvenementsAVenir, getSite } from "@/lib/donnees";
import { ANNONCES } from "@/lib/contenu";
import { blocDate, lienWhatsApp, periode } from "@/lib/format";

export const metadata: Metadata = {
  title: "Programmes et événements",
  description: "Cultes, jeûnes, veillées et événements du Centre des Amoureux de Dieu à Cocody Riviera 2.",
};

export default async function PageProgrammes() {
  const [site, evenements] = await Promise.all([getSite(), getEvenementsAVenir()]);
  const vedette = evenements.find((e) => e.mise_en_avant) ?? evenements[0];

  return (
    <>
      <section className="relative overflow-hidden bg-nuit text-sur-nuit">
        <div className="braises opacity-70" aria-hidden="true" />
        <Conteneur className="entree relative flex flex-col gap-3.5 pb-12 pt-10">
          <Surtitre surNuit>Programmes</Surtitre>
          <h1 className="m-0 font-titre text-[clamp(1.85rem,4.4vw,3rem)] font-bold leading-[1.05]">Nos rendez-vous</h1>
        </Conteneur>
      </section>

      <Conteneur className="flex flex-col gap-16 pb-24 pt-12">
        <section aria-labelledby="semaine" className="flex flex-col gap-5">
          <h2 id="semaine" className="m-0 font-titre text-2xl font-bold">Chaque semaine</h2>
          <div className="grid gap-5 md:grid-cols-3">
            {site.horaires.map((h) => (
              <div key={h.jour} className="flex flex-col gap-1.5 rounded-[20px] border border-ligne bg-white p-6">
                <span className="text-[13px] font-semibold text-flamme-encre">{h.jour}</span>
                <span className="font-titre text-lg font-bold">{h.heures}</span>
                <span className="font-bold">{h.libelle}</span>
                {h.precision && <span className="text-sm text-gris">{h.precision}</span>}
              </div>
            ))}
            <div className="flex flex-col gap-1.5 rounded-[20px] border-2 border-dashed border-pointille bg-white p-6">
              <span className="text-[13px] font-semibold text-flamme-encre">Vendredi</span>
              <span className="font-titre text-lg font-bold"><AConfirmer>Horaire à confirmer</AConfirmer></span>
              <span className="font-bold">Nuit de prière</span>
            </div>
          </div>
          {ANNONCES.map((a) => <p key={a} className="m-0 text-[15px] text-texte-2">{a}</p>)}
        </section>

        <section aria-labelledby="agenda" className="grid items-start gap-12 lg:grid-cols-2">
          <div className="flex min-w-0 flex-col gap-5">
            <div className="flex flex-wrap items-baseline justify-between gap-4">
              <h2 id="agenda" className="m-0 font-titre text-2xl font-bold">Agenda</h2>
              {site.theme_du_mois && <span className="text-sm text-gris">Thème de {site.theme_du_mois.mois.toLowerCase()} : {site.theme_du_mois.titre}</span>}
            </div>
            {evenements.length === 0 ? (
              <p className="m-0 rounded-2xl bg-sable p-5">Les prochains rendez-vous seront publiés ici par le secrétariat.</p>
            ) : (
              <ol className="m-0 flex list-none flex-col gap-2 p-0">
                {evenements.map((e) => {
                  const d = blocDate(e.debut);
                  const fin = e.fin ? blocDate(e.fin) : null;
                  const vedetteCourante = e.slug === vedette?.slug;
                  return (
                    <li key={e.slug} id={e.slug} className={`grid grid-cols-[76px_1fr] items-center gap-4 rounded-2xl px-4 py-3.5 ${
                      vedetteCourante ? "border-2 border-flamme bg-white" : e.a_confirmer ? "border-2 border-dashed border-pointille bg-white" : "border border-ligne bg-white"
                    }`}>
                      <span className="flex flex-col items-center leading-none" aria-hidden="true">
                        <span className="text-xs font-bold text-flamme-encre">{d.jour}</span>
                        <span className="font-titre text-[32px] font-bold">{d.numero}</span>
                        <span className="text-xs font-bold">{fin ? `→ ${fin.numero}` : d.mois}</span>
                      </span>
                      <span className="flex flex-col gap-0.5">
                        <span className="sr-only">{periode(e.debut, e.fin)}</span>
                        <span className="text-[15px] font-bold">{e.titre}</span>
                        <span className="text-sm text-gris">
                          {[e.heure, e.details, e.lieu].filter(Boolean).join(" · ")}
                        </span>
                        {e.a_confirmer && <span className="text-sm"><AConfirmer>{e.a_confirmer}</AConfirmer></span>}
                      </span>
                    </li>
                  );
                })}
              </ol>
            )}
            {site.theme_du_mois?.suivant && (
              <p className="m-0 rounded-2xl bg-sable p-5 text-[15px] text-texte-2">
                {site.theme_du_mois.suivant.mois} · <em className="font-verset text-lg text-encre">{site.theme_du_mois.suivant.titre}</em> : les rendez-vous apparaîtront ici dès leur publication.
              </p>
            )}
          </div>

          {vedette && (
            <aside aria-label="Événement à la une" className="flex flex-col overflow-hidden rounded-3xl border border-ligne bg-white">
              {vedette.affiche && <Image src={vedette.affiche} alt={`Affiche : ${vedette.titre}`} width={872} height={1080} sizes="(min-width: 1024px) 560px, 100vw" className="block h-auto w-full" />}
              <div className="flex flex-col gap-3 p-6">
                <span className="text-[13px] font-bold text-flamme-encre">{periode(vedette.debut, vedette.fin)}{vedette.heure ? ` · ${vedette.heure}` : ""}</span>
                <span className="font-titre text-lg font-bold leading-tight">{vedette.titre}</span>
                {vedette.details && <span className="text-[15px] leading-normal text-texte-2">{vedette.details}</span>}
                <span className="text-[15px] leading-normal text-texte-2">{site.repere}</span>
                <div className="mt-1 flex flex-wrap gap-2.5">
                  <a href={`/programmes/${vedette.slug}/agenda.ics`} className="inline-flex min-h-12 items-center rounded-full bg-flamme px-5 font-bold text-sur-flamme no-underline hover:text-sur-flamme">Ajouter à mon agenda</a>
                  <a href={lienWhatsApp("", `${vedette.titre} — ${periode(vedette.debut, vedette.fin)}${vedette.heure ? ` ${vedette.heure}` : ""}, ${site.adresse}`)} target="_blank" rel="noopener" className="inline-flex min-h-12 items-center rounded-full border-[1.5px] border-[#D4C6B6] px-5 font-bold text-encre no-underline hover:text-encre">Partager sur WhatsApp</a>
                </div>
                <span className="text-sm text-gris">Infos : {site.telephone}{site.telephone2 ? ` · ${site.telephone2}` : ""}</span>
              </div>
            </aside>
          )}
        </section>
      </Conteneur>
    </>
  );
}

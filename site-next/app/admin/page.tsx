import Link from "next/link";
import { getEvenementsAVenir, getPredications } from "@/lib/donnees";
import { blocDate } from "@/lib/format";

export default async function TableauDeBord() {
  const [predications, evenements] = await Promise.all([getPredications(), getEvenementsAVenir()]);
  const datees = evenements.filter((e) => !e.a_confirmer?.includes("date"));
  const tuiles = [
    { titre: "Prédications publiées", valeur: String(predications.length), aide: predications[0] ? `dernière : ${blocDate(predications[0].date).numero} ${blocDate(predications[0].date).mois.toLowerCase()}` : "" },
    { titre: "Événements à venir", valeur: String(datees.length), aide: evenements.length > datees.length ? `+ ${evenements.length - datees.length} date à fixer` : "" },
    { titre: "Prières non lues", valeur: "—", aide: "après branchement de l’API" },
    { titre: "Témoignages à valider", valeur: "—", aide: "après branchement de l’API" },
    { titre: "Dons du mois", valeur: "—", aide: "paiements non activés" },
  ];
  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="m-0 font-titre text-4xl font-black uppercase">Tableau de bord</h1>
        <Link href="/admin/predications/tous-les-grands-ont-reve-grand" className="inline-flex min-h-11 items-center rounded-full bg-flamme px-5 font-extrabold text-sur-flamme no-underline hover:text-sur-flamme">Modifier une prédication</Link>
      </div>
      <div className="grid gap-4 [grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr))]">
        {tuiles.map((t) => (
          <div key={t.titre} className="flex flex-col gap-1.5 rounded-2xl bg-white p-5">
            <span className="text-sm font-bold text-gris">{t.titre}</span>
            <span className={`font-titre text-[40px] font-black ${t.valeur === "—" ? "text-[#8F8275]" : ""}`}>{t.valeur}</span>
            <span className="text-[13px] text-gris">{t.aide}</span>
          </div>
        ))}
      </div>
      <section aria-labelledby="prochains" className="flex flex-col rounded-2xl bg-white p-6">
        <h2 id="prochains" className="m-0 mb-3 text-lg font-extrabold">Prochains rendez-vous</h2>
        {evenements.map((e) => (
          <div key={e.slug} className="grid grid-cols-[110px_1fr_auto] items-center gap-3 border-t border-[#EFE7DC] py-3">
            <span className="font-bold text-flamme-encre">{blocDate(e.debut).numero} {blocDate(e.debut).mois.toLowerCase()}{e.fin ? ` → ${blocDate(e.fin).numero}` : ""}</span>
            <span>{e.titre}</span>
            {e.a_confirmer ? (
              <span className="rounded-full bg-[#FFF1DA] px-2.5 py-1 text-xs font-bold text-[#7A4A06]">{e.a_confirmer.includes("date") ? "Date à fixer" : "Horaire manquant"}</span>
            ) : (
              <span className="rounded-full bg-[#EFEAE3] px-2.5 py-1 text-xs font-bold text-texte-2">Complet</span>
            )}
          </div>
        ))}
      </section>
    </>
  );
}

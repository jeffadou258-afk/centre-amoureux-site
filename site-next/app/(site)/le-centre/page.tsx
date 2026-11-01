import type { Metadata } from "next";
import { BandeauPage } from "@/components/bandeau-page";
import { AConfirmer, Conteneur, Surtitre, TitreSection } from "@/components/ui";
import { DEPARTEMENTS, MISSION, VALEURS, VISION } from "@/lib/contenu";
import { getSite } from "@/lib/donnees";

export const metadata: Metadata = { title: "Le Centre", description: "Vision, mission, valeurs et départements du Centre des Amoureux de Dieu." };

export default async function PageCentre() {
  const site = await getSite();
  return (
    <>
      <BandeauPage surtitre="Qui nous sommes" titre="Une église, une famille, une armée d’amoureux" texte={`Le Centre des Amoureux de Dieu est une communauté chrétienne établie à Abidjan depuis ${site.fondation}.`} />
      <Conteneur className="flex flex-col gap-20 pb-24 pt-14">
        <section className="grid gap-10 lg:grid-cols-2">
          <div className="flex flex-col gap-4">
            <Surtitre>Notre vision</Surtitre>
            <TitreSection>Former, bâtir, équiper</TitreSection>
            <p className="m-0 text-xl font-medium leading-relaxed">« {VISION} »</p>
          </div>
          <div className="flex flex-col gap-4">
            <Surtitre>Notre mission</Surtitre>
            <p className="m-0 text-lg leading-relaxed text-texte-2">« {MISSION} »</p>
            <blockquote className="m-0 mt-4 font-verset text-[26px] italic leading-snug">
              « Le plus petit deviendra un millier, et le moindre une nation puissante. »
              <footer className="mt-2 font-texte text-[13px] font-bold not-italic tracking-[0.1em] text-flamme-encre">ÉSAÏE 60 : 22</footer>
            </blockquote>
          </div>
        </section>

        <section aria-labelledby="valeurs" className="flex flex-col gap-6">
          <TitreSection className="text-3xl">Nos valeurs</TitreSection>
          <ol className="m-0 grid list-none gap-0 border-t border-ligne p-0 sm:grid-cols-2 lg:grid-cols-3">
            {VALEURS.map((v, i) => (
              <li key={v.nom} className="flex flex-col gap-1.5 border-b border-ligne py-6 pr-6">
                <span className="font-titre text-sm font-extrabold text-flamme-encre">{String(i + 1).padStart(2, "0")}</span>
                <span className="font-titre text-[22px] font-extrabold">{v.nom}</span>
                <span className="text-[15px] leading-normal text-texte-2">{v.definition}</span>
                <span className="text-[13px] font-bold text-flamme-encre">{v.reference}</span>
              </li>
            ))}
          </ol>
        </section>

        <section aria-labelledby="departements" className="flex flex-col gap-6">
          <h2 id="departements" className="m-0 font-titre text-3xl font-black uppercase">Les départements</h2>
          <ul className="m-0 grid list-none gap-4 p-0 sm:grid-cols-2 lg:grid-cols-3">
            {DEPARTEMENTS.map((d) => (
              <li key={d.nom} className="flex flex-col gap-2 rounded-2xl border border-ligne bg-white p-5">
                <span className="text-[17px] font-extrabold">{d.nom}</span>
                <span className="text-sm leading-normal text-texte-2">{d.role}</span>
                <span className="text-sm">Responsable : {d.responsable ?? <AConfirmer />}</span>
              </li>
            ))}
          </ul>
        </section>
      </Conteneur>
    </>
  );
}

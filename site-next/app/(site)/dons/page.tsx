import type { Metadata } from "next";
import { Conteneur, Surtitre } from "@/components/ui";
import { FormulaireDon } from "@/components/formulaires";
import { getSite } from "@/lib/donnees";
import { lienWhatsApp } from "@/lib/format";

export const metadata: Metadata = { title: "Faire un don", description: "Soutenir l’œuvre du Centre des Amoureux de Dieu." };

export default async function PageDons() {
  const site = await getSite();
  return (
    <>
      <section className="relative overflow-hidden bg-nuit text-sur-nuit">
        <div className="braises opacity-70" aria-hidden="true" />
        <Conteneur className="entree relative flex flex-col gap-3 pb-12 pt-10">
          <Surtitre surNuit>Faire un don</Surtitre>
          <h1 className="m-0 font-titre text-[clamp(1.85rem,4.4vw,3rem)] font-bold leading-[1.05]">Soutenir l’œuvre</h1>
          <p className="m-0 font-verset text-lg italic leading-snug">« Dieu aime celui qui donne avec joie. »</p>
          <span className="text-xs font-bold tracking-[0.1em] text-or">2 CORINTHIENS 9 : 7</span>
        </Conteneur>
      </section>
      <Conteneur className="grid gap-12 pb-24 pt-10 lg:grid-cols-[minmax(0,560px)_1fr]">
        <FormulaireDon whatsapp={lienWhatsApp(site.whatsapp, "Bonjour, j’ai une question sur les dons.")} />
        <aside className="flex flex-col gap-4">
          <div className="flex flex-col gap-2 rounded-2xl bg-sable p-6">
            <h2 className="m-0 text-lg font-bold">Sur place</h2>
            <p className="m-0 leading-normal text-texte-2">Une urne est disponible lors de chaque culte, {site.horaires.map((h) => `le ${h.jour.toLowerCase()} (${h.heures})`).join(" et ")}.</p>
          </div>
          <div className="flex flex-col gap-2 rounded-2xl border border-ligne bg-white p-6">
            <h2 className="m-0 text-lg font-bold">À quoi servent vos dons</h2>
            <ul className="m-0 flex flex-col gap-1.5 pl-5 leading-normal text-texte-2">
              <li>Le fonctionnement des cultes et des activités de l’église.</li>
              <li>L’accompagnement des personnes en difficulté.</li>
              <li>Les actions sociales et les projets du Centre.</li>
            </ul>
          </div>
        </aside>
      </Conteneur>
    </>
  );
}

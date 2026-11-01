import type { Metadata } from "next";
import { BandeauPage } from "@/components/bandeau-page";
import { Conteneur } from "@/components/ui";
import { FormulairePriere } from "@/components/formulaires";
import { getEvenementsAVenir, getSite } from "@/lib/donnees";
import { lienWhatsApp } from "@/lib/format";

export const metadata: Metadata = { title: "Demander la prière", description: "Confiez une demande de prière à l’équipe du Centre des Amoureux de Dieu. Elle n’est jamais publiée." };

export default async function PagePriere() {
  const [site, evenements] = await Promise.all([getSite(), getEvenementsAVenir()]);
  const jeune = evenements.find((e) => e.fin && e.details?.includes("Prière en ligne"));
  return (
    <>
      <BandeauPage surtitre="Prière" titre="Demander la prière" texte="L’équipe de prière lit chaque demande. Elle reste confidentielle et n’est jamais publiée." />
      <Conteneur className="grid gap-12 pb-24 pt-10 lg:grid-cols-[minmax(0,640px)_1fr]">
        <FormulairePriere whatsapp={lienWhatsApp(site.whatsapp, "Bonjour, je souhaite confier une demande de prière.")} />
        <aside className="flex flex-col gap-4">
          <blockquote className="m-0 font-verset text-lg italic leading-snug">
            « Car là où deux ou trois sont assemblés en mon nom, je suis au milieu d’eux. »
            <footer className="mt-2 font-texte text-[13px] font-bold not-italic tracking-[0.1em] text-flamme-encre">MATTHIEU 18 : 20</footer>
          </blockquote>
          {jeune && (
            <p className="m-0 rounded-2xl bg-sable p-5 text-[15px] leading-normal">
              <strong>{jeune.titre}</strong> : {jeune.details}
            </p>
          )}
        </aside>
      </Conteneur>
    </>
  );
}

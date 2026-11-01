import type { Metadata } from "next";
import Image from "next/image";
import { BandeauPage } from "@/components/bandeau-page";
import { Conteneur, Surtitre, TitreSection } from "@/components/ui";
import { Valeurs } from "@/components/valeurs";
import { MISSION, VALEURS, VISION } from "@/lib/contenu";
import { getSite } from "@/lib/donnees";

export const metadata: Metadata = { title: "Le Centre", description: "Vision, mission et valeurs du Centre des Amoureux de Dieu." };

export default async function PageCentre() {
  const site = await getSite();
  return (
    <>
      <BandeauPage surtitre="Qui nous sommes" titre="Une église, une famille, une armée d’amoureux" texte={`Le Centre des Amoureux de Dieu est une communauté chrétienne établie à Abidjan depuis ${site.fondation}.`} />
      <Conteneur className="flex flex-col gap-24 pb-24 pt-16">
        <section className="grid items-center gap-12 lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)]">
          <div className="flex flex-col gap-10">
            <div data-apparition className="flex flex-col gap-4">
              <Surtitre>Notre vision</Surtitre>
              <TitreSection>Former, bâtir, équiper</TitreSection>
              <p className="m-0 text-[clamp(1.05rem,1.6vw,1.2rem)] font-medium leading-relaxed">{VISION}</p>
            </div>
            <div data-apparition style={{ ["--d" as string]: "120ms" }} className="flex flex-col gap-4">
              <Surtitre>Notre mission</Surtitre>
              <p className="m-0 text-base leading-[1.75] text-texte-2">{MISSION}</p>
            </div>
          </div>
          <figure data-apparition style={{ ["--d" as string]: "200ms" }} className="relative m-0 flex flex-col justify-end overflow-hidden rounded-3xl bg-nuit p-8 text-sur-nuit sm:min-h-[340px]">
            <div className="braises" aria-hidden="true" />
            <Image src="/img/cad-embleme.png" alt="" width={400} height={400} className="absolute -right-10 -top-10 w-56 opacity-10" />
            <blockquote className="relative m-0 font-verset text-[clamp(1.35rem,2.3vw,1.7rem)] italic leading-snug">
              « Le plus petit deviendra un millier, et le moindre une nation puissante. »
            </blockquote>
            <figcaption className="relative mt-3 text-[13px] font-semibold text-or">Ésaïe 60 : 22</figcaption>
          </figure>
        </section>

        <section aria-labelledby="valeurs" className="flex flex-col gap-8">
          <div data-apparition className="flex flex-col gap-3">
            <Surtitre>Ce qui nous tient</Surtitre>
            <TitreSection><span id="valeurs">Nos six valeurs</span></TitreSection>
          </div>
          <div data-apparition className="md:pl-5"><Valeurs valeurs={VALEURS} /></div>
        </section>
      </Conteneur>
    </>
  );
}

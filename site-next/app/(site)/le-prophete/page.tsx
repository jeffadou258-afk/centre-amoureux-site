import type { Metadata } from "next";
import Image from "next/image";
import { AConfirmer, Bouton, Conteneur, Surtitre } from "@/components/ui";
import { CartePredication } from "@/components/predications";
import { getPredications, getSite } from "@/lib/donnees";
import { PROPHETE } from "@/lib/contenu";

export const metadata: Metadata = { title: "Le Prophète Daniel Jeff Adou", description: "Le Prophète Daniel Jeff Adou, prophète et pasteur du Centre des Amoureux de Dieu." };

export default async function PageProphete() {
  const [predications, site] = await Promise.all([getPredications(), getSite()]);
  return (
    <>
      <section className="bg-nuit text-sur-nuit">
        <Conteneur className="grid items-center gap-12 pb-16 pt-10 md:grid-cols-2">
          <div className="flex flex-col gap-5">
            <Surtitre surNuit>Le Prophète</Surtitre>
            <h1 className="m-0 font-titre text-[clamp(2.75rem,5.5vw,4.75rem)] font-black uppercase leading-[0.95] tracking-[-0.02em]">{PROPHETE.nomCourt}</h1>
            <p className="m-0 text-lg text-creme">{PROPHETE.role}</p>
            <Bouton href={site.youtube} externe variante="contour-nuit" grand>Voir sa chaîne YouTube</Bouton>
          </div>
          <Image src="/img/prophete-portrait.jpg" alt={`Portrait du ${PROPHETE.nom}`} width={852} height={1150} priority sizes="(min-width: 768px) 460px, 100vw" className="aspect-[4/5] w-full max-w-[460px] justify-self-center rounded-3xl object-cover" />
        </Conteneur>
      </section>
      <Conteneur className="flex flex-col gap-16 pb-24 pt-14">
        <section className="grid gap-10 lg:grid-cols-2">
          <div className="flex flex-col gap-4 text-[17px] leading-[1.7] text-texte-2">
            <p className="m-0">Le Centre des Amoureux de Dieu est conduit par le {PROPHETE.nom}. Son enseignement est diffusé chaque semaine sur la chaîne du ministère, et porte une conviction simple : la Parole de Dieu éclaire la vie réelle, ici et maintenant.</p>
            <p className="m-0">Sa prédication insiste sur l’amour de Dieu, la vie de prière et la transformation du cœur, trois axes que l’on retrouve dans les messages publiés.</p>
            <p className="m-0 text-[15px]">Biographie officielle et parcours ministériel : <AConfirmer>texte à fournir par le Centre</AConfirmer></p>
          </div>
          <ol className="m-0 flex list-none flex-col border-t border-ligne p-0">
            {[
              ["L’amour de Dieu", "Comprendre qu’on est aimé avant d’être méritant."],
              ["La vie de prière", "Prier simplement, avec constance, en toute saison."],
              ["La transformation", "Passer de l’émotion du moment à un changement durable."],
            ].map(([titre, texte], i) => (
              <li key={titre} className="grid grid-cols-[48px_1fr] gap-3 border-b border-ligne py-5">
                <span className="font-titre text-sm font-extrabold text-flamme-encre">0{i + 1}</span>
                <span className="flex flex-col gap-1"><span className="font-titre text-xl font-extrabold">{titre}</span><span className="text-texte-2">{texte}</span></span>
              </li>
            ))}
          </ol>
        </section>
        <section className="flex flex-col gap-6">
          <h2 className="m-0 font-titre text-3xl font-black uppercase">Ses derniers messages</h2>
          <div className="grid gap-7 sm:grid-cols-2 lg:grid-cols-3">
            {predications.slice(0, 3).map((p) => <CartePredication key={p.slug} p={p} />)}
          </div>
        </section>
      </Conteneur>
    </>
  );
}

import type { Metadata } from "next";
import { BandeauPage } from "@/components/bandeau-page";
import { Conteneur } from "@/components/ui";
import { FormulaireTemoignage } from "@/components/formulaires";
import { getSite, getTemoignages } from "@/lib/donnees";
import { dateLongue, lienWhatsApp } from "@/lib/format";

export const metadata: Metadata = { title: "Témoignages", description: "Ce que Dieu a fait mérite d’être raconté : lisez et partagez un témoignage." };

export default async function PageTemoignages() {
  const [site, temoignages] = await Promise.all([getSite(), getTemoignages()]);
  return (
    <>
      <BandeauPage surtitre="Témoignages" titre="Ce que Dieu a fait" texte="Guérison, délivrance, provision, restauration familiale : chaque témoignage est lu puis validé par l’équipe avant publication." />
      <Conteneur className="grid gap-14 pb-24 pt-10 lg:grid-cols-2">
        <section aria-labelledby="publies" className="flex flex-col gap-5">
          <h2 id="publies" className="m-0 font-titre text-3xl font-black uppercase">Ils ont témoigné</h2>
          {temoignages.length === 0 ? (
            <p className="m-0 rounded-2xl bg-sable p-6 text-[15px] leading-normal">
              Aucun témoignage publié pour l’instant. Les témoignages validés apparaîtront ici, avec l’identité choisie par chacun.
            </p>
          ) : (
            temoignages.map((t) => (
              <article key={t.id} className="flex flex-col gap-2 rounded-2xl border border-ligne bg-white p-6">
                <h3 className="m-0 text-lg font-extrabold">{t.titre}</h3>
                <p className="m-0 whitespace-pre-line leading-relaxed text-texte-2">{t.texte}</p>
                <span className="text-sm text-gris">{t.prenom_affiche} · {dateLongue(t.date)}</span>
              </article>
            ))
          )}
          <blockquote className="m-0 font-verset text-2xl italic">
            « Retourne dans ta maison, et raconte tout ce que Dieu a fait pour toi. »
            <footer className="mt-2 font-texte text-[13px] font-bold not-italic tracking-[0.1em] text-flamme-encre">LUC 8 : 39</footer>
          </blockquote>
        </section>
        <section aria-labelledby="partager" className="flex flex-col gap-5">
          <h2 id="partager" className="m-0 font-titre text-3xl font-black uppercase">Partager le vôtre</h2>
          <FormulaireTemoignage whatsapp={lienWhatsApp(site.whatsapp, "Bonjour, je souhaite partager un témoignage.")} />
        </section>
      </Conteneur>
    </>
  );
}

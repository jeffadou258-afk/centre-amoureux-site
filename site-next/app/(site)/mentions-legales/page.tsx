import type { Metadata } from "next";
import { BandeauPage } from "@/components/bandeau-page";
import { AConfirmer, Conteneur } from "@/components/ui";
import { getSite } from "@/lib/donnees";

export const metadata: Metadata = { title: "Mentions légales", robots: { index: true } };

export default async function PageMentions() {
  const site = await getSite();
  return (
    <>
      <BandeauPage surtitre="Informations légales" titre="Mentions légales" />
      <Conteneur className="flex max-w-[760px] flex-col gap-6 pb-24 pt-10 leading-relaxed text-texte-2">
        <section><h2 className="text-xl font-extrabold text-encre">Éditeur du site</h2><p className="m-0">{site.nom} — {site.adresse}, {site.ville}. Téléphone : {site.telephone}.</p><p className="m-0">Responsable de la publication : Prophète Daniel Jeff Adou, pasteur du Centre.</p><p className="m-0">Identification légale (statut, numéro d’enregistrement) : <AConfirmer /></p></section>
        <section><h2 className="text-xl font-extrabold text-encre">Hébergement</h2><p className="m-0">Hébergeur : <AConfirmer>à renseigner après la mise en ligne</AConfirmer></p></section>
        <section><h2 className="text-xl font-extrabold text-encre">Propriété intellectuelle</h2><p className="m-0">Les textes, visuels et éléments graphiques de ce site sont la propriété du {site.nom}, sauf mention contraire. Les vidéos sont diffusées depuis la chaîne officielle du ministère.</p></section>
        <section><h2 className="text-xl font-extrabold text-encre">Litiges</h2><p className="m-0">Le présent site est soumis au droit ivoirien. En cas de difficulté, une solution amiable sera recherchée avant toute action contentieuse.</p></section>
      </Conteneur>
    </>
  );
}

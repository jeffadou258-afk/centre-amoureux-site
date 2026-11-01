import type { Metadata } from "next";
import { BandeauPage } from "@/components/bandeau-page";
import { AConfirmer, Conteneur } from "@/components/ui";
import { getSite } from "@/lib/donnees";

export const metadata: Metadata = { title: "Confidentialité" };

export default async function PageConfidentialite() {
  const site = await getSite();
  const h2 = "text-lg font-bold text-encre";
  return (
    <>
      <BandeauPage surtitre="Données personnelles" titre="Confidentialité" />
      <Conteneur className="flex max-w-[760px] flex-col gap-6 pb-24 pt-10 leading-relaxed text-texte-2">
        <section><h2 className={h2}>Responsable du traitement</h2><p className="m-0">{site.nom} — {site.adresse}, {site.ville}. Contact : {site.telephone} (téléphone et WhatsApp).</p></section>
        <section>
          <h2 className={h2}>Ce que ce site collecte</h2>
          <ul className="m-0 flex flex-col gap-2 pl-5">
            <li><strong>Demandes de prière</strong> : prénom et contact facultatifs, sujet, message, et le choix de qui peut les lire. Elles ne sont jamais publiées ni utilisées à des fins commerciales.</li>
            <li><strong>Témoignages</strong> : nom ou pseudonyme, texte, identité affichée. Aucun témoignage n’est publié sans votre accord explicite et sans validation de l’équipe.</li>
            <li><strong>Dons</strong> : montant, affectation, moyen de paiement et e-mail facultatif pour le reçu. Le paiement se fait sur la page du prestataire : ce site ne voit jamais votre code ni votre carte.</li>
          </ul>
          <p className="m-0 mt-2">Le site ne dépose aucun cookie de mesure d’audience. Les polices sont hébergées par le site lui-même. Les vidéos YouTube ne sont chargées qu’après votre clic.</p>
        </section>
        <section><h2 className={h2}>Durées de conservation</h2><p className="m-0">Les demandes de prière sont conservées le temps du suivi pastoral. Durées précises : <AConfirmer>à fixer avec le Centre</AConfirmer></p></section>
        <section><h2 className={h2}>Vos droits</h2><p className="m-0">Vous pouvez demander l’accès, la rectification ou la suppression des informations vous concernant en contactant le Centre au {site.telephone}.</p></section>
      </Conteneur>
    </>
  );
}

import type { Metadata } from "next";
import { BandeauPage } from "@/components/bandeau-page";
import { AConfirmer, Conteneur } from "@/components/ui";
import { getSite } from "@/lib/donnees";
import { lienWhatsApp } from "@/lib/format";

export const metadata: Metadata = { title: "Nous rejoindre", description: "Adresse, horaires des cultes et contacts du Centre des Amoureux de Dieu à Cocody Riviera 2, Abidjan." };

export default async function PageRejoindre() {
  const site = await getSite();
  const carte = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent("Imprimerie DA Communication, Riviera 2, Cocody, Abidjan")}`;
  return (
    <>
      <BandeauPage surtitre="Nous rejoindre" titre="Venir au Centre" texte="Vous êtes attendu, tel que vous êtes. Voici tout ce qu’il faut pour votre première visite." />
      <Conteneur className="grid gap-12 pb-24 pt-12 lg:grid-cols-2">
        <section aria-labelledby="adresse" className="flex flex-col gap-4">
          <h2 id="adresse" className="m-0 font-titre text-3xl font-black uppercase">Nous trouver</h2>
          <p className="m-0 text-xl font-bold leading-snug">{site.adresse}</p>
          <p className="m-0 text-[17px] leading-relaxed text-texte-2">{site.repere}</p>
          <a href={carte} target="_blank" rel="noopener" className="inline-flex min-h-[52px] items-center justify-center self-start rounded-full bg-encre px-7 font-bold text-ivoire no-underline hover:text-ivoire">Ouvrir l’itinéraire</a>
          <h2 className="m-0 mt-6 font-titre text-3xl font-black uppercase">Horaires</h2>
          <ul className="m-0 flex list-none flex-col border-t border-ligne p-0">
            {site.horaires.map((h) => (
              <li key={h.jour} className="flex flex-wrap justify-between gap-2 border-b border-ligne py-4">
                <span><strong>{h.jour}</strong> · {h.libelle}{h.precision ? ` (${h.precision})` : ""}</span>
                <span className="font-titre font-extrabold">{h.heures}</span>
              </li>
            ))}
          </ul>
        </section>
        <section aria-labelledby="contact" className="flex flex-col gap-4">
          <h2 id="contact" className="m-0 font-titre text-3xl font-black uppercase">Nous contacter</h2>
          <a href={`tel:${site.telephone.replace(/\s/g, "")}`} className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-flamme px-7 font-extrabold text-sur-flamme no-underline hover:text-sur-flamme">Appeler le {site.telephone}</a>
          <a href={lienWhatsApp(site.whatsapp, "Bonjour, je souhaite visiter le Centre.")} target="_blank" rel="noopener" className="inline-flex min-h-[52px] items-center justify-center rounded-full border-[1.5px] border-[#D4C6B6] bg-white px-7 font-bold text-encre no-underline hover:text-encre">Écrire sur WhatsApp</a>
          {site.telephone2 && <p className="m-0 text-[15px] text-texte-2">Autre numéro : {site.telephone2}</p>}
          <p className="m-0 text-[15px] text-texte-2">E-mail : {site.email ?? <AConfirmer>adresse officielle à fournir</AConfirmer>}</p>
          <blockquote className="m-0 mt-6 font-verset text-[26px] italic leading-snug">
            « Car là où deux ou trois sont assemblés en mon nom, je suis au milieu d’eux. »
            <footer className="mt-2 font-texte text-[13px] font-bold not-italic tracking-[0.1em] text-flamme-encre">MATTHIEU 18 : 20</footer>
          </blockquote>
        </section>
      </Conteneur>
    </>
  );
}

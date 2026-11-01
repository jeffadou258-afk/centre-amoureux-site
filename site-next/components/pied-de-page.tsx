import Link from "next/link";
import Image from "next/image";
import type { Site } from "@/lib/api/contrats";
import { AConfirmer } from "@/components/ui";

export function PiedDePage({ site }: { site: Site }) {
  const reseaux = [
    { nom: "Facebook", url: site.facebook },
    { nom: "Instagram", url: site.instagram },
    { nom: "TikTok", url: site.tiktok },
  ];
  return (
    <footer className="bg-[#0B0705] text-creme">
      <div className="mx-auto grid max-w-[1200px] gap-8 px-5 pb-8 pt-14 text-sm leading-relaxed sm:grid-cols-2 sm:px-8 lg:grid-cols-4">
        <div className="flex flex-col gap-3">
          <Image src="/img/cad-logo-blanc.png" alt="Centre des Amoureux de Dieu" width={800} height={350} className="h-12 w-auto self-start" />
          <p className="m-0">Une maison de prière, de Parole et d’amour fraternel, ouverte à tous.</p>
        </div>
        <div className="flex flex-col gap-1">
          <h2 className="m-0 mb-1 text-xs font-bold uppercase tracking-[0.1em] text-sur-nuit">Nous trouver</h2>
          <p className="m-0">{site.adresse}, {site.ville}</p>
          <a href={`tel:${site.telephone.replace(/\s/g, "")}`} className="text-creme">{site.telephone}</a>
          {site.horaires.map((h) => (
            <p key={h.jour} className="m-0">{h.jour} : {h.heures}</p>
          ))}
        </div>
        <div className="flex flex-col gap-1">
          <h2 className="m-0 mb-1 text-xs font-bold uppercase tracking-[0.1em] text-sur-nuit">Le Centre</h2>
          <Link href="/le-centre" className="text-creme">Qui sommes-nous</Link>
          <Link href="/le-prophete" className="text-creme">Le Prophète</Link>
          <Link href="/programmes" className="text-creme">Programmes</Link>
          <Link href="/predications" className="text-creme">Prédications</Link>
          <Link href="/dons" className="text-creme">Faire un don</Link>
        </div>
        <div className="flex flex-col gap-1">
          <h2 className="m-0 mb-1 text-xs font-bold uppercase tracking-[0.1em] text-sur-nuit">Suivre</h2>
          <a href={site.youtube} target="_blank" rel="noopener" className="text-creme">Chaîne YouTube du ministère</a>
          {reseaux.map((r) =>
            r.url ? (
              <a key={r.nom} href={r.url} target="_blank" rel="noopener" className="text-creme">{r.nom}</a>
            ) : (
              <span key={r.nom}>{r.nom} : <AConfirmer /></span>
            ),
          )}
        </div>
      </div>
      <div className="mx-auto flex max-w-[1200px] flex-wrap justify-between gap-4 border-t border-nuit-ligne px-5 py-6 text-[13px] text-[#8F8275] sm:px-8">
        <span>© {new Date().getFullYear()} {site.nom}</span>
        <span>
          <Link href="/mentions-legales" className="text-[#8F8275]">Mentions légales</Link> ·{" "}
          <Link href="/confidentialite" className="text-[#8F8275]">Confidentialité</Link>
        </span>
      </div>
    </footer>
  );
}

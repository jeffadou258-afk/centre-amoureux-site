import Link from "next/link";
import Image from "next/image";
import type { Predication } from "@/lib/api/contrats";
import { dateCourte, dateLongue } from "@/lib/format";

function IconeLecture({ taille = 56 }: { taille?: number }) {
  return (
    <span className="flex items-center justify-center rounded-full bg-flamme shadow-[0_10px_30px_-6px_rgba(237,108,16,.7)] transition-transform duration-500 group-hover:scale-110" style={{ width: taille, height: taille }} aria-hidden="true">
      <svg width={taille / 3} height={taille / 3} viewBox="0 0 24 24"><path d="M7 4.5v15l13-7.5z" fill="#1A0E05" /></svg>
    </span>
  );
}

export function CartePredicationVedette({ p, surNuit = true }: { p: Predication; surNuit?: boolean }) {
  return (
    <Link href={`/predications/${p.slug}`} className={`group relative flex min-w-0 flex-col overflow-hidden rounded-3xl no-underline ${surNuit ? "bg-nuit" : "bg-nuit-2"}`}>
      <span className="relative block overflow-hidden">
        <Image src={p.vignette} alt="" width={1280} height={720} sizes="(min-width: 1024px) 760px, 100vw" className="block aspect-video w-full object-cover transition-transform duration-[1.2s] ease-[cubic-bezier(.16,1,.3,1)] group-hover:scale-105" />
        <span className="absolute inset-0 bg-gradient-to-t from-nuit via-nuit/20 to-transparent" aria-hidden="true" />
        <span className="absolute bottom-5 left-5"><IconeLecture /></span>
      </span>
      <span className="flex flex-col gap-1.5 px-6 pb-6 pt-2 text-sur-nuit">
        <span className="text-[13px] text-gris-clair">{p.type}, {dateLongue(p.date)}</span>
        <span className="font-titre text-[clamp(1.15rem,1.9vw,1.45rem)] font-bold leading-snug transition-colors group-hover:text-or">{p.titre}</span>
      </span>
    </Link>
  );
}

export function LignePredication({ p }: { p: Predication }) {
  return (
    <Link href={`/predications/${p.slug}`} className="group grid grid-cols-[112px_1fr] items-center gap-3.5 rounded-2xl p-2 text-encre no-underline transition-colors hover:bg-white sm:grid-cols-[128px_1fr]">
      <span className="overflow-hidden rounded-xl">
        <Image src={p.vignette} alt="" width={280} height={158} className="aspect-video w-full object-cover transition-transform duration-700 group-hover:scale-110" />
      </span>
      <span className="flex flex-col gap-0.5">
        <span className="text-xs text-gris">{p.type}, {dateCourte(p.date)}</span>
        <span className="text-sm font-semibold leading-snug">{p.titre}</span>
      </span>
    </Link>
  );
}

export function CartePredication({ p, className = "" }: { p: Predication; className?: string }) {
  return (
    <Link href={`/predications/${p.slug}`} className={`group flex flex-col gap-3 text-encre no-underline ${className}`}>
      <span className="relative block overflow-hidden rounded-2xl">
        <Image src={p.vignette} alt="" width={640} height={360} sizes="(min-width: 1024px) 360px, 80vw" className="aspect-video w-full object-cover transition-transform duration-700 ease-[cubic-bezier(.16,1,.3,1)] group-hover:scale-[1.06]" />
        <span className="absolute inset-0 flex items-center justify-center bg-nuit/0 opacity-0 transition duration-500 group-hover:bg-nuit/30 group-hover:opacity-100" aria-hidden="true"><IconeLecture taille={48} /></span>
      </span>
      <span className="text-xs text-gris">{p.type}, {dateLongue(p.date)}</span>
      <span className="font-titre text-[16px] font-bold leading-snug transition-colors group-hover:text-flamme-encre">{p.titre}</span>
    </Link>
  );
}

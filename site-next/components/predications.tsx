import Link from "next/link";
import Image from "next/image";
import type { Predication } from "@/lib/api/contrats";
import { dateCourte, dateLongue } from "@/lib/format";

function IconeLecture({ taille = 64 }: { taille?: number }) {
  return (
    <span className="flex items-center justify-center rounded-full bg-flamme" style={{ width: taille, height: taille }} aria-hidden="true">
      <svg width={taille / 3} height={taille / 3} viewBox="0 0 24 24"><path d="M7 4.5v15l13-7.5z" fill="#1A0E05" /></svg>
    </span>
  );
}

export function CartePredicationVedette({ p, surNuit = true }: { p: Predication; surNuit?: boolean }) {
  return (
    <Link href={`/predications/${p.slug}`} className={`group flex min-w-0 flex-col overflow-hidden rounded-[20px] no-underline ${surNuit ? "bg-nuit" : "bg-nuit-2"}`}>
      <span className="relative block">
        <Image src={p.vignette} alt="" width={1280} height={720} sizes="(min-width: 1024px) 760px, 100vw" className="block aspect-video w-full object-cover" />
        <span className="absolute bottom-6 left-6"><IconeLecture /></span>
      </span>
      <span className="flex flex-col gap-2 p-6 text-sur-nuit">
        <span className="text-[13px] font-semibold text-gris-clair">{p.type} · {dateLongue(p.date)}</span>
        <span className="font-titre text-[clamp(1.4rem,2.4vw,1.75rem)] font-extrabold uppercase leading-[1.1] group-hover:text-or">{p.titre}</span>
      </span>
    </Link>
  );
}

export function LignePredication({ p }: { p: Predication }) {
  return (
    <Link href={`/predications/${p.slug}`} className="grid grid-cols-[120px_1fr] items-center gap-3.5 rounded-2xl bg-ivoire p-2.5 text-encre no-underline hover:bg-white sm:grid-cols-[140px_1fr]">
      <Image src={p.vignette} alt="" width={280} height={158} className="aspect-video w-full rounded-[10px] object-cover" />
      <span className="flex flex-col gap-1">
        <span className="text-xs font-semibold text-gris">{p.type} · {dateCourte(p.date)}</span>
        <span className="text-[15px] font-bold leading-snug">{p.titre}</span>
      </span>
    </Link>
  );
}

export function CartePredication({ p }: { p: Predication }) {
  return (
    <Link href={`/predications/${p.slug}`} className="group flex flex-col gap-3 text-encre no-underline">
      <Image src={p.vignette} alt="" width={640} height={360} sizes="(min-width: 1024px) 360px, 100vw" className="aspect-video w-full rounded-2xl object-cover" />
      <span className="text-[13px] font-semibold text-gris">{p.type} · {dateLongue(p.date)}</span>
      <span className="font-titre text-[21px] font-extrabold uppercase leading-[1.15] group-hover:text-flamme-encre">{p.titre}</span>
    </Link>
  );
}

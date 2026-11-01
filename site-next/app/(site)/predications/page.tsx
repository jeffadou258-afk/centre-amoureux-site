import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { Conteneur, Surtitre } from "@/components/ui";
import { CartePredication, CartePredicationVedette } from "@/components/predications";
import { getPredications, getSite } from "@/lib/donnees";
import { dateCourte } from "@/lib/format";

export const metadata: Metadata = {
  title: "Prédications",
  description: "Les prédications et enseignements du Prophète Daniel Jeff Adou, à regarder et partager.",
};

const TYPES = [
  { cle: "Enseignement", libelle: "Enseignements" },
  { cle: "Exhortation", libelle: "Exhortations" },
  { cle: "Prière", libelle: "Prière" },
  { cle: "Culte", libelle: "Cultes" },
] as const;

const sansAccents = (t: string) => t.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();

export default async function PagePredications({ searchParams }: { searchParams: Promise<{ type?: string; q?: string }> }) {
  const { type, q } = await searchParams;
  const [toutes, site] = await Promise.all([getPredications(), getSite()]);
  const [recente] = toutes;
  const recherche = (q ?? "").trim().slice(0, 80);
  const filtrees = toutes.filter(
    (p) => (!type || p.type === type) && (!recherche || sansAccents(`${p.titre} ${p.serie ?? ""} ${p.versets.join(" ")}`).includes(sansAccents(recherche))),
  );
  const series = Array.from(new Set(toutes.map((p) => p.serie).filter((s): s is string => !!s)));
  const filtreActif = !!type || !!recherche;

  const pastille = (actif: boolean) =>
    `inline-flex min-h-11 items-center rounded-full px-[18px] text-sm no-underline ${
      actif ? "bg-encre font-bold text-ivoire hover:text-ivoire" : "border-[1.5px] border-[#D4C6B6] font-semibold text-encre hover:border-encre hover:text-encre"
    }`;

  return (
    <>
      <section className="relative overflow-hidden bg-nuit text-sur-nuit">
        <div className="braises opacity-70" aria-hidden="true" />
        <Conteneur className="entree relative grid items-center gap-12 pb-14 pt-10 md:grid-cols-2">
          <div className="flex flex-col gap-4">
            <Surtitre surNuit>Prédications et enseignements</Surtitre>
            <h1 className="m-0 font-titre text-[clamp(1.85rem,4.4vw,3rem)] font-bold leading-[1.05]">La Parole, chaque semaine</h1>
            <p className="m-0 text-[15px] leading-relaxed text-creme">Les messages du Prophète Daniel Jeff Adou, à regarder, écouter et partager.</p>
          </div>
          {recente && <CartePredicationVedette p={recente} surNuit={false} />}
        </Conteneur>
      </section>

      <Conteneur className="flex flex-col gap-8 pb-24 pt-12">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <nav aria-label="Filtrer par type" className="flex flex-wrap gap-2">
            <Link href="/predications" className={pastille(!type)} aria-current={!type ? "page" : undefined}>Toutes · {toutes.length}</Link>
            {TYPES.map((t) => {
              const n = toutes.filter((p) => p.type === t.cle).length;
              if (!n) return null;
              return (
                <Link key={t.cle} href={`/predications?type=${encodeURIComponent(t.cle)}`} className={pastille(type === t.cle)} aria-current={type === t.cle ? "page" : undefined}>
                  {t.libelle} · {n}
                </Link>
              );
            })}
          </nav>
          <form role="search" action="/predications" className="flex min-w-[min(100%,320px)] flex-col gap-1">
            {type && <input type="hidden" name="type" value={type} />}
            <label htmlFor="recherche" className="text-[13px] font-bold">Rechercher un message</label>
            <div className="flex gap-2">
              <input id="recherche" name="q" type="search" defaultValue={recherche} placeholder="Titre, série, verset…" className="min-h-12 flex-1 rounded-xl border-[1.5px] border-champ bg-white px-4 text-[15px]" />
              <button type="submit" className="min-h-12 rounded-xl bg-encre px-4 text-sm font-bold text-ivoire">Chercher</button>
            </div>
          </form>
        </div>

        {!filtreActif &&
          series.map((serie) => {
            const parties = toutes.filter((p) => p.serie === serie).sort((a, b) => a.date.localeCompare(b.date));
            return (
              <section key={serie} aria-labelledby={`serie-${serie}`} className="grid items-center gap-6 rounded-3xl bg-sable p-7 lg:grid-cols-3">
                <div className="flex flex-col gap-2">
                  <span className="text-xs font-bold text-flamme-encre">Série · {parties.length} messages</span>
                  <h2 id={`serie-${serie}`} className="m-0 font-titre text-[32px] font-bold leading-none">{serie}</h2>
                </div>
                {parties.map((p) => (
                  <Link key={p.slug} href={`/predications/${p.slug}`} className="grid grid-cols-[140px_1fr] items-center gap-3.5 rounded-2xl bg-ivoire p-2.5 text-encre no-underline hover:bg-white">
                    <Image src={p.vignette} alt="" width={280} height={158} className="aspect-video w-full rounded-[10px] object-cover" />
                    <span className="flex flex-col gap-1">
                      <span className="text-xs font-semibold text-gris">{dateCourte(p.date)}</span>
                      <span className="text-[15px] font-bold leading-snug">{p.titre}</span>
                    </span>
                  </Link>
                ))}
              </section>
            );
          })}

        {filtrees.length ? (
          <div className="grid gap-7 sm:grid-cols-2 lg:grid-cols-3">
            {filtrees.map((p) => <CartePredication key={p.slug} p={p} />)}
          </div>
        ) : (
          <p role="status" className="m-0 rounded-2xl bg-sable p-6 text-[15px]">
            Aucun message ne correspond à « {recherche} ». <Link href="/predications">Voir toutes les prédications</Link>
          </p>
        )}

        <p className="m-0 text-[13px] text-gris">
          Vidéos hébergées par YouTube : le lecteur ne se charge qu’au clic, sans traceur avant votre choix.{" "}
          <a href={site.youtube} target="_blank" rel="noopener">S’abonner à la chaîne du ministère</a>
        </p>
      </Conteneur>
    </>
  );
}

import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Conteneur, Surtitre } from "@/components/ui";
import { CartePredication } from "@/components/predications";
import { LecteurYoutube } from "@/components/lecteur-youtube";
import { getPredication, getPredications } from "@/lib/donnees";
import { dateLongue, lienWhatsApp } from "@/lib/format";

type Params = { params: Promise<{ slug: string }> };

export async function generateStaticParams() {
  return (await getPredications()).map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const p = await getPredication((await params).slug);
  if (!p) return { title: "Prédication introuvable" };
  return {
    title: p.titre,
    description: p.resume ?? `${p.type} du ${p.orateur}, ${dateLongue(p.date)}.`,
    openGraph: { images: [{ url: p.vignette, width: 1280, height: 720 }] },
  };
}

export default async function PagePredication({ params }: Params) {
  const { slug } = await params;
  const p = await getPredication(slug);
  if (!p) notFound();
  const autres = (await getPredications()).filter((x) => x.slug !== p.slug && (x.serie ? x.serie === p.serie : true)).slice(0, 3);
  const urlPage = `${process.env.NEXT_PUBLIC_SITE_URL ?? ""}/predications/${p.slug}`;

  const donneesStructurees = {
    "@context": "https://schema.org",
    "@type": "VideoObject",
    name: p.titre,
    uploadDate: p.date,
    thumbnailUrl: p.vignette,
    embedUrl: `https://www.youtube-nocookie.com/embed/${p.youtube_id}`,
    description: p.resume ?? `${p.type} — ${p.orateur}`,
  };

  return (
    <>
      <section className="bg-nuit text-sur-nuit">
        <Conteneur className="flex flex-col gap-6 pb-12 pt-8">
          <Link href="/predications" className="text-sm font-bold text-or">← Toutes les prédications</Link>
          <LecteurYoutube id={p.youtube_id} titre={p.titre} vignette={p.vignette} />
          <div className="flex flex-col gap-3">
            <Surtitre surNuit>{p.type} · {dateLongue(p.date)}{p.serie ? ` · Série « ${p.serie} »` : ""}</Surtitre>
            <h1 className="m-0 font-titre text-[clamp(2rem,4vw,3.25rem)] font-black uppercase leading-none tracking-[-0.02em]">{p.titre}</h1>
            <p className="m-0 text-creme">{p.orateur}</p>
          </div>
        </Conteneur>
      </section>
      <Conteneur className="grid gap-12 py-14 lg:grid-cols-[1fr_320px]">
        <div className="flex flex-col gap-4">
          {p.resume ? (
            <p className="m-0 text-lg leading-relaxed text-texte-2">{p.resume}</p>
          ) : (
            <p className="m-0 text-[15px] text-gris">Le résumé de ce message sera ajouté par le secrétariat.</p>
          )}
          {p.versets.length > 0 && (
            <p className="m-0 font-verset text-2xl italic">{p.versets.join(" · ")}</p>
          )}
        </div>
        <aside className="flex flex-col gap-3">
          <a className="inline-flex min-h-12 items-center justify-center rounded-full bg-encre px-6 font-bold text-ivoire no-underline hover:text-ivoire" href={lienWhatsApp("", `${p.titre} — ${urlPage}`)} target="_blank" rel="noopener">
            Partager sur WhatsApp
          </a>
        </aside>
      </Conteneur>
      {autres.length > 0 && (
        <section className="bg-sable">
          <Conteneur className="flex flex-col gap-6 py-14">
            <h2 className="m-0 font-titre text-2xl font-black uppercase">{p.serie ? "Dans la même série" : "À écouter aussi"}</h2>
            <div className="grid gap-7 sm:grid-cols-2 lg:grid-cols-3">
              {autres.map((x) => <CartePredication key={x.slug} p={x} />)}
            </div>
          </Conteneur>
        </section>
      )}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(donneesStructurees).replace(/</g, "\\u003c") }} />
    </>
  );
}

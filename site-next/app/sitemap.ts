import type { MetadataRoute } from "next";
import { getPredications } from "@/lib/donnees";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  const fixes = ["", "/le-centre", "/le-prophete", "/programmes", "/predications", "/priere", "/temoignages", "/nous-rejoindre", "/dons", "/mentions-legales", "/confidentialite"];
  const predications = await getPredications();
  return [
    ...fixes.map((c) => ({ url: `${base}${c}` })),
    ...predications.map((p) => ({ url: `${base}/predications/${p.slug}`, lastModified: p.date })),
  ];
}

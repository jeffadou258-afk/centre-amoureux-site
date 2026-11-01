import "server-only";
import { z } from "zod";
import { apiBranchee, config } from "@/lib/config";
import { Evenement, Liste, Predication, Site, Temoignage } from "@/lib/api/contrats";
import { EVENEMENTS, PREDICATIONS, SITE, TEMOIGNAGES } from "@/lib/contenu";
import { aujourdhui } from "@/lib/format";

/**
 * SOURCE UNIQUE DES DONNÉES DU SITE.
 *  · API de Hermes branchée (CAD_API_URL) → lecture `GET /v1/public/...`,
 *    réponse validée par les schémas du contrat, mise en cache par étiquette
 *    (rafraîchie par /api/revalidate à chaque publication).
 *  · Sinon → contenu réel actuel (lib/contenu), le même que le site statique.
 * Une API branchée mais en panne lève une erreur : jamais de repli silencieux
 * sur une copie qui pourrait être périmée.
 */
export class ErreurLecture extends Error {
  constructor(public chemin: string, public statut: number) {
    super(`API ${chemin} : HTTP ${statut}`);
  }
}

async function lire<T extends z.ZodTypeAny>(chemin: string, schema: T, etiquette: string): Promise<z.infer<T>> {
  const reponse = await fetch(`${config.apiUrl}/v1/public/${chemin}`, {
    headers: { Accept: "application/json" },
    next: { tags: [etiquette], revalidate: 3600 },
  });
  if (!reponse.ok) throw new ErreurLecture(chemin, reponse.status);
  return schema.parse(await reponse.json());
}

export async function getSite(): Promise<Site> {
  return apiBranchee() ? lire("site", Site, "site") : SITE;
}

export async function getPredications(): Promise<Predication[]> {
  const liste = apiBranchee()
    ? (await lire("predications?par_page=100", Liste(Predication), "predications")).elements
    : PREDICATIONS;
  return [...liste].sort((a, b) => b.date.localeCompare(a.date));
}

export async function getPredication(slug: string): Promise<Predication | null> {
  if (apiBranchee()) {
    try {
      return await lire(`predications/${encodeURIComponent(slug)}`, Predication, `predication:${slug}`);
    } catch (e) {
      // Seul un 404 signifie « n'existe pas » ; une panne reste une panne.
      if (e instanceof ErreurLecture && e.statut === 404) return null;
      throw e;
    }
  }
  return PREDICATIONS.find((p) => p.slug === slug) ?? null;
}

export async function getEvenementsAVenir(maintenant = aujourdhui()): Promise<Evenement[]> {
  const liste = apiBranchee()
    ? (await lire("evenements?a_venir=1&par_page=100", Liste(Evenement), "evenements")).elements
    : EVENEMENTS;
  return liste.filter((e) => (e.fin ?? e.debut) >= maintenant).sort((a, b) => a.debut.localeCompare(b.debut));
}

export async function getTemoignages(): Promise<Temoignage[]> {
  return apiBranchee() ? (await lire("temoignages?par_page=50", Liste(Temoignage), "temoignages")).elements : TEMOIGNAGES;
}

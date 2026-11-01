import { z } from "zod";

/**
 * CONTRATS API — PROPOSITION À VALIDER PAR HERMES
 * (document « Site officiel CAD — Architecture frontend et contrats API »).
 *
 * Ces schémas valident CHAQUE réponse de l'API avant affichage : un écart de
 * contrat devient une erreur visible en développement, jamais une page fausse.
 * Le jour où Hermes publie son OpenAPI, ces types seront régénérés depuis lui.
 */

export const Horaire = z.object({
  jour: z.string(),
  libelle: z.string(),
  heures: z.string(),
  precision: z.string().optional(),
});

export const Site = z.object({
  nom: z.string(),
  adresse: z.string(),
  repere: z.string(),
  ville: z.string(),
  telephone: z.string(),
  telephone2: z.string().optional(),
  whatsapp: z.string(),
  email: z.string().nullable(),
  youtube: z.string().url(),
  facebook: z.string().url().nullable(),
  instagram: z.string().url().nullable(),
  tiktok: z.string().url().nullable(),
  fondation: z.string(),
  horaires: z.array(Horaire),
  theme_du_mois: z
    .object({ titre: z.string(), mois: z.string(), suivant: z.object({ titre: z.string(), mois: z.string() }).optional() })
    .nullable(),
});
export type Site = z.infer<typeof Site>;

export const TypePredication = z.enum(["Enseignement", "Exhortation", "Prière", "Culte"]);

export const Predication = z.object({
  slug: z.string(),
  titre: z.string(),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  type: TypePredication,
  orateur: z.string(),
  serie: z.string().nullable(),
  youtube_id: z.string(),
  vignette: z.string(),
  resume: z.string().nullable(),
  versets: z.array(z.string()),
});
export type Predication = z.infer<typeof Predication>;

export const Evenement = z.object({
  slug: z.string(),
  titre: z.string(),
  debut: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  fin: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).nullable(),
  heure: z.string().nullable(),
  details: z.string().nullable(),
  lieu: z.string(),
  affiche: z.string().nullable(),
  /** Date ou horaire pas encore arrêtés : affichés « à confirmer », jamais inventés. */
  a_confirmer: z.string().nullable(),
  mise_en_avant: z.boolean(),
});
export type Evenement = z.infer<typeof Evenement>;

export const Temoignage = z.object({
  id: z.string(),
  prenom_affiche: z.string(),
  titre: z.string(),
  texte: z.string(),
  date: z.string(),
});
export type Temoignage = z.infer<typeof Temoignage>;

export const Liste = <T extends z.ZodTypeAny>(element: T) =>
  z.object({ elements: z.array(element), total: z.number().int(), page: z.number().int(), par_page: z.number().int() });

// ── Envois (formulaires) ────────────────────────────────────────────────
export const ConfidentialitePriere = z.enum(["equipe", "prophete"]);

export const DemandePriere = z.object({
  nom: z.string().trim().max(120).optional(),
  contact: z.string().trim().max(160).optional(),
  sujet: z.enum(["Famille", "Santé", "Travail et finances", "Vie spirituelle", "Autre"]),
  message: z.string().trim().min(5, "Écrivez au moins quelques mots.").max(4000, "4 000 caractères au plus."),
  confidentialite: ConfidentialitePriere,
  consentement: z.literal(true, { error: "Votre accord est nécessaire pour que nous conservions la demande." }),
});
export type DemandePriere = z.infer<typeof DemandePriere>;

export const NouveauTemoignage = z.object({
  nom: z.string().trim().min(1, "Indiquez un nom ou un pseudonyme.").max(120),
  affichage: z.enum(["nom", "prenom", "anonyme"]),
  titre: z.string().trim().min(3, "Donnez un titre.").max(180),
  texte: z.string().trim().min(20, "Racontez en quelques phrases (20 caractères au moins).").max(4000),
  consentement_publication: z.literal(true, { error: "Votre accord de publication est nécessaire." }),
});
export type NouveauTemoignage = z.infer<typeof NouveauTemoignage>;

export const IntentionDon = z.object({
  montant: z.coerce.number().int("Montant en francs CFA, sans décimales.").min(100, "100 FCFA au minimum.").max(10_000_000),
  affectation: z.enum(["dime", "offrande", "projet"]),
  moyen: z.string().min(1),
  email: z.string().trim().email("Adresse e-mail invalide.").optional().or(z.literal("")),
});
export type IntentionDon = z.infer<typeof IntentionDon>;

export const ErreurApi = z.object({
  erreur: z.object({ code: z.string(), message: z.string(), champs: z.record(z.string(), z.string()).optional() }),
});

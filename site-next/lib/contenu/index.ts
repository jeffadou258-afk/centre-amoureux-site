import type { Evenement, Predication, Site, Temoignage } from "@/lib/api/contrats";

/**
 * CONTENU RÉEL ACTUEL DU CENTRE — repris du site statique validé
 * (outils/generer.py, décisions du client du 31/10/2026) et de l'affiche
 * officielle « Remporter les batailles par la prière ».
 *
 * Ce n'est PAS un jeu de données fictif : c'est ce que le site public affiche
 * déjà. Il sert de source tant que l'API de Hermes n'est pas branchée
 * (CAD_API_URL vide). Ce qui n'est pas fourni par le Centre reste `null` et
 * s'affiche « à confirmer » — jamais inventé.
 */

export const SITE: Site = {
  nom: "Centre des Amoureux de Dieu",
  adresse: "Cocody Riviera 2, en face de l’imprimerie DA Communication",
  repere: "Du rond-point de la Riviera 2 vers la station-service Petroleum : tournez à gauche puis 100 m, en face de l’imprimerie DA Communication.",
  ville: "Abidjan, Côte d’Ivoire",
  telephone: "+225 07 87 59 32 89",
  telephone2: "+225 07 02 82 47 72",
  whatsapp: "+2250787593289",
  email: null,
  youtube: "https://www.youtube.com/@jeffadou3161",
  facebook: null,
  instagram: null,
  tiktok: null,
  fondation: "octobre 2023",
  horaires: [
    { jour: "Dimanche", libelle: "Culte d’adoration", heures: "14h00 – 18h30" },
    { jour: "Mercredi", libelle: "Culte de la Parole", heures: "19h00 – 21h00", precision: "une semaine sur deux" },
  ],
  theme_du_mois: {
    titre: "Remporter les batailles par la prière",
    mois: "Novembre 2026",
    suivant: { titre: "Atmosphère de miracle", mois: "Décembre 2026" },
  },
};

export const PROPHETE = {
  nom: "Prophète Daniel Jeff Adou",
  nomCourt: "Daniel Jeff Adou",
  role: "Prophète et pasteur du Centre des Amoureux de Dieu",
};

export const VISION =
  "Former des ouvriers et des serviteurs de Dieu, bâtir une armée d’amoureux passionnés pour Dieu et les équiper pour impacter la société.";

export const MISSION =
  "Par la prédication de la Parole, l’évangélisation, la formation biblique et le développement de leaders, nous équipons nos membres pour qu’ils deviennent des serviteurs fidèles capables de transformer leur famille, leur communauté et impacter positivement la société.";

export const VALEURS = [
  { nom: "Amour", definition: "Servir et agir avec compassion envers Dieu et envers les autres.", reference: "Jean 13 : 34-35" },
  { nom: "Foi", definition: "Croire en Dieu et en Sa Parole dans toutes les situations, et vivre selon cette confiance.", reference: "Hébreux 11 : 1" },
  { nom: "Intégrité", definition: "Être honnête, transparent et fidèle dans toutes nos actions.", reference: "Proverbes 10 : 9" },
  { nom: "Crainte de Dieu", definition: "Respecter et honorer Dieu dans nos pensées, paroles et actions.", reference: "Proverbes 9 : 10" },
  { nom: "Obéissance à la Parole", definition: "Mettre en pratique les enseignements bibliques dans notre vie quotidienne.", reference: "Jacques 1 : 22" },
  { nom: "Excellence", definition: "Poursuivre la qualité et la diligence dans tout ce que nous faisons pour glorifier Dieu.", reference: "Colossiens 3 : 23" },
] as const;

const ORATEUR = "Prophète Daniel Jeff Adou";
const v = (id: string) => `/img/predications/${id}.jpg`;

/** Titres repris tels que publiés sur la chaîne YouTube du ministère. */
export const PREDICATIONS: Predication[] = [
  { slug: "tous-les-grands-ont-reve-grand", titre: "Tous les grands ont d'abord rêvé grand", date: "2026-10-17", type: "Exhortation", orateur: ORATEUR, serie: null, youtube_id: "Vke4iYzemIs", vignette: v("Vke4iYzemIs"), resume: null, versets: [] },
  { slug: "onction-royale-10-choses-a-savoir", titre: "10 CHOSES A SAVOIR SUR L'ONCTION ROYALE", date: "2026-10-16", type: "Enseignement", orateur: ORATEUR, serie: null, youtube_id: "SXql767Lo7w", vignette: v("SXql767Lo7w"), resume: null, versets: [] },
  { slug: "onction-royale-10-choses", titre: "10 CHOSES A SAVOIR SUR L'ONCTION ROYALE", date: "2026-10-12", type: "Enseignement", orateur: ORATEUR, serie: null, youtube_id: "jrefqSertlc", vignette: v("jrefqSertlc"), resume: null, versets: [] },
  { slug: "huile-coeur-et-trone", titre: "L'huile, le cœur et le trône", date: "2026-09-28", type: "Enseignement", orateur: ORATEUR, serie: "L’huile, le cœur et le trône", youtube_id: "2CHnQLRtN0Y", vignette: v("2CHnQLRtN0Y"), resume: null, versets: [] },
  { slug: "prions-ensemble", titre: "PRIONS ENSEMBLE", date: "2026-09-24", type: "Prière", orateur: ORATEUR, serie: null, youtube_id: "-hKzzUDnh0E", vignette: v("-hKzzUDnh0E"), resume: null, versets: [] },
  { slug: "huile-coeur-et-trone-partie-1", titre: "L'HUILE LE COEUR ET LE TRONE (PARTIE 1)", date: "2026-09-22", type: "Enseignement", orateur: ORATEUR, serie: "L’huile, le cœur et le trône", youtube_id: "OlT6R0wc0JQ", vignette: v("OlT6R0wc0JQ"), resume: null, versets: [] },
  { slug: "reconnaitre-un-sorcier", titre: "Comment reconnaître un sorcier", date: "2026-08-12", type: "Enseignement", orateur: ORATEUR, serie: null, youtube_id: "_fldckxVCDI", vignette: v("_fldckxVCDI"), resume: null, versets: [] },
  { slug: "service-prophetique", titre: "Service prophétique", date: "2026-08-12", type: "Culte", orateur: ORATEUR, serie: null, youtube_id: "h8dCZFevdI8", vignette: v("h8dCZFevdI8"), resume: null, versets: [] },
];

const LIEU = "Cocody Riviera 2";

/** Programme communiqué par le Centre pour novembre 2026 (affiche officielle et programme validé). */
export const EVENEMENTS: Evenement[] = [
  { slug: "remporter-les-batailles-par-la-priere", titre: "Remporter les batailles par la prière", debut: "2026-11-01", fin: null, heure: "dès 14h00", details: "Culte d’ouverture du thème de novembre, avec le Prophète Daniel Jeff Adou.", lieu: LIEU, affiche: "/img/affiches/remporter-les-batailles.jpg", a_confirmer: null, mise_en_avant: true },
  { slug: "jeune-14-jours-novembre-2026", titre: "14 jours de jeûne pour vivre la gloire de Dieu", debut: "2026-11-09", fin: "2026-11-22", heure: null, details: "Prière en ligne chaque jour à 5h30 et 21h00.", lieu: "En ligne et au Centre", affiche: null, a_confirmer: null, mise_en_avant: false },
  { slug: "veillee-20-novembre-2026", titre: "Veillée de prière", debut: "2026-11-20", fin: null, heure: null, details: null, lieu: LIEU, affiche: null, a_confirmer: "Horaire à confirmer", mise_en_avant: false },
  { slug: "anniversaire-3-ans", titre: "Culte d’anniversaire : le Centre a 3 ans", debut: "2026-11-22", fin: null, heure: null, details: "Dernier jour du jeûne de 14 jours.", lieu: LIEU, affiche: null, a_confirmer: "Horaire à confirmer", mise_en_avant: false },
  { slug: "sortie-des-ouvriers", titre: "Sortie des ouvriers", debut: "2026-11-28", fin: null, heure: null, details: null, lieu: "Lieu à confirmer", affiche: null, a_confirmer: "28 novembre ou 5 décembre : date à confirmer", mise_en_avant: false },
];

/** Aucun témoignage n'a encore été validé pour publication. */
export const TEMOIGNAGES: Temoignage[] = [];

/** Annonce validée : les cultes du matin commencent en janvier 2027 (horaire non communiqué). */
export const ANNONCES = ["À partir de janvier 2027 : cultes du matin (horaire à confirmer)."];

import { describe, expect, it } from "vitest";
import { DemandePriere, IntentionDon, NouveauTemoignage, Predication } from "@/lib/api/contrats";
import { EVENEMENTS, PREDICATIONS, SITE } from "@/lib/contenu";
import { Evenement, Site } from "@/lib/api/contrats";

describe("le contenu réel respecte les contrats proposés à Hermes", () => {
  it("site", () => expect(Site.safeParse(SITE).success).toBe(true));
  it("8 prédications valides, slugs uniques", () => {
    PREDICATIONS.forEach((p) => expect(Predication.safeParse(p).success).toBe(true));
    expect(PREDICATIONS).toHaveLength(8);
    expect(new Set(PREDICATIONS.map((p) => p.slug)).size).toBe(8);
  });
  it("événements valides", () => EVENEMENTS.forEach((e) => expect(Evenement.safeParse(e).success).toBe(true)));
  it("rien d'inventé : les inconnues restent nulles ou « à confirmer »", () => {
    expect(SITE.email).toBeNull();
    expect(SITE.facebook).toBeNull();
    expect(EVENEMENTS.find((e) => e.slug === "sortie-des-ouvriers")?.a_confirmer).toMatch(/à confirmer/);
  });
});

describe("validation des formulaires", () => {
  const priere = { sujet: "Famille", message: "Priez pour nous", confidentialite: "equipe", consentement: true } as const;
  it("accepte une demande complète", () => expect(DemandePriere.safeParse(priere).success).toBe(true));
  it("refuse sans consentement", () => expect(DemandePriere.safeParse({ ...priere, consentement: false }).success).toBe(false));
  it("refuse un message vide", () => expect(DemandePriere.safeParse({ ...priere, message: "   " }).success).toBe(false));
  it("témoignage : 20 caractères minimum", () =>
    expect(NouveauTemoignage.safeParse({ nom: "A", affichage: "prenom", titre: "Merci", texte: "court", consentement_publication: true }).success).toBe(false));
  it("don : montant minimum 100 FCFA, entier", () => {
    expect(IntentionDon.safeParse({ montant: "50", affectation: "dime", moyen: "Wave" }).success).toBe(false);
    expect(IntentionDon.safeParse({ montant: "5000", affectation: "dime", moyen: "Wave" }).success).toBe(true);
    expect(IntentionDon.safeParse({ montant: "12.5", affectation: "dime", moyen: "Wave" }).success).toBe(false);
  });
});

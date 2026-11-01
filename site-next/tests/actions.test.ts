import { describe, expect, it, vi } from "vitest";

describe("sans API branchée, rien n'est simulé", () => {
  it("la prière n'est pas « envoyée » et le texte est rendu", async () => {
    vi.stubEnv("CAD_API_URL", "");
    const { envoyerPriere } = await import("@/lib/actions");
    const fd = new FormData();
    fd.set("sujet", "Famille"); fd.set("message", "Priez pour ma famille"); fd.set("confidentialite", "equipe"); fd.set("consentement", "on");
    const espion = vi.spyOn(globalThis, "fetch");
    const r = await envoyerPriere({ statut: "initial" }, fd);
    expect(r.statut).toBe("non-branche");
    expect(r.valeurs?.message).toBe("Priez pour ma famille");
    expect(espion).not.toHaveBeenCalled();
  });
  it("le don ne prépare aucun paiement", async () => {
    vi.stubEnv("CAD_API_URL", "");
    const { preparerDon } = await import("@/lib/actions");
    const fd = new FormData();
    fd.set("montant", "5 000"); fd.set("affectation", "offrande"); fd.set("moyen", "Wave");
    const r = await preparerDon({ statut: "initial" }, fd);
    expect(r.statut).toBe("non-branche");
    expect(r.urlPaiement).toBeUndefined();
  });
});

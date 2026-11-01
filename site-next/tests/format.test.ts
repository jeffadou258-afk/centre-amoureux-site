import { describe, expect, it } from "vitest";
import { blocDate, dateLongue, lienWhatsApp, periode } from "@/lib/format";

describe("dates (jours civils d'Abidjan, sans décalage de fuseau)", () => {
  it("écrit le 1er du mois", () => expect(dateLongue("2026-11-01")).toBe("1er novembre 2026"));
  it("donne le bon jour de la semaine", () => {
    expect(blocDate("2026-11-01")).toEqual({ jour: "DIM.", numero: "1", mois: "NOV." });
    expect(blocDate("2026-11-20").jour).toBe("VEN.");
    expect(blocDate("2026-11-22").jour).toBe("DIM.");
  });
  it("écrit une période dans le même mois", () => expect(periode("2026-11-09", "2026-11-22")).toBe("du 9 au 22 novembre 2026"));
  it("écrit une date seule", () => expect(periode("2026-11-20", null)).toBe("20 novembre 2026"));
});

describe("WhatsApp", () => {
  it("nettoie le numéro et encode le texte", () =>
    expect(lienWhatsApp("+225 07 87 59 32 89", "Bonjour, prière")).toBe("https://wa.me/2250787593289?text=Bonjour%2C%20pri%C3%A8re"));
});

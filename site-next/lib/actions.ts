"use server";

import { z } from "zod";
import { apiBranchee, config } from "@/lib/config";
import { DemandePriere, IntentionDon, NouveauTemoignage } from "@/lib/api/contrats";

export type EtatEnvoi = {
  statut: "initial" | "succes" | "invalide" | "non-branche" | "echec";
  message?: string;
  erreurs?: Record<string, string>;
  valeurs?: Record<string, string>;
  urlPaiement?: string;
};

const valeursDe = (fd: FormData) =>
  Object.fromEntries([...fd.entries()].filter(([k, v]) => typeof v === "string" && !k.startsWith("$") && k !== "cf-turnstile-response")) as Record<string, string>;

function erreursDe(e: z.ZodError): Record<string, string> {
  const sortie: Record<string, string> = {};
  for (const i of e.issues) {
    const cle = String(i.path[0] ?? "formulaire");
    if (!sortie[cle]) sortie[cle] = i.message;
  }
  return sortie;
}

const NON_BRANCHE =
  "L’envoi en ligne n’est pas encore branché : rien n’a été transmis. Votre texte est conservé ci-dessous. Vous pouvez nous écrire dès maintenant sur WhatsApp.";

/** Envoi vers l'API de Hermes. Aucune donnée n'est stockée par le site lui-même. */
async function envoyer(chemin: string, corps: unknown, jeton: string | null): Promise<{ ok: boolean; donnees?: unknown; message?: string }> {
  try {
    const r = await fetch(`${config.apiUrl}/v1/public/${chemin}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ ...(corps as object), jeton_antirobot: jeton }),
      cache: "no-store",
    });
    const donnees = await r.json().catch(() => null);
    if (r.ok) return { ok: true, donnees };
    if (r.status === 429) return { ok: false, message: "Trop d’envois depuis votre connexion. Réessayez dans un moment." };
    return { ok: false, message: (donnees as { erreur?: { message?: string } } | null)?.erreur?.message ?? "L’envoi n’a pas abouti." };
  } catch {
    return { ok: false, message: "Le service est momentanément injoignable. Votre texte est conservé : réessayez dans un instant." };
  }
}

export async function envoyerPriere(_prec: EtatEnvoi, fd: FormData): Promise<EtatEnvoi> {
  const valeurs = valeursDe(fd);
  const r = DemandePriere.safeParse({
    nom: valeurs.nom || undefined,
    contact: valeurs.contact || undefined,
    sujet: valeurs.sujet,
    message: valeurs.message ?? "",
    confidentialite: valeurs.confidentialite,
    consentement: valeurs.consentement === "on",
  });
  if (!r.success) return { statut: "invalide", erreurs: erreursDe(r.error), valeurs };
  if (!apiBranchee()) return { statut: "non-branche", message: NON_BRANCHE, valeurs };
  const res = await envoyer("prieres", r.data, (fd.get("cf-turnstile-response") as string) || null);
  return res.ok ? { statut: "succes" } : { statut: "echec", message: res.message, valeurs };
}

export async function envoyerTemoignage(_prec: EtatEnvoi, fd: FormData): Promise<EtatEnvoi> {
  const valeurs = valeursDe(fd);
  const r = NouveauTemoignage.safeParse({
    nom: valeurs.nom ?? "",
    affichage: valeurs.affichage,
    titre: valeurs.titre ?? "",
    texte: valeurs.texte ?? "",
    consentement_publication: valeurs.consentement_publication === "on",
  });
  if (!r.success) return { statut: "invalide", erreurs: erreursDe(r.error), valeurs };
  if (!apiBranchee()) return { statut: "non-branche", message: NON_BRANCHE, valeurs };
  const res = await envoyer("temoignages", r.data, (fd.get("cf-turnstile-response") as string) || null);
  return res.ok ? { statut: "succes" } : { statut: "echec", message: res.message, valeurs };
}

export async function preparerDon(_prec: EtatEnvoi, fd: FormData): Promise<EtatEnvoi> {
  const valeurs = valeursDe(fd);
  const r = IntentionDon.safeParse({
    montant: (valeurs.montant ?? "").replace(/[\s.]/g, ""),
    affectation: valeurs.affectation,
    moyen: valeurs.moyen ?? "",
    email: valeurs.email ?? "",
  });
  if (!r.success) return { statut: "invalide", erreurs: erreursDe(r.error), valeurs };
  if (!apiBranchee()) {
    return {
      statut: "non-branche",
      message: "Le paiement en ligne n’est pas encore activé : aucun montant n’a été prélevé. Vous pouvez donner sur place lors des cultes, ou contacter le secrétariat.",
      valeurs,
    };
  }
  const res = await envoyer("dons", { ...r.data, devise: "XOF" }, (fd.get("cf-turnstile-response") as string) || null);
  const url = (res.donnees as { url_paiement?: string } | undefined)?.url_paiement;
  // Seule une adresse HTTPS renvoyée par l'API est suivie ; jamais une adresse saisie.
  if (res.ok && url && url.startsWith("https://")) return { statut: "succes", urlPaiement: url };
  return { statut: "echec", message: res.message ?? "Le paiement n’a pas pu être préparé.", valeurs };
}

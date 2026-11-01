"use client";

import { useActionState, useEffect } from "react";
import Script from "next/script";
import type { EtatEnvoi } from "@/lib/actions";
import { envoyerPriere, envoyerTemoignage, preparerDon } from "@/lib/actions";

const champ = "min-h-[52px] w-full rounded-xl border-[1.5px] border-champ bg-white px-4 text-base text-encre";
const champErreur = "border-2 border-[#B3261E]";

function Erreur({ id, message }: { id: string; message?: string }) {
  if (!message) return null;
  return <span id={id} className="text-sm font-semibold text-[#B3261E]">{message}</span>;
}

function AntiRobot() {
  const cle = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY;
  if (!cle) return null;
  return (
    <>
      <Script src="https://challenges.cloudflare.com/turnstile/v0/api.js" strategy="lazyOnload" />
      <div className="cf-turnstile" data-sitekey={cle} data-language="fr" />
    </>
  );
}

function Retour({ etat, whatsapp, succes }: { etat: EtatEnvoi; whatsapp: string; succes: string }) {
  if (etat.statut === "succes") {
    return (
      <div role="status" className="flex items-start gap-3.5 rounded-2xl border border-ligne bg-white p-5">
        <span className="flex h-9 w-9 flex-none items-center justify-center rounded-full bg-[#EAF4EC]" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1E6B34" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
        </span>
        <span className="font-bold">{succes}</span>
      </div>
    );
  }
  if (etat.statut === "non-branche" || etat.statut === "echec") {
    return (
      <div role="alert" className="flex flex-col gap-2 rounded-2xl border border-[#F3B9B3] bg-[#FDECEA] p-5">
        <span className="font-bold text-[#8A1C14]">L’envoi n’a pas abouti.</span>
        <span className="text-sm leading-normal text-texte-2">{etat.message}</span>
        <a href={whatsapp} target="_blank" rel="noopener" className="self-start font-bold">Écrire sur WhatsApp →</a>
      </div>
    );
  }
  if (etat.statut === "invalide") {
    return <p role="alert" className="m-0 font-semibold text-[#B3261E]">Certains champs sont à compléter : voir ci-dessus.</p>;
  }
  return null;
}

const ETAT_INITIAL: EtatEnvoi = { statut: "initial" };

export function FormulairePriere({ whatsapp }: { whatsapp: string }) {
  const [etat, action, enCours] = useActionState(envoyerPriere, ETAT_INITIAL);
  const v = etat.valeurs ?? {};
  const e = etat.erreurs ?? {};
  if (etat.statut === "succes") return <Retour etat={etat} whatsapp={whatsapp} succes="Votre demande est bien arrivée. Nous prions avec vous." />;
  return (
    <form action={action} noValidate className="flex flex-col gap-5">
      <div className="flex flex-col gap-1.5">
        <label htmlFor="p-nom" className="font-bold">Votre prénom <span className="font-medium text-gris">(facultatif)</span></label>
        <input id="p-nom" name="nom" autoComplete="given-name" defaultValue={v.nom} className={champ} />
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="p-contact" className="font-bold">Téléphone ou e-mail <span className="font-medium text-gris">(si vous souhaitez être rappelé)</span></label>
        <input id="p-contact" name="contact" defaultValue={v.contact} className={champ} />
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="p-sujet" className="font-bold">Sujet</label>
        <select id="p-sujet" name="sujet" defaultValue={v.sujet ?? ""} aria-invalid={!!e.sujet} aria-describedby={e.sujet ? "p-sujet-err" : undefined} className={`${champ} px-3 ${e.sujet ? champErreur : ""}`}>
          <option value="" disabled>Choisir…</option>
          <option>Famille</option><option>Santé</option><option>Travail et finances</option><option>Vie spirituelle</option><option>Autre</option>
        </select>
        <Erreur id="p-sujet-err" message={e.sujet && "Choisissez un sujet."} />
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="p-message" className="font-bold">Votre demande</label>
        <textarea id="p-message" name="message" rows={6} maxLength={4000} defaultValue={v.message} aria-invalid={!!e.message} aria-describedby="p-message-aide" className={`${champ} py-3 ${e.message ? champErreur : ""}`} />
        <span id="p-message-aide" className="text-[13px] text-gris">4 000 caractères au plus.</span>
        <Erreur id="p-message-err" message={e.message} />
      </div>
      <fieldset className="m-0 flex flex-col gap-2.5 border-0 p-0">
        <legend className="mb-2 font-bold">Qui peut lire votre demande ?</legend>
        {[
          { valeur: "equipe", titre: "L’équipe de prière", aide: "Les intercesseurs du Centre" },
          { valeur: "prophete", titre: "Le Prophète seulement", aide: "Pour une situation très personnelle" },
        ].map((o) => (
          <label key={o.valeur} className="flex cursor-pointer items-start gap-3 rounded-2xl border-[1.5px] border-[#D4C6B6] bg-white p-3.5 has-[:checked]:border-2 has-[:checked]:border-flamme">
            <input type="radio" name="confidentialite" value={o.valeur} defaultChecked={(v.confidentialite ?? "equipe") === o.valeur} className="mt-0.5 h-5 w-5 accent-[#A64C0B]" />
            <span className="flex flex-col"><span className="font-bold">{o.titre}</span><span className="text-sm text-gris">{o.aide}</span></span>
          </label>
        ))}
      </fieldset>
      <label className="flex items-start gap-3 text-sm leading-normal">
        <input type="checkbox" name="consentement" defaultChecked={v.consentement === "on"} className="h-[22px] w-[22px] flex-none accent-[#A64C0B]" />
        <span>J’accepte que le Centre conserve ma demande le temps de prier pour elle. <a href="/confidentialite">Confidentialité</a></span>
      </label>
      <Erreur id="p-consentement-err" message={e.consentement} />
      <AntiRobot />
      <button type="submit" disabled={enCours} className="min-h-14 rounded-full border-0 bg-flamme text-[15px] font-bold text-sur-flamme disabled:opacity-60">
        {enCours ? "Envoi…" : "Envoyer ma demande"}
      </button>
      <Retour etat={etat} whatsapp={whatsapp} succes="" />
    </form>
  );
}

export function FormulaireTemoignage({ whatsapp }: { whatsapp: string }) {
  const [etat, action, enCours] = useActionState(envoyerTemoignage, ETAT_INITIAL);
  const v = etat.valeurs ?? {};
  const e = etat.erreurs ?? {};
  if (etat.statut === "succes") return <Retour etat={etat} whatsapp={whatsapp} succes="Merci ! L’équipe lira votre témoignage avant toute publication." />;
  return (
    <form action={action} noValidate className="flex flex-col gap-5">
      <div className="flex flex-col gap-1.5">
        <label htmlFor="t-nom" className="font-bold">Nom ou pseudonyme</label>
        <input id="t-nom" name="nom" defaultValue={v.nom} aria-invalid={!!e.nom} className={`${champ} ${e.nom ? champErreur : ""}`} />
        <Erreur id="t-nom-err" message={e.nom} />
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="t-titre" className="font-bold">Titre du témoignage</label>
        <input id="t-titre" name="titre" defaultValue={v.titre} aria-invalid={!!e.titre} className={`${champ} ${e.titre ? champErreur : ""}`} />
        <Erreur id="t-titre-err" message={e.titre} />
      </div>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="t-texte" className="font-bold">Votre témoignage</label>
        <textarea id="t-texte" name="texte" rows={7} maxLength={4000} defaultValue={v.texte} aria-invalid={!!e.texte} placeholder="Racontez ce qui s’est passé, et ce que cela a changé pour vous." className={`${champ} py-3 ${e.texte ? champErreur : ""}`} />
        <Erreur id="t-texte-err" message={e.texte} />
      </div>
      <fieldset className="m-0 flex flex-col gap-2 border-0 p-0">
        <legend className="mb-2 font-bold">Identité affichée</legend>
        {[["nom", "Afficher mon nom"], ["prenom", "Afficher uniquement mon prénom"], ["anonyme", "Rester anonyme"]].map(([val, lib]) => (
          <label key={val} className="flex min-h-11 items-center gap-3">
            <input type="radio" name="affichage" value={val} defaultChecked={(v.affichage ?? "prenom") === val} className="h-5 w-5 accent-[#A64C0B]" /> {lib}
          </label>
        ))}
      </fieldset>
      <label className="flex items-start gap-3 text-sm leading-normal">
        <input type="checkbox" name="consentement_publication" defaultChecked={v.consentement_publication === "on"} className="h-[22px] w-[22px] flex-none accent-[#A64C0B]" />
        <span>J’autorise la publication de mon témoignage après validation par l’équipe du Centre.</span>
      </label>
      <Erreur id="t-consentement-err" message={e.consentement_publication} />
      <AntiRobot />
      <button type="submit" disabled={enCours} className="min-h-14 rounded-full border-0 bg-flamme text-[15px] font-bold text-sur-flamme disabled:opacity-60">
        {enCours ? "Envoi…" : "Envoyer mon témoignage"}
      </button>
      <Retour etat={etat} whatsapp={whatsapp} succes="" />
    </form>
  );
}

export function FormulaireDon({ whatsapp }: { whatsapp: string }) {
  const [etat, action, enCours] = useActionState(preparerDon, ETAT_INITIAL);
  const v = etat.valeurs ?? {};
  const e = etat.erreurs ?? {};
  useEffect(() => {
    if (etat.statut === "succes" && etat.urlPaiement) window.location.assign(etat.urlPaiement);
  }, [etat]);
  const affectations = [["dime", "Dîme"], ["offrande", "Offrande"], ["projet", "Projet"]];
  const moyens = ["Wave", "Orange Money", "MTN Mobile Money", "Moov Money", "Carte bancaire"];
  return (
    <form action={action} noValidate className="flex flex-col gap-6">
      <fieldset className="m-0 flex flex-col gap-2.5 border-0 p-0">
        <legend className="mb-2 text-base font-bold">1. Pour quoi donnez-vous ?</legend>
        <div className="grid grid-cols-3 gap-2">
          {affectations.map(([val, lib]) => (
            <label key={val} className="flex min-h-12 cursor-pointer items-center justify-center rounded-xl border-[1.5px] border-[#D4C6B6] bg-white text-sm font-bold has-[:checked]:border-encre has-[:checked]:bg-encre has-[:checked]:text-ivoire has-[:focus-visible]:outline has-[:focus-visible]:outline-3 has-[:focus-visible]:outline-or">
              <input type="radio" name="affectation" value={val} defaultChecked={(v.affectation ?? "dime") === val} className="sr-only" />{lib}
            </label>
          ))}
        </div>
      </fieldset>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="d-montant" className="text-base font-bold">2. Montant (FCFA)</label>
        <input id="d-montant" name="montant" inputMode="numeric" autoComplete="off" placeholder="Ex. : 5 000" defaultValue={v.montant} aria-invalid={!!e.montant} className={`${champ} text-[15px] ${e.montant ? champErreur : ""}`} />
        <Erreur id="d-montant-err" message={e.montant} />
      </div>
      <fieldset className="m-0 flex flex-col gap-2.5 border-0 p-0">
        <legend className="mb-2 text-base font-bold">3. Moyen de paiement</legend>
        {moyens.map((m) => (
          <label key={m} className="flex min-h-14 cursor-pointer items-center gap-3 rounded-2xl border-[1.5px] border-[#D4C6B6] bg-white px-4 font-bold has-[:checked]:border-2 has-[:checked]:border-flamme">
            <input type="radio" name="moyen" value={m} defaultChecked={(v.moyen ?? "Wave") === m} className="h-5 w-5 accent-[#A64C0B]" /> {m}
          </label>
        ))}
        <span className="text-[13px] text-gris">Liste définitive selon le prestataire retenu.</span>
      </fieldset>
      <div className="flex flex-col gap-1.5">
        <label htmlFor="d-email" className="font-bold">E-mail pour le reçu <span className="font-medium text-gris">(facultatif)</span></label>
        <input id="d-email" name="email" type="email" autoComplete="email" defaultValue={v.email} aria-invalid={!!e.email} className={`${champ} ${e.email ? champErreur : ""}`} />
        <Erreur id="d-email-err" message={e.email} />
      </div>
      <AntiRobot />
      <button type="submit" disabled={enCours} className="min-h-14 rounded-full border-0 bg-flamme text-[15px] font-bold text-sur-flamme disabled:opacity-60">
        {enCours ? "Préparation…" : "Continuer vers le paiement sécurisé"}
      </button>
      <p className="m-0 flex items-start gap-2 text-[13px] leading-normal text-gris">
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mt-0.5 flex-none"><rect x="5" y="11" width="14" height="10" rx="2" /><path d="M8 11V8a4 4 0 0 1 8 0v3" /></svg>
        Vous payez sur la page sécurisée du prestataire. Le site ne voit jamais votre code ni votre carte.
      </p>
      <Retour etat={etat} whatsapp={whatsapp} succes="Redirection vers la page de paiement…" />
    </form>
  );
}

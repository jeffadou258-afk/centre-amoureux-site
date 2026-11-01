# Site officiel du Centre des Amoureux de Dieu — frontend Next.js

Implémentation des maquettes « Site officiel CAD — Maquettes » (31/10/2026).
Le site statique historique (dossier parent) n'est pas modifié.

## Règles tenues

- **Frontend seulement.** Aucune base, aucune table, aucun backend parallèle :
  les données passent par l'API de Hermes dès que `CAD_API_URL` est renseignée.
- **Contrats API** : `lib/api/contrats.ts` (proposition à valider par Hermes).
  Chaque réponse de l'API est validée avant affichage.
- **Pas de faux contenu.** Sans API, le site affiche le contenu réel actuel
  (`lib/contenu`, repris du site statique validé). Ce qui n'est pas fourni par
  le Centre s'affiche « à confirmer ».
- **Pas de faux succès.** Sans API, les formulaires disent qu'ils n'ont rien
  envoyé, gardent le texte saisi et proposent WhatsApp.
- **Aucun secret dans le navigateur** (vérifié sur le build : 0 occurrence).
- **Administration** : aperçu en lecture seule, en local uniquement
  (`CAD_ADMIN_APERCU=1`, jamais en production). La vraie connexion viendra
  avec Supabase Auth et l'API de Hermes.

## Commandes

```bash
npm ci
cp .env.example .env.local     # puis renseigner les valeurs
npm run dev                    # http://localhost:3000
npm run build && npm start     # production
npm run typecheck && npm run lint && npm test
```

## Vérifié le 31/10/2026

- Types, lint : sans erreur. 16 tests unitaires.
- 47 vérifications de parcours (Playwright, ordinateur 1440 px et téléphone
  390 px) : 28 pages sans erreur console, sans débordement, sans requête
  externe ; filtre et recherche ; lecteur YouTube chargé au clic seulement ;
  formulaires (validation, échec honnête sans API, texte conservé) ;
  redirections des anciennes adresses `.html` ; fichier agenda `.ics` ;
  administration fermée en production ; revalidation refusée sans secret.
- Accessibilité (axe-core, WCAG 2.2 AA) : 0 violation sur 24 pages contrôlées.
- JavaScript chargé par page : 103 à 112 Ko (compressé).

## À brancher (dépend de Hermes)

`CAD_API_URL`, `CAD_REVALIDATE_SECRET`, `NEXT_PUBLIC_TURNSTILE_SITE_KEY`,
connexion de l'administration, prestataire de paiement.

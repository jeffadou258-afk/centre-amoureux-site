# Centre des Amoureux de Dieu — site officiel

**En ligne :** https://jeffadou258-afk.github.io/centre-amoureux-site/

> Publié par **GitHub Pages** (le dépôt est public : c'est la condition du
> Pages gratuit). GitHub Pages ne permet pas d'en-têtes HTTP personnalisés :
> la CSP de `vercel.json` ne s'y applique donc pas. Sur un hébergement qui
> accepte les en-têtes (Vercel, Netlify, VPS), elle s'applique telle quelle.

Site public du **Centre des Amoureux de Dieu** (Côte d'Ivoire).
Statique, sans build, sans dépendance, sans back-end. Les formulaires ne
stockent rien : ils composent un message dans la messagerie du visiteur.

## Rubriques (cahier des charges §3)

| Rubrique CDC | Page |
|---|---|
| 3.1 Accueil | `index.html` |
| 3.2 À propos | `le-centre.html` |
| 3.3 Le Prophète | `le-prophete.html` |
| 3.4 Nos programmes | `programmes.html` |
| 3.5 Prédications / enseignements | `enseignements.html` + `predications/*.html` (8 fiches) |
| 3.6 Médiathèque | `mediatheque.html` |
| 3.7 Demande de prière | `priere.html` |
| 3.8 Témoignages | `temoignages.html` |
| 3.9 Nous rejoindre | `nous-rejoindre.html` |
| 3.10 Faire un don | `dons.html` |
| Mentions légales / données | `mentions-legales.html`, `confidentialite.html` |
| Erreur | `404.html` |

## Commandes

```bash
python3 outils/generer.py            # régénère 21 pages + sitemap + CONTENU-A-COMPLETER.md
python3 outils/serveur.py 4321       # http://127.0.0.1:4321/ (en-têtes de production)
python3 outils/verifier-contrastes.py
python3 outils/verifier-liens.py
```

## Identité et coordonnées (fournies le 31/10/2026)

| Élément | Valeur |
|---|---|
| Adresse | Cocody Rivera 2, en face de l'imprimerie DA Communication — Abidjan |
| Culte | Dimanche 14h00 – 18h30 |
| Culte de la Parole | Mercredi, une semaine sur deux, 19h00 – 21h00 |
| Téléphone / WhatsApp | +225 07 87 59 32 89 |
| Logo | flamme + colombe (détourée depuis la vidéo du Centre) → `assets/img/logo-flamme.png` |
| Logo animé | `assets/img/logo-anime.mp4` (257 Ko, muet, boucle) |
| Portraits | `assets/img/prophete-*.jpg` (filigrane retiré par recadrage) |

Vision, mission, six valeurs et onze départements viennent du document de la
direction (`Desktop/k/EMMANUEL KONAN.docx`), recopiés sans réécriture.

## Décisions du client (31/10/2026)

1. **Palette orange conservée** (`#ED6C10` / `#EF9C19` / `#ED2727`) et non le
   bleu nuit du cahier des charges. Une variante « nuit & or » reste codée et
   testée dans `assets/css/style.css` (`:root[data-theme="nuit"]`), inactive :
   elle s'active par `<html data-theme="nuit">`.
2. **Le pasteur du Centre est Daniel Jeff Adou**, et non « Issa Kourouma » cité
   par le cahier des charges (erreur du document, tranchée par le client). La
   constante `PROPHETE` du générateur porte la décision.
3. **Pas de base de données pour l'instant** : site statique. L'administration
   (ch. 4 et 5 du CDC), les paiements (3.10) et la PWA (ch. 10) viendront dans
   un lot ultérieur, avec une base dédiée — aucun lien avec une autre
   application.

## Charte

Orange `#ED6C10` · doré `#EF9C19` · rouge `#ED2727` · noir `#171717` · blanc ·
gris `#F5F5F5` / `#666666`. Mode clair, mobile d'abord.

Règle tenue : les surfaces de marque ne servent jamais de couleur de texte sur
fond clair. Texte orange = `--brand-ink #A64C0B`, texte doré = `--gold-ink
#8D5C0F`, bordure de champ = `--input-line #8A8A8A` (3,38:1, WCAG 1.4.11).

`verifier-contrastes.py` mesure **35 paires** réelles pour le thème orange et
**21** pour la variante nuit & or ; il sort en code 1 au premier écart.

## Contenu réel

- 8 prédications réelles, tirées du flux RSS officiel de la chaîne du ministère,
  avec leur vignette téléchargée localement (aucun appel à `i.ytimg.com` côté
  visiteur).
- Le lecteur YouTube ne se charge qu'au clic (`youtube-nocookie.com`).
- Ce qui n'est pas fourni par le Centre est **marqué** (fond doré pointillé) et
  listé dans `CONTENU-A-COMPLETER.md`, généré en relisant les pages.

## Déploiement

Statique. Vercel (le `vercel.json` porte la CSP), Netlify, ou tout hébergeur
de fichiers. Après déploiement : renseigner `EGLISE["site"]` (canonical, OG,
sitemap, robots) puis régénérer.

## Administration (dossier `admin/`)

Le secrétariat publie lui-même les affiches, traite les demandes de prière et
valide les témoignages. Aucune ligne de code à toucher.

```bash
python3 admin/serveur.py                     # http://127.0.0.1:4400
python3 admin/serveur.py --motdepasse '…'    # définir / changer le mot de passe
```

| Écran | Ce qu'il fait |
|---|---|
| Tableau de bord | compteurs + prochaines affiches |
| Affiches & événements | publier une veillée / convention avec affiche (JPG, PNG, WEBP — 4 Mo), supprimer |
| Demandes de prière | lire, marquer comme traitée, supprimer — jamais publiées sur le site |
| Témoignages | publier ou refuser — rien n'apparaît sans validation |

Ce qui est publié est **exporté automatiquement** vers
`assets/data/agenda.json`, `affiches.json`, `temoignages.json`, lus par le site
statique. Le site reste donc déployable sur n'importe quel hébergeur ; seul ce
serveur doit tourner de façon persistante.

### Brancher les formulaires du site

Dans `assets/js/config.js` :

```js
window.CAD_API = "https://admin.centre-des-amoureux.org";
```

Les formulaires de prière et de témoignage envoient alors réellement
(`POST /api/priere`, `/api/temoignage`) et la demande arrive dans
l'administration. Si `CAD_API` reste vide, ils composent un message dans la
messagerie du visiteur — jamais de faux succès.

### Sécurité en place

Mot de passe haché PBKDF2 (240 000 itérations) · session signée HMAC, cookie
`HttpOnly` + `SameSite=Strict`, 12 h · jeton CSRF sur chaque écriture ·
validation binaire des images, 4 Mo max, nom aléatoire, écriture bornée au
dossier `assets/img/affiches` · aucune écriture hors des dossiers prévus ·
CSP `script-src 'none'` sur les pages d'administration · quota de 30 envois
par heure et par IP sur l'API publique.

⚠️ **Le serveur d'administration écoute sur `127.0.0.1`** : il n'est pas
exposé à Internet en l'état. Pour le mettre en ligne, il faut un hébergement
(VPS/ Render / Fly) derrière HTTPS, et changer le mot de passe provisoire.

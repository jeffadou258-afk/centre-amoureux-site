# Centre des Amoureux de Dieu — site officiel

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

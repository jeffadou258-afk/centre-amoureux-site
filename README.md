# Centre des Amoureux de Dieu — site vitrine

Site public du **Centre des Amoureux de Dieu** (Côte d'Ivoire).
**Indépendant de toute autre application** : aucun lien, aucune donnée partagée,
aucun back-end. Fichiers statiques uniquement.

## Structure

```
centre-amoureux-site/
├── index.html                 Accueil
├── le-centre.html             Qui nous sommes, vision, pasteur
├── cultes.html                Horaires, lieu, déroulement, première visite
├── enseignements.html         Vidéos de la chaîne du ministère
├── evenements.html            Rendez-vous et temps forts
├── priere.html                Demande de prière
├── contact.html               Coordonnées et message
├── dons.html                  Moyens de soutenir l'œuvre
├── mentions-legales.html      Éditeur, données personnelles, hébergeur
├── 404.html                   Page introuvable
├── robots.txt · sitemap.xml
├── vercel.json                En-têtes de sécurité (CSP) + cache
├── CONTENU-A-COMPLETER.md     Généré : tout ce qui reste à fournir
├── assets/
│   ├── css/style.css          Charte orange, une seule feuille
│   ├── js/site.js             Menu, lecteur paresseux, formulaires
│   └── img/favicon.svg · img/partage.png (1200×630)
└── outils/
    ├── generer.py             Génère les 10 pages depuis une source unique
    ├── serveur.py             Prévisualisation avec les en-têtes de production
    ├── verifier-contrastes.py Contrôle WCAG mesuré (échec = code 1)
    ├── verifier-liens.py      Liens, ancres, balises (échec = code 1)
    └── partage.html           Source de l'image de partage
```

## Commandes

```bash
python3 outils/generer.py            # régénère les 10 pages + sitemap + CONTENU-A-COMPLETER.md
python3 outils/serveur.py 4321       # http://127.0.0.1:4321/
python3 outils/verifier-contrastes.py
python3 outils/verifier-liens.py
```

Aucune dépendance : Python 3 et un navigateur suffisent. Pas de `npm install`,
pas de build.

## Modifier les informations de l'église

Tout part de `EGLISE` et `CRENEAUX` dans `outils/generer.py`, puis :

```bash
python3 outils/generer.py
```

Ce qui n'est pas encore fourni porte un marqueur visuel (fond doré pointillé)
et est listé dans `CONTENU-A-COMPLETER.md`. Quand il n'en reste aucun, retirer
`data-etat="travail"` de la balise `<html>` dans `page_html()` pour masquer le
bandeau de travail.

## Charte

Orange `#ED6C10` · doré `#EF9C19` · rouge `#ED2727` · noir `#171717` · blanc ·
gris `#F5F5F5` / `#666666`. Mode clair. Mobile d'abord.

Règle de contraste tenue : les surfaces de marque (`--brand`, `--gold`, `--red`)
ne servent **jamais** de couleur de texte sur fond clair — le texte orange
utilise `--brand-ink` (`#A64C0B`), le texte doré `--gold-ink` (`#8D5C0F`).
`python3 outils/verifier-contrastes.py` mesure 33 paires réelles et sort en
code 1 au premier écart.

## Ce que le site ne fait pas (par choix)

- Aucun cookie, aucun traceur, aucune mesure d'audience.
- Aucun formulaire ne stocke de données : ils composent un message dans la
  messagerie du visiteur (`mailto:`), et le disent à l'écran.
- Aucun paiement en ligne : la page « dons » affiche des moyens de don à
  confirmer, elle n'encaisse rien.
- Les vidéos YouTube ne se chargent qu'après un clic explicite
  (`youtube-nocookie.com`, aucune requête avant le clic).

## Déployer

Le site est purement statique. Au choix :

- **Vercel** : importer le dépôt ; `vercel.json` porte déjà la CSP et le cache.
- **Netlify** : publier la racine, sans commande de build.
- **GitHub Pages** : publier la branche `main` à la racine (le dépôt doit être
  public pour un hébergement gratuit).

Après déploiement : renseigner le domaine réel dans `EGLISE["site"]`
(canonical, Open Graph, sitemap, `robots.txt`) puis régénérer.

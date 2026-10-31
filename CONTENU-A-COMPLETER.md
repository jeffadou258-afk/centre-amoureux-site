# Contenu à fournir par le Centre des Amoureux de Dieu

Ce fichier est **généré automatiquement** par `outils/generer.py` à partir des
pages réellement produites. Il liste chaque information encore marquée
« à confirmer » sur le site (fond doré pointillé).

Total : **54 marqueurs** sur le site.

## 1. Informations d'identité

| Champ | Valeur actuelle | À fournir |
|---|---|---|
| Ville | à confirmer | ville du siège |
| Quartier | à confirmer | quartier / commune |
| Adresse | à confirmer | adresse complète + point de repère |
| Téléphone | à confirmer | numéro du secrétariat |
| WhatsApp | à confirmer | numéro WhatsApp |
| E-mail | contact@centre-des-amoureux.org | adresse e-mail réelle |
| Année de fondation | à confirmer | année |
| Facebook / TikTok | à confirmer | URL des pages officielles |
| Domaine | centre-des-amoureux.org | domaine réellement acheté |
| Logo | aucun fichier fourni | fichier PNG ou SVG (le monogramme actuel est un rendu CSS) |
| Photo du pasteur | aucune fournie | portrait officiel |
| Numéro Mobile Money | à confirmer | numéro marchand |
| Coordonnées bancaires | à confirmer | IBAN / compte |
| Hébergeur | à renseigner | nom et adresse de l'hébergeur (mentions légales) |
| Identification légale | à compléter | numéro d'enregistrement / statut |

## 2. Horaires des cultes

| Rendez-vous | Horaire |
|---|---|
| Culte d'adoration (dimanche) | à confirmer |
| Culte de la Parole (mercredi) | à confirmer |
| Nuit de prière (vendredi) | à confirmer |

## 3. Où chaque marqueur apparaît

### `index.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `le-centre.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `cultes.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `enseignements.html`

- à confirmer
- à confirmer
- à confirmer

### `evenements.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `priere.html`

- à confirmer
- à confirmer
- à confirmer

### `contact.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `dons.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `mentions-legales.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

## 4. Comment remplacer

1. Ouvrir `outils/generer.py` et renseigner le dictionnaire `EGLISE`
   (et la liste `CRENEAUX` pour les horaires).
2. Lancer `python3 outils/generer.py`.
3. Les 10 pages et ce fichier sont régénérés. Quand plus aucun marqueur ne
   subsiste, retirer l'attribut `data-etat="travail"` de la balise `<html>`
   (dans la fonction `page_html`) pour masquer le bandeau de travail.

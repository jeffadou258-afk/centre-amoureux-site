# Contenu à fournir par le Centre des Amoureux de Dieu

Fichier **généré** par `outils/generer.py` en relisant les pages réellement
produites. Il liste chaque information encore marquée « à confirmer » (fond
doré pointillé sur le site).

Total : **13 marqueurs** sur le site.

## 1. Identité et contacts

| Champ | À fournir |
|---|---|
| Ville / quartier / adresse complète | adresse officielle + point de repère |
| Téléphone / WhatsApp | numéros du secrétariat |
| E-mail | adresse réelle (actuellement `contact@centre-des-amoureux.org`, provisoire) |
| Année de fondation, histoire du Centre | texte validé par la direction |
| Responsables (pasteurs, anciens, départements) | liste et rôles |
| Logo, photos officielles, portrait du Prophète | fichiers haute définition |
| Facebook / Instagram / TikTok | URL des pages officielles |
| Domaine, hébergeur, identification légale | informations administratives |
| Mobile Money / coordonnées bancaires | compte marchand agréé |

## 2. Horaires

| Rendez-vous | Horaire |
|---|---|
| Culte d'adoration (dimanche) | à confirmer |
| Culte de la Parole (mercredi) | à confirmer |
| Nuit de prière (vendredi) | à confirmer |

## 3. Où chaque marqueur apparaît

### `dons.html`

- à confirmer
- à confirmer

### `le-centre.html`

- à confirmer
- à confirmer
- à confirmer
- à confirmer
- à confirmer

### `nous-rejoindre.html`

- page à confirmer
- compte à confirmer
- compte à confirmer

### `programmes.html`

- à confirmer
- à confirmer
- à confirmer

## 4. Après réception

1. Renseigner `EGLISE` et `CRENEAUX` dans `outils/generer.py`.
2. Lancer `python3 outils/generer.py`.
3. Quand plus aucun marqueur ne subsiste, retirer `data-etat="travail"` de la
   balise `<html>` dans le gabarit `T_PAGE` pour masquer le bandeau de travail.

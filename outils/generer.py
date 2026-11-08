#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du site du CENTRE DES AMOUREUX DE DIEU.

Site statique : chaque page est produite ici à partir d'une seule source de
vérité (EGLISE, CRENEAUX, VIDEOS, EVENEMENTS, PROPHETE). Ne pas modifier les
fichiers .html à la main : modifier ce fichier puis relancer.

Les gabarits utilisent string.Template (`$jeton`) : un « $ » littéral s'écrit
« $$ ».

Usage :
    python3 outils/generer.py
"""

import json
import os
import re
from string import Template

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════════════════
# 1. DONNÉES — la seule source de vérité du site
# ══════════════════════════════════════════════════════════════════════

EGLISE = {
    "nom": "Centre des Amoureux de Dieu",
    "sigle": "CAD",
    "pays": "Côte d'Ivoire",
    "ville": "Abidjan",
    "quartier": "Cocody Riviera 2",
    "adresse": "Cocody Riviera 2, en face de l'imprimerie DA Communication",
    "acces": ("Du rond-point de la Riviera 2, prenez la direction de la station-service "
              "Petroleum, tournez à gauche puis faites 100 m : nous sommes en face de "
              "l'imprimerie DA Communication."),
    "telephone": "+225 07 87 59 32 89",
    "whatsapp": "2250787593289",
    "youtube": "https://www.youtube.com/@jeffadou3161",
    "facebook": "https://www.facebook.com/profile.php?id=61554023926797",
    "tiktok": "https://www.tiktok.com/@centre.des.amoure",
    "fondation": "octobre 2023",
    "maps": "https://www.google.com/maps/search/?api=1&amp;query=Cocody+Riviera+2+imprimerie+DA+Communication+Abidjan",
    # Adresse de publication (canonical, partage, sitemap).
    "site": "https://jeffadou258-afk.github.io/centre-amoureux-site",
}

# Décision du client (31/10/2026) : le pasteur du Centre est Daniel Jeff Adou.
PROPHETE = {
    "nom": "Prophète Daniel Jeff Adou",
    "nom_court": "Daniel Jeff Adou",
    "role": "Fondateur et pasteur du Centre des Amoureux de Dieu",
    "facebook": "https://www.facebook.com/DanielJeffProphete",
}

# Horaires communiqués par le Centre (31/10/2026).
CRENEAUX = [
    ("Dimanche", "Culte d'adoration", "14h00 – 18h30"),
    ("Mercredi", "Culte de la Parole, une semaine sur deux", "19h00 – 21h00"),
]

VISION = ("Former des ouvriers et des serviteurs de Dieu, bâtir une armée "
          "d'amoureux passionnés pour Dieu et les équiper pour impacter la société.")

MISSION = ("Par la prédication de la Parole, l'évangélisation, la formation biblique "
           "et le développement de leaders, nous équipons nos membres pour qu'ils "
           "deviennent des serviteurs fidèles capables de transformer leur famille, "
           "leur communauté et impacter positivement la société.")

VALEURS = [
    ("Amour", "Servir et agir avec compassion envers Dieu et envers les autres.", "Jean 13 : 34-35"),
    ("Foi", "Croire en Dieu et en Sa Parole dans toutes les situations, et vivre selon cette confiance.", "Hébreux 11 : 1"),
    ("Intégrité", "Être honnête, transparent et fidèle dans toutes nos actions.", "Proverbes 10 : 9"),
    ("Crainte de Dieu", "Respecter et honorer Dieu dans nos pensées, paroles et actions.", "Proverbes 9 : 10"),
    ("Obéissance à la Parole", "Mettre en pratique les enseignements bibliques dans notre vie quotidienne.", "Jacques 1 : 22"),
    ("Excellence", "Poursuivre la qualité et la diligence dans tout ce que nous faisons pour glorifier Dieu.", "Colossiens 3 : 23"),
]

# Vidéos de la chaîne officielle, de la plus récente à la plus ancienne.
VIDEOS = [
    {"id": "EKI8TVqpyzs", "titre": "Remporter les batailles par la prière",
     "iso": "2026-11-01", "date": "1er novembre 2026", "genre": "Culte",
     "slug": "remporter-les-batailles-par-la-priere"},
    {"id": "Vke4iYzemIs", "titre": "Tous les grands ont d'abord rêvé grand",
     "iso": "2026-10-17", "date": "17 octobre 2026", "genre": "Exhortation",
     "slug": "tous-les-grands-ont-reve-grand"},
    {"id": "SXql767Lo7w", "titre": "10 choses à savoir sur l'onction royale (partie 2)",
     "iso": "2026-10-16", "date": "16 octobre 2026", "genre": "Enseignement",
     "slug": "onction-royale-10-choses-a-savoir"},
    {"id": "jrefqSertlc", "titre": "10 choses à savoir sur l'onction royale (partie 1)",
     "iso": "2026-10-12", "date": "12 octobre 2026", "genre": "Enseignement",
     "slug": "onction-royale-10-choses"},
    {"id": "2CHnQLRtN0Y", "titre": "L'huile, le cœur et le trône",
     "iso": "2026-09-28", "date": "28 septembre 2026", "genre": "Enseignement",
     "slug": "huile-coeur-et-trone"},
    {"id": "-hKzzUDnh0E", "titre": "Prions ensemble",
     "iso": "2026-09-24", "date": "24 septembre 2026", "genre": "Prière",
     "slug": "prions-ensemble"},
    {"id": "OlT6R0wc0JQ", "titre": "L'huile, le cœur et le trône (partie 1)",
     "iso": "2026-09-22", "date": "22 septembre 2026", "genre": "Enseignement",
     "slug": "huile-coeur-et-trone-partie-1"},
    {"id": "_fldckxVCDI", "titre": "Comment reconnaître un sorcier",
     "iso": "2026-08-12", "date": "12 août 2026", "genre": "Enseignement",
     "slug": "reconnaitre-un-sorcier"},
    {"id": "h8dCZFevdI8", "titre": "Service prophétique",
     "iso": "2026-08-12", "date": "12 août 2026", "genre": "Culte",
     "slug": "service-prohetique"},
]

GENRES = []
for _v in VIDEOS:
    if _v["genre"] not in GENRES:
        GENRES.append(_v["genre"])

# Événements à l'affiche. « fin » (AAAA-MM-JJ) : le lendemain, la carte
# disparaît toute seule du site (assets/js/site.js).
EVENEMENTS = [
    {
        "titre": "14 jours de jeûnes et prières",
        "theme": "Expérimenter la gloire de Dieu",
        "quand": "Du lundi 9 au dimanche 22 novembre 2026",
        "detail": ("Prière du matin de 5h00 à 5h30 sur WhatsApp, prière du soir dès "
                   "20h45 sur Google Meet, et les mercredis 11 et 18 à l'église."),
        "affiche": "assets/img/affiches/jeune-14-jours-2026.jpg",
        "lien": "jeune.html",
        "action": "M'inscrire au jeûne",
        "fin": "2026-11-22",
    },
    {
        "titre": "Grande nuit de prophéties et de délivrances",
        "theme": "J'ai ouvert devant toi une porte que nul ne peut fermer",
        "quand": "Vendredi 20 novembre 2026, dès 21h00",
        "detail": ("Avec le Prophète Abraham Aké, leader du MIFE, et le Prophète "
                   "Jeff Adou. Au Centre, à Cocody Riviera 2."),
        "affiche": "assets/img/affiches/nuit-propheties-2026.jpg",
        "lien": "nous-rejoindre.html",
        "action": "Voir l'itinéraire",
        "fin": "2026-11-20",
    },
]

# Photos tirées des captations de cultes (dossier assets/img/culte).
PHOTOS_CULTE = [
    ("culte-scene", "Le Prophète Daniel Jeff Adou au pupitre, pendant le culte"),
    ("culte-predication", "Prédication du dimanche au Centre des Amoureux de Dieu"),
    ("culte-proche", "Le Prophète prêche, micro en main"),
    ("culte-assemblee", "Le Prophète s'adresse à l'assemblée"),
    ("culte-salle", "La salle du Centre et l'estrade, avant le culte"),
    ("culte-large", "L'estrade du Centre des Amoureux de Dieu"),
]

NAV = [
    ("index.html", "Accueil"),
    ("le-centre.html", "Le Centre"),
    ("le-prophete.html", "Le Prophète"),
    ("programmes.html", "Programmes"),
    ("enseignements.html", "Prédications"),
    ("mediatheque.html", "Médiathèque"),
    ("priere.html", "Prière"),
    ("nous-rejoindre.html", "Nous rejoindre"),
]

# ══════════════════════════════════════════════════════════════════════
# 2. COMPOSANTS
# ══════════════════════════════════════════════════════════════════════


def attr(texte):
    return texte.replace('"', "&quot;")


def vignette(v):
    return "assets/img/videos/%s.jpg" % v["id"]


def lien_fiche(v, prefixe=""):
    return "%spredications/%s.html" % (prefixe, v["slug"])


T_VIDEO = Template("""            <article class="video" data-genre="$genre" data-titre="$titre_attr">
              <button class="lecteur" type="button" data-video="$id" data-titre="$titre_attr"
                      aria-label="Lire la vidéo : $titre_attr">
                <img src="$prefixe$vignette" alt="" width="1280" height="720" loading="lazy">
                <span class="lecteur__bouton" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
              </button>
              <p class="video__meta">$genre, $date</p>
              <h3 class="video__titre"><a href="$lien">$titre</a></h3>
            </article>""")


def carte_video(v, prefixe=""):
    return T_VIDEO.substitute(
        id=v["id"], titre=v["titre"], titre_attr=attr(v["titre"]), date=v["date"],
        genre=v["genre"], lien=lien_fiche(v, prefixe), vignette=vignette(v), prefixe=prefixe,
    )


def lignes_horaires():
    return "\n".join(
        """              <div class="horaire">
                <span class="horaire__jour">%s</span>
                <span class="horaire__nom">%s</span>
                <span class="horaire__heure">%s</span>
              </div>""" % c
        for c in CRENEAUX
    )


T_EVENEMENT = Template("""          <article class="evenement" data-fin="$fin">
            <a class="evenement__affiche" href="$lien"><img src="$prefixe$affiche" alt="Affiche : $titre_attr" width="900" height="1114" loading="lazy"></a>
            <div class="evenement__texte">
              <p class="evenement__quand">$quand</p>
              <h3>$titre</h3>
              <p class="evenement__theme">« $theme »</p>
              <p>$detail</p>
              <a class="btn btn--feu" href="$prefixe$lien">$action</a>
            </div>
          </article>""")


def evenements(prefixe=""):
    return "\n".join(
        T_EVENEMENT.substitute(prefixe=prefixe, titre_attr=attr(e["titre"]), **e) for e in EVENEMENTS
    )


T_ENTETE = Template("""      <section class="entete$classe" style="background-image:url('$prefixe$photo')">
        <div class="wrap">
          <nav class="fil" aria-label="Fil d'Ariane"><a href="${prefixe}index.html">Accueil</a> <span aria-hidden="true">/</span> $libelle</nav>
          <h1>$titre</h1>
          <p class="entete__intro">$intro</p>
        </div>
      </section>""")


def entete(libelle, titre, intro, photo="assets/img/culte/culte-salle.jpg", prefixe="", classe=""):
    return T_ENTETE.substitute(libelle=libelle, titre=titre, intro=intro, photo=photo,
                               prefixe=prefixe, classe=(" " + classe) if classe else "")


T_APPEL = Template("""      <section class="appel" style="background-image:url('${prefixe}assets/img/culte/culte-large.jpg')">
        <div class="wrap appel__grille">
          <div>
            <h2>Venez tel que vous êtes.</h2>
            <p>Que ce soit votre première fois ou que vous cherchiez une maison spirituelle,
            il y a une place pour vous dimanche.</p>
          </div>
          <div class="appel__infos">
$horaires
            <p class="appel__adresse">$adresse</p>
            <div class="actions">
              <a class="btn btn--feu" href="${prefixe}nous-rejoindre.html">Préparer ma visite</a>
              <a class="btn btn--contour" href="$maps" target="_blank" rel="noopener">Itinéraire</a>
            </div>
          </div>
        </div>
      </section>""")


def appel(prefixe=""):
    return T_APPEL.substitute(prefixe=prefixe, horaires=lignes_horaires(),
                              adresse=EGLISE["adresse"], maps=EGLISE["maps"])


def bouton_whatsapp(texte, libelle, classe="btn btn--feu"):
    from urllib.parse import quote
    return '<a class="%s" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s</a>' % (
        classe, EGLISE["whatsapp"], quote(texte), libelle)


# ── Gabarit de page ───────────────────────────────────────────────────

T_PAGE = Template("""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>$titre_complet</title>
    <meta name="description" content="$description">
    <meta name="robots" content="$robots">
    <meta name="theme-color" content="#1B0F0A">
    <link rel="canonical" href="$canonical">
    <link rel="icon" href="${prefixe}assets/img/icone-512.png" type="image/png">
    <link rel="apple-touch-icon" href="${prefixe}assets/img/icone-512.png">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="$nom">
    <meta property="og:locale" content="fr_FR">
    <meta property="og:title" content="$og_titre">
    <meta property="og:description" content="$description">
    <meta property="og:url" content="$canonical">
    <meta property="og:image" content="$site/assets/img/partage.png">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="preload" href="${prefixe}assets/fonts/anton.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="${prefixe}assets/css/style.css">
    <script type="application/ld+json">
$jsonld
    </script>
  </head>
  <body class="$classe_corps">
    <a class="skip" href="#contenu">Aller au contenu</a>

    <header class="site-header">
      <div class="wrap site-header__in">
        <a class="marque" href="${prefixe}index.html" aria-label="$nom, accueil">
          <img src="${prefixe}assets/img/logo-flamme.png" alt="" width="26" height="46">
          <span>Centre des<br>Amoureux de Dieu</span>
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-principal">
          <span class="nav-toggle__barre" aria-hidden="true"></span>
          <span class="sr-only">Menu</span>
        </button>
        <nav class="nav" id="nav-principal" data-ouvert="false" aria-label="Navigation principale">
$navigation
        </nav>
      </div>
    </header>

$corps

    <footer class="site-footer">
      <div class="wrap">
        <div class="site-footer__haut">
          <p class="site-footer__devise">Une maison de prière, de Parole et d'amour fraternel.</p>
          <div class="reseaux">
            <a href="$youtube" target="_blank" rel="noopener">YouTube</a>
            <a href="$facebook" target="_blank" rel="noopener">Facebook</a>
            <a href="$tiktok" target="_blank" rel="noopener">TikTok</a>
            <a href="https://wa.me/$whatsapp" target="_blank" rel="noopener">WhatsApp</a>
          </div>
        </div>
        <div class="site-footer__grille">
          <div>
            <h2>Nous trouver</h2>
            <p>$adresse<br>$ville, $pays</p>
            <p><a href="tel:+$whatsapp">$telephone</a></p>
          </div>
          <div>
            <h2>Cultes</h2>
            <p>Dimanche, 14h00 – 18h30<br>Mercredi (une semaine sur deux), 19h00 – 21h00</p>
          </div>
          <div>
            <h2>Le Centre</h2>
            <ul>
              <li><a href="${prefixe}le-centre.html">Qui nous sommes</a></li>
              <li><a href="${prefixe}le-prophete.html">Le Prophète</a></li>
              <li><a href="${prefixe}programmes.html">Programmes</a></li>
              <li><a href="${prefixe}temoignages.html">Témoignages</a></li>
            </ul>
          </div>
          <div>
            <h2>Agir</h2>
            <ul>
              <li><a href="${prefixe}priere.html">Demander une prière</a></li>
              <li><a href="${prefixe}enseignements.html">Écouter une prédication</a></li>
              <li><a href="${prefixe}dons.html">Faire un don</a></li>
              <li><a href="${prefixe}nous-rejoindre.html">Nous écrire</a></li>
            </ul>
          </div>
        </div>
        <div class="site-footer__bas">
          <p>© <span data-annee>2026</span> $nom</p>
          <p><a href="${prefixe}mentions-legales.html">Mentions légales</a> <a href="${prefixe}confidentialite.html">Confidentialité</a></p>
        </div>
      </div>
    </footer>

    <script src="${prefixe}assets/js/config.js" defer></script>
    <script src="${prefixe}assets/js/site.js" defer></script>
    <script src="${prefixe}assets/js/donnees.js" defer></script>
  </body>
</html>
""")


def navigation(page, prefixe=""):
    liens = []
    for href, libelle in NAV:
        actif = ' aria-current="page"' if href == page else ""
        liens.append('          <a href="%s%s"%s>%s</a>' % (prefixe, href, actif, libelle))
    liens.append('          <a class="btn btn--feu nav__don" href="%sdons.html">Faire un don</a>' % prefixe)
    return "\n".join(liens)


def page_html(page, titre, description, corps, index=True, jsonld=None, prefixe="", classe_corps=""):
    nom_complet = (EGLISE["nom"] + " · Abidjan") if page == "index.html" else "%s · %s" % (titre, EGLISE["nom"])
    if jsonld is None:
        jsonld = {
            "@context": "https://schema.org",
            "@type": "Church",
            "name": EGLISE["nom"],
            "url": EGLISE["site"],
            "address": {"@type": "PostalAddress", "streetAddress": EGLISE["adresse"],
                        "addressLocality": EGLISE["ville"], "addressCountry": "CI"},
            "telephone": EGLISE["telephone"],
            "sameAs": [EGLISE["youtube"], EGLISE["facebook"], EGLISE["tiktok"]],
        }
    return T_PAGE.substitute(
        titre_complet=nom_complet, description=description,
        robots="index,follow" if index else "noindex,follow",
        canonical=EGLISE["site"] + "/" + ("" if page == "index.html" else page),
        og_titre=titre, site=EGLISE["site"], nom=EGLISE["nom"], pays=EGLISE["pays"],
        youtube=EGLISE["youtube"], facebook=EGLISE["facebook"], tiktok=EGLISE["tiktok"],
        whatsapp=EGLISE["whatsapp"], ville=EGLISE["ville"], adresse=EGLISE["adresse"],
        telephone=EGLISE["telephone"], navigation=navigation(page, prefixe),
        jsonld=json.dumps(jsonld, ensure_ascii=False, indent=2), corps=corps,
        prefixe=prefixe, classe_corps=classe_corps,
    )


# ══════════════════════════════════════════════════════════════════════
# 3. PAGES
# ══════════════════════════════════════════════════════════════════════

CORPS_ACCUEIL = Template("""    <main id="contenu">
      <section class="hero">
        <img class="hero__photo" src="assets/img/culte/culte-salle.jpg" alt="" width="1280" height="658" fetchpriority="high">
        <div class="wrap hero__contenu">
          <p class="hero__lieu">Église à Cocody Riviera 2, Abidjan</p>
          <h1 class="hero__titre"><span>Un lieu pour</span> <span>aimer Dieu</span> <span>et être aimé de Lui.</span></h1>
          <p class="hero__texte">Une famille spirituelle où la Parole est enseignée avec clarté,
          où la prière est une respiration, et où chacun est accueilli avec dignité.</p>
          <div class="actions">
            <a class="btn btn--feu" href="nous-rejoindre.html">Venir dimanche</a>
            <a class="btn btn--contour" href="#predications">Écouter une prédication</a>
          </div>
        </div>
        <div class="hero__bas">
          <div class="wrap hero__bas-in">
            <p class="compte" data-compte>Culte chaque dimanche, de 14h00 à 18h30</p>
            <p class="hero__adresse">$adresse · <a href="$maps" target="_blank" rel="noopener">Itinéraire</a></p>
          </div>
        </div>
      </section>

      <section class="section section--nuit" id="a-l-affiche">
        <div class="wrap">
          <div class="tete">
            <h2>À l'affiche ce mois-ci</h2>
            <p>Notre thème de novembre : <strong>remporter les batailles par la prière</strong>.</p>
          </div>
          <div class="evenements">
$evenements
          </div>
        </div>
      </section>

      <section class="section" id="predications">
        <div class="wrap">
          <div class="tete tete--ligne">
            <h2>Dernières prédications</h2>
            <a class="lien" href="enseignements.html">Toutes les prédications</a>
          </div>
          <div class="une">
            <div class="une__principale">
$premiere
            </div>
            <div class="une__suite">
$suivantes
            </div>
          </div>
        </div>
      </section>

      <section class="prophete-bloc">
        <div class="prophete-bloc__photo">
          <img src="assets/img/prophete-bras-croises.jpg" alt="Le Prophète Daniel Jeff Adou" width="720" height="960" loading="lazy">
        </div>
        <div class="prophete-bloc__texte">
          <blockquote>
            <p>Une prophétie que tu reçois est une invitation à la prière.</p>
          </blockquote>
          <p class="prophete-bloc__nom">Prophète Daniel Jeff Adou</p>
          <p>Fondateur et pasteur du Centre des Amoureux de Dieu depuis octobre 2023.
          Son enseignement insiste sur l'amour de Dieu, la vie de prière et le combat
          spirituel ; il est l'auteur de <em>Sortir des prisons familiales</em>.</p>
          <a class="lien" href="le-prophete.html">Découvrir son ministère</a>
        </div>
      </section>

      <section class="section">
        <div class="wrap trio">
          <div>
            <h2>Qui nous sommes</h2>
            <p>« Amoureux de Dieu » n'est pas un titre que l'on se donne : c'est une direction
            de vie. Notre vision : former des ouvriers, bâtir une armée d'amoureux passionnés
            pour Dieu et les équiper pour impacter la société.</p>
            <a class="lien" href="le-centre.html">Notre vision et nos valeurs</a>
          </div>
          <div>
            <h2>Un fardeau à déposer ?</h2>
            <p>Santé, famille, travail, mariage, finances : écrivez-nous. L'équipe pastorale
            prie pour chaque demande, en toute confidentialité.</p>
            <a class="lien" href="priere.html">Demander une prière</a>
          </div>
          <div>
            <h2>Dieu a agi ?</h2>
            <p>Guérison, délivrance, restauration : votre témoignage peut fortifier la foi
            d'un autre. Racontez-nous ce que vous avez vécu.</p>
            <a class="lien" href="temoignages.html">Partager un témoignage</a>
          </div>
        </div>
      </section>

$appel
    </main>
""")


def corps_accueil():
    return CORPS_ACCUEIL.substitute(
        adresse=EGLISE["adresse"], maps=EGLISE["maps"], evenements=evenements(),
        premiere=carte_video(VIDEOS[0]),
        suivantes="\n".join(carte_video(v) for v in VIDEOS[1:4]),
        appel=appel(),
    )


CORPS_CENTRE = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes">
          <div>
            <h2>Notre vision</h2>
            <p class="grand">$vision</p>
          </div>
          <div>
            <h2>Notre mission</h2>
            <p>$mission</p>
            <ul class="liste">
              <li>Prédication et enseignement biblique</li>
              <li>Évangélisation et formation continue</li>
              <li>Développement de leaders passionnés</li>
              <li>Implication dans la transformation de la société</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="verset">
        <div class="wrap">
          <p>« Le plus petit deviendra un millier, et le moindre une nation puissante. »</p>
          <cite>Ésaïe 60 : 22</cite>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="tete">
            <h2>Nos valeurs</h2>
            <p>Six principes, chacun enraciné dans l'Écriture, qui guident nos décisions.</p>
          </div>
          <dl class="valeurs">
$valeurs
          </dl>
        </div>
      </section>

      <section class="section section--nuit">
        <div class="wrap colonnes colonnes--centre">
          <div>
            <h2>Notre histoire</h2>
            <p>Le Centre des Amoureux de Dieu est né en octobre 2023 à Abidjan, à Cocody
            Riviera 2. Depuis, la communauté se rassemble chaque dimanche, et un mercredi sur
            deux, autour de la Parole, de la prière et du service. En 2026, l'église a fêté
            ses trois ans.</p>
            <a class="btn btn--feu" href="le-prophete.html">Le Prophète Daniel Jeff Adou</a>
          </div>
          <img class="photo-arrondie" src="assets/img/culte/culte-salle.jpg" alt="La salle et l'estrade du Centre des Amoureux de Dieu" width="1280" height="658" loading="lazy">
        </div>
      </section>

$appel
    </main>
""")


def corps_centre():
    valeurs = "\n".join(
        """            <div>
              <dt>%s</dt>
              <dd>%s <span class="ref">%s</span></dd>
            </div>""" % v for v in VALEURS
    )
    return CORPS_CENTRE.substitute(
        entete=entete("Le Centre", "Une église, une famille, une armée d'amoureux.",
                      "Une communauté chrétienne établie à Abidjan depuis octobre 2023, "
                      "pour former des ouvriers et équiper chacun à impacter la société.",
                      "assets/img/culte/culte-large.jpg"),
        vision=VISION, mission=MISSION, valeurs=valeurs, appel=appel(),
    )


CORPS_PROPHETE = Template("""    <main id="contenu">
      <section class="entete entete--prophete">
        <div class="wrap entete--prophete__grille">
          <div>
            <nav class="fil" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <span aria-hidden="true">/</span> Le Prophète</nav>
            <h1>Prophète Daniel Jeff Adou</h1>
            <p class="entete__intro">Fondateur et pasteur du Centre des Amoureux de Dieu, à Abidjan.</p>
            <div class="actions">
              <a class="btn btn--feu" href="$youtube" target="_blank" rel="noopener">Sa chaîne YouTube</a>
              <a class="btn btn--contour" href="$facebook" target="_blank" rel="noopener">Sa page Facebook</a>
            </div>
          </div>
          <img src="assets/img/prophete-portrait.jpg" alt="Portrait du Prophète Daniel Jeff Adou" width="852" height="1150">
        </div>
      </section>

      <section class="section">
        <div class="wrap colonnes">
          <div>
            <h2>Son ministère</h2>
            <p class="grand">Le Prophète Daniel Jeff Adou a fondé le Centre des Amoureux de Dieu
            en octobre 2023, avec une conviction : la Parole de Dieu éclaire la vie réelle,
            ici et maintenant.</p>
          </div>
          <div>
            <p>Son enseignement s'articule autour de trois axes que l'on retrouve dans
            chacun de ses messages :</p>
            <ul class="liste">
              <li><strong>L'amour de Dieu</strong> : comprendre qu'on est aimé avant d'être méritant.</li>
              <li><strong>La vie de prière</strong> : prier avec constance, en toute saison.</li>
              <li><strong>Le combat spirituel</strong> : discerner l'origine des combats et les remporter par la prière.</li>
            </ul>
            <p>Ses prédications sont diffusées chaque semaine sur la chaîne YouTube du ministère.</p>
          </div>
        </div>
      </section>

      <section class="section section--nuit">
        <div class="wrap livre">
          <img src="assets/img/livre-sortir-des-prisons.jpg" alt="Couverture du livre Sortir des prisons familiales" width="640" height="907" loading="lazy">
          <div>
            <p class="livre__auteur">Le livre du Prophète</p>
            <h2>Sortir des prisons familiales</h2>
            <p class="grand">100 prières pour briser les chaînes, renverser les limitations
            et restaurer ta destinée.</p>
            <p>Prisons spirituelles, familiales, ancestrales, prisons du nom et du territoire :
            ce livre explique comment elles se forment, pourquoi elles se transmettent et
            comment en sortir, avant de conduire le lecteur dans cent prières ciblées.</p>
            <p class="petit">Le Biographe Édition, Abidjan, 2025.</p>
            $commander
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="tete tete--ligne">
            <h2>Ses derniers messages</h2>
            <a class="lien" href="enseignements.html">Toutes les prédications</a>
          </div>
          <div class="grille-videos">
$videos
          </div>
        </div>
      </section>

      <section class="galerie-bande" aria-label="Photos">
        <img src="assets/img/prophete-face.jpg" alt="Le Prophète Daniel Jeff Adou, portrait" width="720" height="960" loading="lazy">
        <img src="assets/img/culte/culte-proche.jpg" alt="Le Prophète prêche pendant le culte" width="1280" height="658" loading="lazy">
        <img src="assets/img/culte/culte-assemblee.jpg" alt="Le Prophète s'adresse à l'assemblée" width="1280" height="658" loading="lazy">
      </section>

$appel
    </main>
""")


def corps_prophete():
    return CORPS_PROPHETE.substitute(
        youtube=EGLISE["youtube"], facebook=PROPHETE["facebook"],
        videos="\n".join(carte_video(v) for v in VIDEOS[:3]),
        commander=bouton_whatsapp("Bonjour, je souhaite me procurer le livre « Sortir des prisons familiales » du Prophète Jeff Adou.",
                                  "Se procurer le livre"),
        appel=appel(),
    )


CORPS_PROGRAMMES = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes">
          <div>
            <h2>Nos cultes</h2>
            <div class="horaires">
$horaires
            </div>
            <p class="petit">Le culte de la Parole du mercredi a lieu une semaine sur deux :
            renseignez-vous au $telephone.</p>
          </div>
          <div>
            <h2>Comment se passe un culte</h2>
            <ol class="etapes">
              <li><strong>Accueil.</strong> Vous êtes reçu à l'entrée et installé.</li>
              <li><strong>Louange et adoration.</strong> Un temps de chants, ouvert à tous.</li>
              <li><strong>La Parole.</strong> L'enseignement du message du jour.</li>
              <li><strong>Prière.</strong> Un temps de prière pour ceux qui le désirent.</li>
            </ol>
          </div>
        </div>
      </section>

      <section class="section section--nuit">
        <div class="wrap">
          <div class="tete">
            <h2>Temps forts</h2>
            <p>Jeûnes, nuits de prière, conférences : les prochains rendez-vous du Centre.</p>
          </div>
          <div class="evenements">
$evenements
          </div>
          <div class="agenda" data-agenda hidden></div>
        </div>
      </section>

      <section class="section">
        <div class="wrap colonnes">
          <div>
            <h2>C'est votre première fois ?</h2>
            <ul class="liste">
              <li>Venez tel que vous êtes : aucune tenue particulière n'est exigée.</li>
              <li>Arrivez dix minutes avant pour être installé sans précipitation.</li>
              <li>Signalez-vous à l'accueil si vous souhaitez être accompagné.</li>
              <li>Les enfants sont les bienvenus.</li>
            </ul>
          </div>
          <div>
            <h2>Prévenir de votre venue</h2>
            <p>Dites-nous quand vous venez : l'équipe d'accueil vous attendra.</p>
            $visite
          </div>
        </div>
      </section>

$appel
    </main>
""")


def corps_programmes():
    return CORPS_PROGRAMMES.substitute(
        entete=entete("Programmes", "Venez vivre un culte avec nous.",
                      "Chaque dimanche après-midi et un mercredi soir sur deux, nous nous "
                      "rassemblons pour adorer Dieu, écouter Sa Parole et prier ensemble.",
                      "assets/img/culte/culte-predication.jpg"),
        horaires=lignes_horaires(), telephone=EGLISE["telephone"], evenements=evenements(),
        visite=bouton_whatsapp("Bonjour, je souhaite venir au culte du Centre des Amoureux de Dieu.",
                               "Prévenir sur WhatsApp"),
        appel=appel(),
    )


CORPS_ENSEIGNEMENTS = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap">
          <div class="filtres" role="search">
            <label class="sr-only" for="recherche">Rechercher une prédication</label>
            <input id="recherche" type="search" placeholder="Rechercher un titre" data-recherche>
            <div class="filtres__puces">
              <button class="puce" type="button" data-filtre="tous" aria-pressed="true">Tout</button>
$puces
            </div>
            <span class="compteur" data-compteur>$total messages</span>
          </div>
          <div class="grille-videos" data-liste>
$videos
          </div>
          <p class="vide" data-aucun-resultat hidden>Aucun message ne correspond à cette recherche.
          Essayez un autre mot, ou revenez à « Tout ».</p>
          <p class="centre"><a class="btn btn--contour-sombre" href="$youtube" target="_blank" rel="noopener">Toute la chaîne YouTube</a></p>
        </div>
      </section>

      <section class="verset">
        <div class="wrap">
          <p>« Ta parole est une lampe à mes pieds, et une lumière sur mon sentier. »</p>
          <cite>Psaume 119 : 105</cite>
        </div>
      </section>
$appel
    </main>
""")


def puces():
    return "\n".join(
        '              <button class="puce" type="button" data-filtre="%s" aria-pressed="false">%s</button>' % (g, g)
        for g in GENRES
    )


def corps_enseignements():
    return CORPS_ENSEIGNEMENTS.substitute(
        entete=entete("Prédications", "Écouter, comprendre, mettre en pratique.",
                      "Les messages du Prophète Daniel Jeff Adou, publiés sur la chaîne du ministère.",
                      "assets/img/culte/culte-assemblee.jpg"),
        puces=puces(), total=len(VIDEOS), videos="\n".join(carte_video(v) for v in VIDEOS),
        youtube=EGLISE["youtube"], appel=appel(),
    )


CORPS_MEDIATHEQUE = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap">
          <h2>Au culte</h2>
          <div class="mosaique">
$photos
          </div>
        </div>
      </section>

      <section class="section section--nuit">
        <div class="wrap">
          <h2>Affiches</h2>
          <div class="affiches">
$affiches
          </div>
          <div class="affiches" data-affiches hidden></div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="tete tete--ligne">
            <h2>En vidéo</h2>
            <a class="lien" href="enseignements.html">Toutes les prédications</a>
          </div>
          <div class="grille-videos">
$videos
          </div>
        </div>
      </section>
    </main>

    <dialog class="visionneuse" data-visionneuse aria-label="Image agrandie">
      <img src="" alt="" data-visionneuse-image>
      <form method="dialog">
        <span data-visionneuse-legende></span>
        <button type="submit">Fermer</button>
      </form>
    </dialog>
""")


def corps_mediatheque():
    photos = "\n".join(
        """            <button type="button" data-image="assets/img/culte/%s.jpg" data-legende="%s">
              <img src="assets/img/culte/%s.jpg" alt="%s" width="1280" height="658" loading="lazy">
            </button>""" % (f, attr(l), f, attr(l))
        for f, l in PHOTOS_CULTE
    )
    affiches = "\n".join(
        """            <button type="button" data-image="%s" data-legende="%s">
              <img src="%s" alt="Affiche : %s" width="900" height="1114" loading="lazy">
            </button>""" % (e["affiche"], attr(e["titre"] + ", " + e["quand"]), e["affiche"], attr(e["titre"]))
        for e in EVENEMENTS
    )
    return CORPS_MEDIATHEQUE.substitute(
        entete=entete("Médiathèque", "La vie du Centre en images.",
                      "Cultes, affiches et prédications du Centre des Amoureux de Dieu.",
                      "assets/img/culte/culte-proche.jpg"),
        photos=photos, affiches=affiches, videos="\n".join(carte_video(v) for v in VIDEOS[:6]),
    )


T_CASE = Template("""              <div class="champ">
                <label>
                  <input type="checkbox" name="$nom" required>
                  <span>$texte</span>
                </label>
              </div>""")

CORPS_TEMOIGNAGES = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes colonnes--form">
          <div>
            <h2>Partager mon témoignage</h2>
            <form class="formulaire" data-whatsapp="$whatsapp" data-api="temoignage" data-sujet="Témoignage">
              <div class="champ-duo">
                <div class="champ">
                  <label for="t-nom">Nom ou prénom</label>
                  <input id="t-nom" name="nom" type="text" required>
                </div>
                <div class="champ">
                  <label for="t-titre">Titre du témoignage</label>
                  <input id="t-titre" name="titre" type="text" placeholder="Ex. Dieu a guéri ma mère" required>
                </div>
              </div>
              <div class="champ">
                <label for="t-texte">Votre témoignage</label>
                <textarea id="t-texte" name="texte" required minlength="40"></textarea>
              </div>
              <div class="champ">
                <label for="t-identite">Sur le site, afficher</label>
                <select id="t-identite" name="identite">
                  <option>Mon nom</option>
                  <option>Mon prénom seulement</option>
                  <option>Rien (anonyme)</option>
                </select>
              </div>
$case
              <button class="btn btn--feu" type="submit">Envoyer mon témoignage</button>
              <p class="avis" data-avis hidden role="status"></p>
            </form>
          </div>
          <aside class="aparte">
            <h3>Ce qui se passe ensuite</h3>
            <ol class="etapes etapes--petit">
              <li>Votre témoignage arrive au Centre sur WhatsApp.</li>
              <li>L'équipe le lit et vous recontacte si besoin.</li>
              <li>Avec votre accord, il est publié sur cette page.</li>
            </ol>
            <blockquote class="aparte__verset">« Retourne dans ta maison, et raconte tout ce que Dieu t'a fait. » <cite>Luc 8 : 39</cite></blockquote>
          </aside>
        </div>
      </section>

      <section class="section section--sable" data-temoignages-bloc hidden>
        <div class="wrap">
          <h2>Ils ont témoigné</h2>
          <div class="temoignages" data-temoignages></div>
        </div>
      </section>
    </main>
""")


def corps_temoignages():
    return CORPS_TEMOIGNAGES.substitute(
        entete=entete("Témoignages", "Ce que Dieu a fait mérite d'être raconté.",
                      "Guérison, délivrance, provision, restauration familiale : partagez ce que vous avez vécu.",
                      "assets/img/culte/culte-assemblee.jpg"),
        whatsapp=EGLISE["whatsapp"],
        case=T_CASE.substitute(nom="autorisation", texte="J'autorise la publication de mon témoignage après relecture par l'équipe du Centre."),
    )


CORPS_PRIERE = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes colonnes--form">
          <div>
            <h2>Écrire une demande</h2>
            <form class="formulaire" data-whatsapp="$whatsapp" data-api="priere" data-sujet="Demande de prière">
              <div class="champ-duo">
                <div class="champ">
                  <label for="p-nom">Nom ou prénom</label>
                  <input id="p-nom" name="nom" type="text" required>
                </div>
                <div class="champ">
                  <label for="p-categorie">Sujet</label>
                  <select id="p-categorie" name="categorie">
                    <option>Famille</option>
                    <option>Santé</option>
                    <option>Travail</option>
                    <option>Mariage</option>
                    <option>Études et concours</option>
                    <option>Finances</option>
                    <option>Délivrance</option>
                    <option>Vie spirituelle</option>
                    <option>Autre</option>
                  </select>
                </div>
              </div>
              <div class="champ">
                <label for="p-message">Votre demande</label>
                <textarea id="p-message" name="message" required placeholder="Décrivez la situation pour laquelle vous souhaitez que l'on prie."></textarea>
              </div>
              <div class="champ">
                <label for="p-confidentialite">Confidentialité</label>
                <select id="p-confidentialite" name="confidentialite">
                  <option>Équipe pastorale uniquement</option>
                  <option>Peut être portée en réunion de prière, sans mon nom</option>
                </select>
              </div>
$case
              <button class="btn btn--feu" type="submit">Envoyer ma demande</button>
              <p class="avis" data-avis hidden role="status"></p>
            </form>
          </div>
          <aside class="aparte">
            <h3>Votre demande est entre de bonnes mains</h3>
            <ul class="liste">
              <li>Elle est lue et portée dans la prière par l'équipe pastorale.</li>
              <li>Elle n'est jamais publiée.</li>
              <li>Vous pouvez demander à être rappelé.</li>
            </ul>
            <blockquote class="aparte__verset">« Ne vous inquiétez de rien ; mais en toute chose faites connaître vos besoins à Dieu par des prières et des supplications, avec des actions de grâces. » <cite>Philippiens 4 : 6</cite></blockquote>
          </aside>
        </div>
      </section>
    </main>
""")


def corps_priere():
    return CORPS_PRIERE.substitute(
        entete=entete("Prière", "Déposez ce qui pèse sur votre cœur.",
                      "Santé, famille, travail, mariage, finances : l'équipe pastorale prie pour votre intention.",
                      "assets/img/culte/culte-scene.jpg"),
        whatsapp=EGLISE["whatsapp"],
        case=T_CASE.substitute(nom="consentement", texte="J'accepte que ma demande soit transmise à l'équipe pastorale du Centre."),
    )


CORPS_REJOINDRE = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes">
          <div>
            <h2>L'adresse</h2>
            <p class="grand">$adresse</p>
            <p>$acces</p>
            <div class="actions">
              <a class="btn btn--feu" href="$maps" target="_blank" rel="noopener">Ouvrir l'itinéraire</a>
              <a class="btn btn--contour-sombre" href="tel:+$whatsapp">Appeler le $telephone</a>
            </div>
          </div>
          <div>
            <h2>Les horaires</h2>
            <div class="horaires">
$horaires
            </div>
          </div>
        </div>
      </section>

      <section class="section section--sable">
        <div class="wrap colonnes colonnes--form">
          <div>
            <h2>Nous écrire</h2>
            <form class="formulaire" data-whatsapp="$whatsapp" data-sujet="Message depuis le site">
              <div class="champ-duo">
                <div class="champ">
                  <label for="c-nom">Nom</label>
                  <input id="c-nom" name="nom" type="text" autocomplete="name" required>
                </div>
                <div class="champ">
                  <label for="c-tel">Téléphone</label>
                  <input id="c-tel" name="telephone" type="tel" autocomplete="tel">
                </div>
              </div>
              <div class="champ">
                <label for="c-objet">Objet</label>
                <select id="c-objet" name="objet">
                  <option>Je souhaite venir au culte</option>
                  <option>Question sur les programmes</option>
                  <option>Accompagnement pastoral</option>
                  <option>Faire un don</option>
                  <option>Autre</option>
                </select>
              </div>
              <div class="champ">
                <label for="c-msg">Message</label>
                <textarea id="c-msg" name="message" required></textarea>
              </div>
              <button class="btn btn--feu" type="submit">Envoyer le message</button>
              <p class="avis" data-avis hidden role="status"></p>
            </form>
          </div>
          <aside class="aparte">
            <h3>Suivez le Centre</h3>
            <ul class="liens-reseaux">
              <li><a href="$youtube" target="_blank" rel="noopener">YouTube : les prédications</a></li>
              <li><a href="$facebook" target="_blank" rel="noopener">Facebook : les annonces</a></li>
              <li><a href="$tiktok" target="_blank" rel="noopener">TikTok : les extraits</a></li>
            </ul>
            <blockquote class="aparte__verset">« Car là où deux ou trois sont assemblés en mon nom, je suis au milieu d'eux. » <cite>Matthieu 18 : 20</cite></blockquote>
          </aside>
        </div>
      </section>
    </main>
""")


def corps_rejoindre():
    return CORPS_REJOINDRE.substitute(
        entete=entete("Nous rejoindre", "Venir au Centre.",
                      "Adresse, horaires et contact : tout pour préparer votre première visite.",
                      "assets/img/culte/culte-salle.jpg"),
        adresse=EGLISE["adresse"], acces=EGLISE["acces"], maps=EGLISE["maps"],
        whatsapp=EGLISE["whatsapp"], telephone=EGLISE["telephone"], horaires=lignes_horaires(),
        youtube=EGLISE["youtube"], facebook=EGLISE["facebook"], tiktok=EGLISE["tiktok"],
    )


CORPS_DONS = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes">
          <div>
            <h2>Comment donner</h2>
            <dl class="valeurs valeurs--une">
              <div>
                <dt>Pendant le culte</dt>
                <dd>Offrandes et dîmes sont reçues à chaque culte, le dimanche et le mercredi.</dd>
              </div>
              <div>
                <dt>Par Mobile Money</dt>
                <dd>Écrivez au secrétariat : il vous communique le numéro du Centre et vous confirme la réception de votre don.</dd>
              </div>
              <div>
                <dt>Pour un projet précis</dt>
                <dd>Un don pour une action sociale ou un événement ? Précisez-le au secrétariat.</dd>
              </div>
            </dl>
            $bouton
          </div>
          <div>
            <h2>À quoi servent vos dons</h2>
            <ul class="liste">
              <li>Le fonctionnement des cultes et des activités de l'église.</li>
              <li>L'accompagnement des personnes en difficulté.</li>
              <li>Les actions sociales et les projets du Centre.</li>
            </ul>
            <blockquote class="aparte__verset">« Que chacun donne comme il l'a résolu en son cœur, sans tristesse ni contrainte ; car Dieu aime celui qui donne avec joie. » <cite>2 Corinthiens 9 : 7</cite></blockquote>
          </div>
        </div>
      </section>
    </main>
""")


def corps_dons():
    return CORPS_DONS.substitute(
        entete=entete("Faire un don", "Donner, c'est participer à l'œuvre.",
                      "Vos dons soutiennent les cultes, l'accompagnement des personnes et les actions du Centre.",
                      "assets/img/culte/culte-large.jpg"),
        bouton=bouton_whatsapp("Bonjour, je souhaite faire un don au Centre des Amoureux de Dieu.",
                               "Écrire au secrétariat"),
    )


CORPS_JEUNE = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap colonnes colonnes--form">
          <div>
            <h2>Je participe au jeûne</h2>
            <form class="formulaire" id="form-jeune" data-programme="jeune-14-jours-nov-2026" novalidate>
              <div class="champ-duo">
                <div class="champ">
                  <label for="j-nom">Nom</label>
                  <input id="j-nom" name="nom" type="text" autocomplete="family-name" maxlength="80" required>
                </div>
                <div class="champ">
                  <label for="j-prenom">Prénom</label>
                  <input id="j-prenom" name="prenom" type="text" autocomplete="given-name" maxlength="80" required>
                </div>
              </div>
              <div class="champ">
                <label for="j-quartier">Quartier</label>
                <input id="j-quartier" name="quartier" type="text" placeholder="Ex. Riviera 2, Yopougon, Abobo" maxlength="80" required>
              </div>
              <div class="champ">
                <label for="j-telephone">Numéro de téléphone (WhatsApp)</label>
                <input id="j-telephone" name="telephone" type="tel" inputmode="tel" autocomplete="tel" placeholder="07 00 00 00 00" maxlength="20" pattern="[+0-9 .()-]{8,20}" required>
              </div>
$case
              <button class="btn btn--feu" type="submit">Valider et rejoindre le groupe WhatsApp</button>
              <p class="avis" data-avis hidden role="status"></p>
            </form>
            <div class="aparte aparte--alerte" id="jeune-groupe" hidden>
              <h3>WhatsApp ne s'est pas ouvert ?</h3>
              <p>Touchez le bouton pour entrer dans le groupe du jeûne.</p>
              <a class="btn btn--feu" id="lien-groupe" href="$groupe" rel="noopener">Rejoindre le groupe WhatsApp</a>
            </div>
          </div>
          <aside>
            <img class="affiche-seule" src="assets/img/affiches/jeune-14-jours-2026.jpg" alt="Affiche : 14 jours de jeûnes et prières, du 9 au 22 novembre 2026" width="900" height="1114">
            <div class="horaires horaires--compact">
              <div class="horaire"><span class="horaire__jour">Chaque matin</span><span class="horaire__nom">WhatsApp, groupe CAD Prière matinale</span><span class="horaire__heure">5h00 – 5h30</span></div>
              <div class="horaire"><span class="horaire__jour">Chaque soir</span><span class="horaire__nom">Google Meet</span><span class="horaire__heure">dès 20h45</span></div>
              <div class="horaire"><span class="horaire__jour">11 et 18 nov.</span><span class="horaire__nom">À l'église</span><span class="horaire__heure">mercredi</span></div>
              <div class="horaire"><span class="horaire__jour">20 nov.</span><span class="horaire__nom">Grande nuit de prophéties et de délivrances</span><span class="horaire__heure">dès 21h00</span></div>
            </div>
          </aside>
        </div>
      </section>
    </main>
    <script src="assets/js/jeune.js" defer></script>
""")

GROUPE_JEUNE = "https://chat.whatsapp.com/Hloy0fmD8zvFcszL4Epzfv"


def corps_jeune():
    return CORPS_JEUNE.substitute(
        entete=entete("Jeûne de novembre", "14 jours de jeûnes et prières",
                      "Thème : « Expérimenter la gloire de Dieu ». Du lundi 9 au dimanche 22 novembre 2026.",
                      "assets/img/culte/culte-scene.jpg"),
        groupe=GROUPE_JEUNE,
        case=T_CASE.substitute(nom="consentement", texte="J'accepte que ces informations servent au Centre pour l'organisation du jeûne."),
    )


CORPS_CONFIDENTIALITE = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap texte-long">
          <h2>Responsable</h2>
          <p>Centre des Amoureux de Dieu, $adresse, $ville ($pays). Téléphone : $telephone.</p>

          <h2>Ce que le site recueille</h2>
          <p>Le site ne crée aucun compte et ne dépose aucun cookie de mesure d'audience.</p>
          <ul class="liste">
            <li><strong>Formulaires de prière, de témoignage et de contact.</strong> Les informations saisies
            composent un message WhatsApp adressé au Centre ; vous choisissez de l'envoyer.</li>
            <li><strong>Inscription au jeûne.</strong> Nom, prénom, quartier et numéro servent uniquement à
            l'organisation du jeûne.</li>
            <li><strong>Demandes de prière.</strong> Elles sont traitées de manière confidentielle et ne sont
            jamais publiées.</li>
            <li><strong>Témoignages.</strong> Aucun témoignage n'est publié sans votre autorisation.</li>
            <li><strong>Vidéos.</strong> Le lecteur YouTube ne se charge qu'après un clic sur la vidéo.</li>
          </ul>

          <h2>Durée de conservation</h2>
          <p>Les messages reçus sont conservés le temps du suivi pastoral, puis supprimés à votre demande.</p>

          <h2>Vos droits</h2>
          <p>Vous pouvez demander l'accès, la correction ou la suppression des informations qui vous
          concernent en écrivant au Centre au $telephone.</p>
        </div>
      </section>
    </main>
""")

CORPS_LEGAL = Template("""    <main id="contenu">
$entete

      <section class="section">
        <div class="wrap texte-long">
          <h2>Éditeur</h2>
          <p>Centre des Amoureux de Dieu<br>$adresse<br>$ville, $pays<br>Téléphone : $telephone</p>
          <p>Responsable de la publication : Prophète Daniel Jeff Adou.</p>

          <h2>Propriété intellectuelle</h2>
          <p>Les textes, photographies et visuels de ce site appartiennent au Centre des Amoureux de
          Dieu, sauf mention contraire. Les vidéos sont diffusées depuis la chaîne officielle du ministère.</p>

          <h2>Données personnelles</h2>
          <p>Leur traitement est décrit dans la <a href="confidentialite.html">politique de confidentialité</a>.</p>

          <h2>Droit applicable</h2>
          <p>Ce site est soumis au droit ivoirien.</p>
        </div>
      </section>
    </main>
""")

CORPS_404 = Template("""    <main id="contenu">
      <section class="entete entete--seul" style="background-image:url('assets/img/culte/culte-salle.jpg')">
        <div class="wrap">
          <h1>Cette page n'existe pas.</h1>
          <p class="entete__intro">Le lien est peut-être ancien ou mal saisi.</p>
          <div class="actions">
            <a class="btn btn--feu" href="index.html">Retour à l'accueil</a>
            <a class="btn btn--contour" href="enseignements.html">Voir les prédications</a>
          </div>
        </div>
      </section>
    </main>
""")


def corps_simple(modele, libelle, titre, intro):
    return modele.substitute(
        entete=entete(libelle, titre, intro, "assets/img/culte/culte-salle.jpg", classe="entete--court"),
        adresse=EGLISE["adresse"], ville=EGLISE["ville"], pays=EGLISE["pays"], telephone=EGLISE["telephone"],
    )


CORPS_FICHE = Template("""    <main id="contenu">
      <section class="fiche">
        <div class="wrap">
          <nav class="fil" aria-label="Fil d'Ariane"><a href="../index.html">Accueil</a> <span aria-hidden="true">/</span> <a href="../enseignements.html">Prédications</a></nav>
          <div class="fiche__lecteur">
            <button class="lecteur lecteur--grand" type="button" data-video="$id" data-titre="$titre_attr" aria-label="Lire la vidéo : $titre_attr">
              <img src="../$vignette" alt="" width="1280" height="720">
              <span class="lecteur__bouton" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
            </button>
          </div>
          <div class="fiche__texte">
            <p class="video__meta">$genre, $date</p>
            <h1>$titre</h1>
            <p>Message du Prophète Daniel Jeff Adou, publié le $date sur la chaîne officielle du Centre des Amoureux de Dieu.</p>
            <div class="partage">
              <a class="btn btn--feu" href="https://wa.me/?text=$texte_partage" target="_blank" rel="noopener">Partager sur WhatsApp</a>
              <a class="btn btn--contour" href="https://www.facebook.com/sharer/sharer.php?u=$url" target="_blank" rel="noopener">Facebook</a>
              <button class="btn btn--contour" type="button" data-copier="$url">Copier le lien</button>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="tete tete--ligne">
            <h2>Autres messages</h2>
            <a class="lien" href="../enseignements.html">Toutes les prédications</a>
          </div>
          <div class="grille-videos">
$autres
          </div>
        </div>
      </section>
    </main>
""")


def fiche(v):
    from urllib.parse import quote
    url = "%s/predications/%s.html" % (EGLISE["site"], v["slug"])
    autres = [a for a in VIDEOS if a["id"] != v["id"]][:3]
    corps = CORPS_FICHE.substitute(
        titre=v["titre"], titre_attr=attr(v["titre"]), genre=v["genre"], date=v["date"],
        id=v["id"], vignette=vignette(v), url=url,
        texte_partage=quote("%s, Prophète Daniel Jeff Adou : %s" % (v["titre"], url)),
        autres="\n".join(carte_video(a, prefixe="../") for a in autres),
    )
    jsonld = {
        "@context": "https://schema.org", "@type": "VideoObject", "name": v["titre"],
        "description": "Message du %s, %s." % (v["date"], PROPHETE["nom"]),
        "uploadDate": v["iso"], "url": url,
        "thumbnailUrl": "%s/%s" % (EGLISE["site"], vignette(v)),
        "embedUrl": "https://www.youtube-nocookie.com/embed/%s" % v["id"],
        "publisher": {"@type": "Organization", "name": EGLISE["nom"]},
    }
    return page_html("predications/%s.html" % v["slug"], v["titre"],
                     "%s : message du %s, %s." % (v["titre"], v["date"], PROPHETE["nom"]),
                     corps, index=True, jsonld=jsonld, prefixe="../")


# ── Liste des pages ───────────────────────────────────────────────────

def pages_simples():
    return [
        ("index.html", "Accueil",
         "Centre des Amoureux de Dieu, église à Cocody Riviera 2 (Abidjan) : cultes le dimanche, prédications du Prophète Daniel Jeff Adou, prière et événements.",
         corps_accueil(), True, None, "page-accueil"),
        ("le-centre.html", "Le Centre",
         "Vision, mission et valeurs du Centre des Amoureux de Dieu, église fondée en octobre 2023 à Abidjan.",
         corps_centre(), True, None, ""),
        ("le-prophete.html", "Le Prophète",
         "Le Prophète Daniel Jeff Adou, fondateur et pasteur du Centre des Amoureux de Dieu, auteur de « Sortir des prisons familiales ».",
         corps_prophete(), True, None, ""),
        ("programmes.html", "Programmes",
         "Horaires des cultes, déroulement, jeûnes, nuits de prière et événements du Centre des Amoureux de Dieu.",
         corps_programmes(), True, None, ""),
        ("enseignements.html", "Prédications",
         "Les prédications du Prophète Daniel Jeff Adou, avec recherche et filtres.",
         corps_enseignements(), True, None, ""),
        ("mediatheque.html", "Médiathèque",
         "Photos des cultes, affiches et vidéos du Centre des Amoureux de Dieu.",
         corps_mediatheque(), True, None, ""),
        ("temoignages.html", "Témoignages",
         "Partager un témoignage avec le Centre des Amoureux de Dieu.",
         corps_temoignages(), True, None, ""),
        ("priere.html", "Prière",
         "Envoyer une demande de prière à l'équipe pastorale du Centre des Amoureux de Dieu, en toute confidentialité.",
         corps_priere(), True, None, ""),
        ("jeune.html", "Jeûne de novembre",
         "Inscription aux 14 jours de jeûnes et prières du Centre des Amoureux de Dieu (9 au 22 novembre 2026) : Expérimenter la gloire de Dieu.",
         corps_jeune(), True, None, ""),
        ("nous-rejoindre.html", "Nous rejoindre",
         "Adresse, itinéraire, horaires et contact du Centre des Amoureux de Dieu à Cocody Riviera 2, Abidjan.",
         corps_rejoindre(), True, None, ""),
        ("dons.html", "Faire un don",
         "Soutenir les cultes, l'accompagnement et les actions du Centre des Amoureux de Dieu.",
         corps_dons(), True, None, ""),
        ("mentions-legales.html", "Mentions légales",
         "Mentions légales du site du Centre des Amoureux de Dieu.",
         corps_simple(CORPS_LEGAL, "Mentions légales", "Mentions légales", "Éditeur, propriété intellectuelle et droit applicable."),
         False, None, ""),
        ("confidentialite.html", "Confidentialité",
         "Politique de confidentialité du site du Centre des Amoureux de Dieu.",
         corps_simple(CORPS_CONFIDENTIALITE, "Confidentialité", "Vos données", "Ce que le site recueille, pourquoi, et vos droits."),
         False, None, ""),
        ("404.html", "Page introuvable", "La page demandée n'existe pas.",
         CORPS_404.substitute(), False, None, ""),
    ]


# ══════════════════════════════════════════════════════════════════════
# 4. ÉCRITURE
# ══════════════════════════════════════════════════════════════════════

OBSOLETES = ["cultes.html", "evenements.html", "contact.html",
             "predications/service-prohetique-ancien.html"]


def ecrire():
    ecrits = []
    for fichier, titre, description, corps, index, jsonld, classe in pages_simples():
        html = page_html(fichier, titre, description, corps, index=index, jsonld=jsonld, classe_corps=classe)
        with open(os.path.join(RACINE, fichier), "w", encoding="utf-8") as fh:
            fh.write(html)
        ecrits.append((fichier, len(html)))

    dossier = os.path.join(RACINE, "predications")
    os.makedirs(dossier, exist_ok=True)
    for v in VIDEOS:
        html = fiche(v)
        with open(os.path.join(dossier, "%s.html" % v["slug"]), "w", encoding="utf-8") as fh:
            fh.write(html)
        ecrits.append(("predications/%s.html" % v["slug"], len(html)))

    for nom in OBSOLETES:
        chemin = os.path.join(RACINE, nom)
        if os.path.exists(chemin):
            os.remove(chemin)
    return ecrits


def sitemap():
    entrees = []
    for fichier, _, _, _, index, _, _ in pages_simples():
        if not index:
            continue
        entrees.append(
            "  <url>\n    <loc>%s/%s</loc>\n    <changefreq>weekly</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (EGLISE["site"], "" if fichier == "index.html" else fichier,
               "1.0" if fichier == "index.html" else "0.7"))
    for v in VIDEOS:
        entrees.append(
            "  <url>\n    <loc>%s/predications/%s.html</loc>\n    <lastmod>%s</lastmod>\n    <priority>0.6</priority>\n  </url>"
            % (EGLISE["site"], v["slug"], v["iso"]))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(entrees) + "\n</urlset>\n")


A_FOURNIR = """# Contenus à fournir par le Centre

Le site ne montre plus de cases « à confirmer » : ce qui manque est simplement
absent. Voici ce qui l'enrichirait.

- **Photos HD** des cultes, de la louange et des événements (les photos actuelles
  sont tirées des vidéos de culte, en 720p).
- **Biographie du Prophète** : parcours, appel, dates clés.
- **Histoire du Centre** : étapes marquantes depuis octobre 2023.
- **Numéro Mobile Money** du Centre, si vous voulez l'afficher sur la page Dons.
- **Instagram**, si le Centre a un compte.
- **Couverture HD du livre** « Sortir des prisons familiales »
  (`assets/img/livre-sortir-des-prisons.jpg`, actuellement générée depuis le PDF).

Pour modifier le site : éditer `outils/generer.py` puis lancer
`python3 outils/generer.py`.
"""


if __name__ == "__main__":
    resultat = ecrire()
    with open(os.path.join(RACINE, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap())
    with open(os.path.join(RACINE, "CONTENU-A-COMPLETER.md"), "w", encoding="utf-8") as fh:
        fh.write(A_FOURNIR)
    for nom, taille in resultat:
        print("%-52s %7d octets" % (nom, taille))

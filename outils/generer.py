#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du site vitrine du CENTRE DES AMOUREUX DE DIEU.

Structure conforme au cahier des charges (rubriques 3.1 à 3.10) pour la partie
publique. Les gabarits utilisent string.Template (`$jeton`) et non `%` : un
style en ligne contenant `border-radius:50%` casse un gabarit formaté par `%`
(TypeError: not enough arguments for format string) et la ligne signalée est
celle du gabarit, pas le `%` coupable.

Une seule source de vérité : EGLISE, CRENEAUX, VIDEOS, PROPHETE.

Usage :
    python3 outils/generer.py
"""

import json
import os
import re
import unicodedata
from string import Template

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════════════════
# 1. DONNÉES — la seule source de vérité du site
# ══════════════════════════════════════════════════════════════════════

AC = "A_COMPLETER"

EGLISE = {
    "nom": "Centre des Amoureux de Dieu",
    "nom_maj": "CENTRE DES AMOUREUX DE DIEU",
    "sigle": "CAD",
    "pays": "Côte d'Ivoire",
    "ville": "Abidjan",
    "quartier": "Cocody Rivera 2",
    "adresse": "Cocody Rivera 2, en face de l'imprimerie DA Communication",
    "telephone": "+225 07 87 59 32 89",
    "whatsapp": "+225 07 87 59 32 89",
    "email": "contact@centre-des-amoureux.org",
    "youtube": "https://www.youtube.com/@jeffadou3161",
    "facebook": AC,
    "instagram": AC,
    "tiktok": AC,
    "annee_fondation": "octobre 2023",
    # Adresse de publication actuelle. Le jour où le domaine est acheté,
    # remplacer par "https://centre-des-amoureux.org" puis régénérer.
    "site": "https://jeffadou258-afk.github.io/centre-amoureux-site",
}

# Décision du client (31/10/2026) : le pasteur du Centre est Daniel Jeff Adou.
# Le cahier des charges nomme « Issa Kourouma » — erreur du document, signalée
# et tranchée par le client. Ne pas « corriger » sans nouvelle décision.
PROPHETE = {
    "nom": "Prophète Daniel Jeff Adou",
    "nom_court": "Daniel Jeff Adou",
    "role": "Prophète et pasteur du Centre des Amoureux de Dieu",
    "chaine": EGLISE["youtube"],
}

# Horaires communiqués par le Centre le 31/10/2026.
# Le culte du mercredi a lieu « en quinze » : une semaine sur deux.
CRENEAUX = [
    ("Dimanche", "Culte d'adoration", "14h00 – 18h30"),
    ("Mercredi", "Culte de la Parole (toutes les deux semaines)", "19h00 – 21h00"),
]

# ── Vision, mission et valeurs officielles (document de la direction) ──
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

# Responsable omis = poste non encore communiqué (affiché « à confirmer »).
DEPARTEMENTS = [
    ("Accueil des nouveaux", "Koffi Prisca", "Prise en charge des nouveaux et des visiteurs, orientation vers les cellules et le pasteur."),
    ("Sentinelles (intercession)", None, "Couvre l'église en prière, intercède avant et pendant chaque culte."),
    ("La Voix des Chérubins (chantres)", "Lilian Armoo", "Prépare l'atmosphère spirituelle : louange, adoration, répétitions."),
    ("Médias", "N'Taye Daniel", "Sonorisation, captation, diffusion en direct, réseaux sociaux et visuels."),
    ("Gagneurs d'âmes (évangélisation)", "Carmel Yao", "Sorties d'évangélisation, campagnes et suivi des nouveaux convertis."),
    ("Accueil général", "Marylène", "Accueil à l'entrée, placement, ordre et propreté du lieu."),
    ("Gestion des cultes", None, "Coordonne le programme du culte et les plannings des intervenants."),
    ("Trésorerie", None, "Dîmes, offrandes, comptabilité et rapports au pasteur."),
    ("Secrétariat", None, "Documents, courriers, plannings et comptes rendus de réunions."),
    ("Moyens généraux", "Kossonou Léon", "Logistique matérielle : chaises, tentes, eau, entretien."),
    ("Services d'ordre", None, "Sécurité des lieux, maintien de l'ordre et gestion des flux."),
]

VIDEOS = [
    {"id": "Vke4iYzemIs", "titre": "Tous les grands ont d'abord rêvé grand",
     "iso": "2026-10-17", "date": "17 octobre 2026", "genre": "Exhortation",
     "slug": "tous-les-grands-ont-reve-grand"},
    {"id": "SXql767Lo7w", "titre": "10 CHOSES A SAVOIR SUR L'ONCTION ROYALE",
     "iso": "2026-10-16", "date": "16 octobre 2026", "genre": "Enseignement",
     "slug": "onction-royale-10-choses-a-savoir"},
    {"id": "jrefqSertlc", "titre": "10 CHOSES A SAVOIR SUR L'ONCTION ROYALE",
     "iso": "2026-10-12", "date": "12 octobre 2026", "genre": "Enseignement",
     "slug": "onction-royale-10-choses"},
    {"id": "2CHnQLRtN0Y", "titre": "L'huile, le cœur et le trône",
     "iso": "2026-09-28", "date": "28 septembre 2026", "genre": "Enseignement",
     "slug": "huile-coeur-et-trone"},
    {"id": "-hKzzUDnh0E", "titre": "PRIONS ENSEMBLE",
     "iso": "2026-09-24", "date": "24 septembre 2026", "genre": "Prière",
     "slug": "prions-ensemble"},
    {"id": "OlT6R0wc0JQ", "titre": "L'HUILE LE COEUR ET LE TRONE (PARTIE 1)",
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

NAV = [
    ("index.html", "Accueil"),
    ("le-centre.html", "Le Centre"),
    ("le-prophete.html", "Le Prophète"),
    ("programmes.html", "Programmes"),
    ("enseignements.html", "Enseignements"),
    ("mediatheque.html", "Médiathèque"),
    ("temoignages.html", "Témoignages"),
    ("priere.html", "Prière"),
    ("nous-rejoindre.html", "Nous rejoindre"),
]

# ══════════════════════════════════════════════════════════════════════
# 2. OUTILS
# ══════════════════════════════════════════════════════════════════════


def m(valeur, quoi="à confirmer"):
    """Marque une information que l'église doit encore fournir."""
    if valeur == AC:
        return (
            '<span class="a-completer" data-a-completer="1" '
            'title="Information à fournir par le Centre">%s</span>' % quoi
        )
    return valeur


def vignette(v):
    return "assets/img/videos/%s.jpg" % v["id"]


def lien_fiche(v, prefixe=""):
    return "%spredications/%s.html" % (prefixe, v["slug"])


# ── Composants ────────────────────────────────────────────────────────

T_VIDEO = Template("""            <article class="video-carte monte" data-genre="$genre" data-titre="$titre_attr">
              <div class="video-carte__media">
                <button class="lecteur" type="button" data-video="$id" data-titre="$titre_attr"
                        aria-label="Lire la vidéo : $titre_attr">
                  <img class="vignette" src="$vignette" alt="" width="1280" height="720" loading="lazy">
                  <span class="lecteur__voile" aria-hidden="true"></span>
                  <span class="lecteur__badge" aria-hidden="true">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                  </span>
                  <span class="lecteur__legende">Cliquer pour lire</span>
                </button>
              </div>
              <div class="video-carte__corps">
                <p class="video-carte__meta">$genre · $date</p>
                <h3 class="video-carte__titre">
                  <a href="$lien" style="text-decoration:none;color:inherit">$titre</a>
                </h3>
              </div>
            </article>""")


def carte_video(v, prefixe=""):
    return T_VIDEO.substitute(
        id=v["id"],
        titre=v["titre"],
        titre_attr=v["titre"].replace('"', "&quot;"),
        date=v["date"],
        genre=v["genre"],
        slug=v["slug"],
        lien=lien_fiche(v, prefixe),
        vignette=vignette(v),
    )


T_LIGNE_CRENEAU = Template("""          <div class="programme__ligne">
            <span class="programme__jour">$jour</span>
            <span class="programme__nom">$intitule</span>
            <span class="programme__heure">$heure</span>
          </div>""")


def lignes_creneaux():
    return "\n".join(
        T_LIGNE_CRENEAU.substitute(jour=j, intitule=i, heure=m(h))
        for j, i, h in CRENEAUX
    )


T_CARTE_CULTE = Template("""          <aside class="carte-culte monte monte--2" aria-label="Horaires des cultes">
            <p class="carte-culte__titre">
              <span class="pastille-vie" aria-hidden="true"></span>
              Nos rendez-vous
            </p>
$lignes
            <div class="carte-culte__pied">
              <span>$ville</span>
              <a class="link-arrow" href="programmes.html">Voir les programmes</a>
            </div>
          </aside>""")


def carte_culte():
    lignes = []
    for jour, intitule, heure in CRENEAUX:
        lignes.append(
            """            <div class="creneau">
              <span>
                <span class="creneau__jour">%s</span><br>
                <span class="tiny muted">%s</span>
              </span>
              <span class="creneau__heure">%s</span>
            </div>"""
            % (jour, intitule, m(heure, "horaire à confirmer"))
        )
    return T_CARTE_CULTE.substitute(
        lignes="\n".join(lignes), ville=m(EGLISE["ville"], "ville à confirmer")
    )


T_CTA = Template("""      <div class="wrap">
        <div class="cta-final">
          <h2>Vous êtes attendu, tel que vous êtes.</h2>
          <p>
            Que vous veniez pour la première fois ou que vous cherchiez une maison
            spirituelle, il y a une place pour vous au $nom.
          </p>
          <div class="cta-final__actions">
            <a class="btn btn--primary btn--lg" href="${prefixe}nous-rejoindre.html">Préparer ma visite</a>
            <a class="btn btn--sur-ink btn--lg" href="${prefixe}priere.html">Demander une prière</a>
          </div>
        </div>
      </div>""")

CTA_FINAL = T_CTA.substitute(nom=EGLISE["nom"], prefixe="")

T_FIL = Template("""          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="${prefixe}index.html">Accueil</a><span aria-hidden="true">/</span><span>$libelle</span>
          </nav>""")


def fil(libelle, prefixe=""):
    return T_FIL.substitute(prefixe=prefixe, libelle=libelle)


def cta_final(prefixe=""):
    return T_CTA.substitute(nom=EGLISE["nom"], prefixe=prefixe)


# ── Gabarit de page ───────────────────────────────────────────────────

T_PAGE = Template("""<!doctype html>
<html lang="fr" data-etat="travail">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>$titre_complet</title>
    <meta name="description" content="$description">
    <meta name="robots" content="$robots">
    <meta name="theme-color" content="#ED6C10">
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

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="${prefixe}assets/css/style.css">
    <script type="application/ld+json">
$jsonld
    </script>
  </head>
  <body>
    <a class="skip" href="#contenu">Aller au contenu</a>

    <div class="bandeau-travail" role="note">
      Version de travail — les informations surlignées doivent être fournies par le Centre.
    </div>

    <header class="site-header">
      <div class="wrap">
        <a class="marque" href="${prefixe}index.html" aria-label="$nom — accueil">
          <img class="marque__logo" src="${prefixe}assets/img/logo-flamme.png"
               alt="" width="26" height="46" fetchpriority="high">
          <span class="marque__texte">
            <span class="marque__nom">$nom</span>
            <span class="marque__sous">$pays</span>
          </span>
        </a>

        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-principal">
          <span class="nav-toggle__barre" aria-hidden="true"></span>
          <span class="sr-only">Ouvrir le menu</span>
        </button>

        <nav class="nav" id="nav-principal" data-ouvert="false" aria-label="Navigation principale">
$navigation
        </nav>

        <a class="btn btn--primary nav-cta" href="${prefixe}dons.html">Faire un don</a>
      </div>
    </header>

$corps

    <footer class="site-footer">
      <div class="wrap">
        <div class="footer-grille">
          <div>
            <a class="marque" href="${prefixe}index.html">
              <img class="marque__logo" src="${prefixe}assets/img/logo-flamme.png"
               alt="" width="26" height="46" fetchpriority="high">
              <span class="marque__texte">
                <span class="marque__nom">$nom</span>
                <span class="marque__sous">$pays</span>
              </span>
            </a>
            <p class="espace-haut" style="max-width:34ch">
              Une maison de prière, de Parole et d'amour fraternel, ouverte à tous.
            </p>
            <p class="tiny" style="margin-top:18px">
              <a href="$youtube" rel="noopener" target="_blank">Chaîne YouTube du ministère</a>
            </p>
          </div>
          <div>
            <h3>Le Centre</h3>
            <ul class="footer-liens">
              <li><a href="${prefixe}le-centre.html">Qui nous sommes</a></li>
              <li><a href="${prefixe}le-prophete.html">Le Prophète</a></li>
              <li><a href="${prefixe}programmes.html">Nos programmes</a></li>
              <li><a href="${prefixe}temoignages.html">Témoignages</a></li>
            </ul>
          </div>
          <div>
            <h3>Ressources</h3>
            <ul class="footer-liens">
              <li><a href="${prefixe}enseignements.html">Enseignements</a></li>
              <li><a href="${prefixe}mediatheque.html">Médiathèque</a></li>
              <li><a href="${prefixe}priere.html">Demande de prière</a></li>
              <li><a href="${prefixe}dons.html">Faire un don</a></li>
            </ul>
          </div>
          <div>
            <h3>Nous trouver</h3>
            <ul class="footer-liens">
              <li>Ville : $ville</li>
              <li>Adresse : $adresse</li>
              <li>Téléphone : $telephone</li>
              <li><a href="mailto:$email">$email</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bas">
          <p class="mb-0">© <span data-annee>2026</span> $nom. Tous droits réservés.</p>
          <ul>
            <li><a href="${prefixe}mentions-legales.html">Mentions légales</a></li>
            <li><a href="${prefixe}confidentialite.html">Confidentialité</a></li>
            <li><a href="${prefixe}nous-rejoindre.html">Contact</a></li>
          </ul>
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
    liens.append(
        '          <a class="btn btn--primary nav__don" href="%sdons.html">Faire un don</a>' % prefixe
    )
    return "\n".join(liens)


def page_html(page, titre, description, corps, index=True, jsonld=None, prefixe=""):
    nom_complet = (
        "%s · %s" % (EGLISE["nom"], titre)
        if titre == "Accueil"
        else "%s · %s" % (titre, EGLISE["nom"])
    )
    if jsonld is None:
        jsonld = {
            "@context": "https://schema.org",
            "@type": "Church",
            "name": EGLISE["nom"],
            "alternateName": EGLISE["nom_maj"],
            "description": "Église du Centre des Amoureux de Dieu — cultes, enseignements, prière et vie fraternelle.",
            "url": EGLISE["site"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": EGLISE["adresse"],
                "addressLocality": EGLISE["ville"],
                "addressCountry": "CI",
            },
            "telephone": EGLISE["telephone"],
            "sameAs": [EGLISE["youtube"]],
        }
    return T_PAGE.substitute(
        titre_complet=nom_complet,
        description=description,
        robots="index,follow" if index else "noindex,follow",
        canonical=EGLISE["site"] + "/" + ("" if page == "index.html" else page),
        og_titre=titre,
        site=EGLISE["site"],
        nom=EGLISE["nom"],
        sigle=EGLISE["sigle"],
        pays=EGLISE["pays"],
        youtube=EGLISE["youtube"],
        email=EGLISE["email"],
        ville=m(EGLISE["ville"]),
        adresse=m(EGLISE["adresse"]),
        telephone=m(EGLISE["telephone"]),
        navigation=navigation(page, prefixe),
        jsonld=json.dumps(jsonld, ensure_ascii=False, indent=2),
        corps=corps,
        prefixe=prefixe,
    )


# ══════════════════════════════════════════════════════════════════════
# 3. PAGES
# ══════════════════════════════════════════════════════════════════════

CORPS_ACCUEIL = Template("""    <main id="contenu">
      <section class="hero">
        <div class="wrap">
          <div class="hero__grille">
            <div>
              <p class="eyebrow monte">Église · Abidjan · depuis octobre 2023</p>
              <h1 class="monte monte--2">
                Un lieu pour <em>aimer Dieu</em>,<br>et être aimé de Lui.
              </h1>
              <p class="lead monte monte--3">
                Le Centre des Amoureux de Dieu est une famille spirituelle où la
                Parole est enseignée avec clarté, où la prière est une respiration,
                et où chacun est accueilli avec dignité.
              </p>
              <div class="hero__actions monte monte--3">
                <a class="btn btn--primary btn--lg" href="le-centre.html">Découvrir notre ministère</a>
                <a class="btn btn--ghost btn--lg" href="nous-rejoindre.html">Nous rejoindre</a>
              </div>
              <p class="hero__note monte monte--3">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-4.6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.4-7 10-7 10Z"/></svg>
                Ouvert à tous, sans condition et sans tenue exigée. Culte le dimanche
                de 14h00 à 18h30, à Cocody Rivera 2.
              </p>
            </div>
$carte_culte
          </div>
        </div>
      </section>

      <section class="section section--serre">
        <div class="wrap">
          <div class="grille grille--4">
            <div class="carte">
              <p class="carte__numero">01</p>
              <h3>Adoration</h3>
              <p class="tiny muted mb-0">Nous nous rassemblons pour honorer Dieu, dans la louange et le silence.</p>
            </div>
            <div class="carte">
              <p class="carte__numero">02</p>
              <h3>Parole</h3>
              <p class="tiny muted mb-0">La Bible est enseignée simplement, pour être vécue au quotidien.</p>
            </div>
            <div class="carte">
              <p class="carte__numero">03</p>
              <h3>Communion</h3>
              <p class="tiny muted mb-0">Personne ne devrait avancer seul : nous marchons ensemble.</p>
            </div>
            <div class="carte">
              <p class="carte__numero">04</p>
              <h3>Service</h3>
              <p class="tiny muted mb-0">Aimer Dieu se traduit par des actes concrets envers les autres.</p>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="align-items:center;gap:clamp(28px,5vw,64px)">
            <div>
              <p class="eyebrow">Qui nous sommes</p>
              <h2>Une maison où l'on apprend à aimer.</h2>
              <p>
                « Amoureux de Dieu » n'est pas un titre que l'on se donne : c'est une
                direction de vie. Nous apprenons à aimer Dieu d'un amour vrai, et à
                nous aimer les uns les autres sans masque.
              </p>
              <ul class="liste-propre">
                <li>Un accueil chaleureux, dès la porte.</li>
                <li>Des enseignements clairs, ancrés dans l'Écriture.</li>
                <li>Un accompagnement pastoral pour les moments difficiles.</li>
                <li>Une place pour les enfants, les jeunes et les familles.</li>
              </ul>
              <a class="link-arrow" href="le-centre.html">Découvrir le Centre</a>
            </div>
            <div class="encart encart--or">
              <p class="verse">
                « Pour nous, nous l'aimons, parce qu'il nous a aimés le premier. »
                <cite>1 Jean 4 : 19</cite>
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Enseignements</p>
            <h2>Les dernières prédications</h2>
            <p class="lead">
              Retrouvez les prédications et temps de prière publiés sur la chaîne
              du ministère, à écouter et à partager.
            </p>
          </div>
          <div class="grille grille--3">
$videos
          </div>
          <p class="section__pied">
            <a class="btn btn--ghost" href="enseignements.html">Toutes les prédications</a>
          </p>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="align-items:center;gap:clamp(28px,5vw,64px)">
            <figure class="portrait" style="margin:0">
              <img src="assets/img/prophete-bras-croises.jpg" alt="$pasteur"
                   width="720" height="960" loading="lazy">
            </figure>
            <div>
              <p class="eyebrow">Le Prophète</p>
              <h2>Une parole portée, pas seulement prononcée.</h2>
              <p class="lead">
                Le Centre des Amoureux de Dieu est conduit par le $pasteur, dont
                l'enseignement est diffusé chaque semaine sur la chaîne du ministère.
              </p>
              <p>
                Sa priorité : une parole compréhensible, fidèle au texte biblique,
                qui éclaire la vie réelle des personnes.
              </p>
              <a class="link-arrow" href="le-prophete.html">Lire sa présentation</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--ink">
        <div class="wrap">
          <div class="section__entete section__entete--centre">
            <p class="eyebrow eyebrow--or" style="color:#EF9C19">Prière</p>
            <h2>Un fardeau à déposer ?</h2>
            <p class="lead">
              Notre équipe pastorale prie chaque semaine pour les intentions reçues.
              Vous pouvez écrire librement : votre demande restera confidentielle.
            </p>
            <div class="hero__actions" style="justify-content:center">
              <a class="btn btn--primary btn--lg" href="priere.html">Envoyer une demande</a>
              <a class="btn btn--sur-ink btn--lg" href="temoignages.html">Partager un témoignage</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          $cta
        </div>
      </section>
    </main>
""")


CORPS_CENTRE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Qui nous sommes</p>
          <h1>Une église, une famille, une armée d'amoureux.</h1>
          <p class="lead">
            Le Centre des Amoureux de Dieu est une communauté chrétienne établie à
            $ville, en $pays. Notre raison d'être tient en une phrase : former des
            ouvriers, bâtir une armée d'amoureux passionnés pour Dieu, et les
            équiper pour impacter la société.
          </p>
        </div>
      </section>

      <section class="section" id="vision">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,60px);align-items:center">
            <div>
              <p class="eyebrow">Notre vision</p>
              <h2>Former, bâtir, équiper.</h2>
              <p class="lead">« $vision »</p>
              <ul class="liste-propre">
                <li><strong>Former des ouvriers et des serviteurs</strong> — équiper les membres pour le ministère et le service.</li>
                <li><strong>Bâtir une armée d'amoureux passionnés</strong> — créer un peuple engagé et motivé.</li>
                <li><strong>Impacter la société</strong> — influencer positivement les familles, les communautés et les nations.</li>
              </ul>
            </div>
            <div class="encart encart--or">
              <p class="verse">
                « Le plus petit deviendra un millier, et le moindre, une nation puissante. »
                <cite>Ésaïe 60 : 22</cite>
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,60px);align-items:start">
            <div>
              <p class="eyebrow">Notre mission</p>
              <h2>Comment nous y allons.</h2>
              <p>« $mission »</p>
            </div>
            <div class="carte">
              <h3>Nos actions concrètes</h3>
              <ul class="liste-propre mb-0">
                <li>Prédication et enseignement biblique</li>
                <li>Évangélisation et formation continue</li>
                <li>Développement de leaders passionnés</li>
                <li>Implication dans la transformation de la société</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="valeurs">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Nos valeurs</p>
            <h2>Les principes qui nous gouvernent</h2>
            <p class="lead">
              Six valeurs, chacune rattachée à un texte biblique : elles servent de
              référence à nos décisions et à nos projets.
            </p>
          </div>
          <div class="grille grille--3">
$valeurs
          </div>
        </div>
      </section>

      <section class="section section--alt" id="departements">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Nos départements</p>
            <h2>Onze services, une même maison</h2>
            <p class="lead">
              Chaque département a sa mission et son responsable. Les postes dont le
              responsable n'est pas encore communiqué sont signalés comme tels.
            </p>
          </div>
          <div class="grille grille--3">
$departements
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(24px,4vw,48px);align-items:center">
            <div>
              <p class="eyebrow">Le pasteur</p>
              <h2>$pasteur</h2>
              <p class="lead">$role</p>
              <p>
                Le Centre des Amoureux de Dieu est conduit par le $pasteur, dont
                l'enseignement est diffusé chaque semaine sur la chaîne du ministère.
              </p>
              <a class="link-arrow" href="le-prophete.html">Le présenter en détail</a>
            </div>
            <figure class="portrait" style="margin:0">
              <img src="assets/img/prophete-portrait.jpg" alt="$pasteur"
                   width="852" height="1150" loading="lazy">
            </figure>
          </div>
        </div>
      </section>

      <section class="section section--ink">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(24px,4vw,48px);align-items:center">
            <div>
              <p class="eyebrow eyebrow--or" style="color:#EF9C19">Le logo du Centre</p>
              <h2>La flamme et la colombe.</h2>
              <p>
                Un oiseau qui prend son envol dans une flamme : la passion pour Dieu
                et la liberté qu'Il donne. Le logo animé ci-contre est celui du Centre.
              </p>
            </div>
            <video class="logo-video" src="assets/img/logo-anime.mp4"
                   poster="assets/img/logo-animation-affiche.jpg"
                   autoplay muted loop playsinline preload="metadata"
                   aria-label="Logo animé du Centre des Amoureux de Dieu"></video>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(24px,4vw,48px)">
            <div>
              <h2>Notre histoire</h2>
              <p>
                Le Centre des Amoureux de Dieu a été <strong>fondé en octobre
                2023</strong>, à Abidjan (Cocody Rivera 2). Depuis, la communauté
                se rassemble chaque dimanche et une semaine sur deux en milieu de
                semaine, autour de la Parole, de la prière et du service.
              </p>
              <div class="etat-vide" style="text-align:left">
                <p class="tiny mb-0">
                  Les étapes du développement du ministère — premiers cultes,
                  ouvertures de départements, campagnes — seront ajoutées ici
                  lorsque la direction les aura communiquées. Aucun récit n'est
                  inventé.
                </p>
              </div>
            </div>
            <div>
              <h2>Nous rendre visite</h2>
              <div class="carte">
                <p class="carte__numero">Adresse</p>
                <p class="mb-0"><strong>$adresse</strong></p>
                <p class="mb-0">$quartier — $ville</p>
                <p class="tiny muted espace-haut mb-0">
                  Culte le dimanche de 14h00 à 18h30. Culte de la Parole le mercredi,
                  une semaine sur deux, de 19h00 à 21h00.
                </p>
              </div>
              <a class="btn btn--primary espace-haut" href="nous-rejoindre.html">Préparer ma visite</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">$cta</div>
      </section>
    </main>
""")


CORPS_PROPHETE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Le Prophète</p>
          <h1>$pasteur</h1>
          <p class="lead">$role</p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,60px);align-items:start">
            <div>
              <h2>Présentation</h2>
              <p>
                Le Centre des Amoureux de Dieu est conduit par le $pasteur. Son
                enseignement est diffusé chaque semaine sur la chaîne du ministère,
                et porte une conviction simple : la Parole de Dieu éclaire la vie
                réelle, ici et maintenant.
              </p>
              <p>
                Sa prédication insiste sur l'amour de Dieu, la vie de prière et la
                transformation du cœur — trois axes que l'on retrouve dans les
                messages publiés.
              </p>
              <div class="etat-vide" style="text-align:left">
                <h3 style="font-size:1.05rem">Biographie officielle et parcours</h3>
                <p class="mb-0 tiny">
                  Les éléments biographiques (date de conversion, parcours
                  ministériel, ordination, années de service) doivent être fournis
                  par le Centre. Ils ne sont pas inventés ici : la place est
                  réservée, le texte viendra du ministère.
                </p>
              </div>
            </div>
            <div>
              <figure class="portrait" style="margin:0">
                <img src="assets/img/prophete-portrait.jpg" alt="$pasteur"
                     width="852" height="1150" loading="lazy">
              </figure>
              <a class="btn btn--primary espace-haut" href="$youtube" target="_blank" rel="noopener" style="width:100%">
                Voir sa chaîne YouTube
              </a>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Ses messages</p>
            <h2>Les dernières prédications</h2>
            <p class="lead">Vidéos publiées sur la chaîne officielle du ministère.</p>
          </div>
          <div class="grille grille--3">
$videos
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Son ministère</p>
            <h2>Ce qui caractérise le ministère</h2>
          </div>
          <div class="grille grille--3">
            <article class="carte">
              <p class="carte__numero">01</p>
              <h3>L'amour de Dieu</h3>
              <p class="tiny muted mb-0">Comprendre qu'on est aimé avant d'être méritant.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">02</p>
              <h3>La vie de prière</h3>
              <p class="tiny muted mb-0">Prier simplement, avec constance, en toute saison.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">03</p>
              <h3>La transformation</h3>
              <p class="tiny muted mb-0">Passer de l'émotion du moment à un changement durable.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Photographies officielles</p>
            <h2>Le Prophète en images</h2>
          </div>
          <div class="galerie-portraits">
            <img src="assets/img/prophete-portrait.jpg" alt="Portrait officiel du $pasteur"
                 width="852" height="1150" loading="lazy">
            <img src="assets/img/prophete-face.jpg" alt="Le $pasteur, portrait de face"
                 width="720" height="960" loading="lazy">
            <img src="assets/img/prophete-bras-croises.jpg" alt="Le $pasteur, bras croisés"
                 width="720" height="960" loading="lazy">
          </div>
          <div class="grille grille--2 espace-haut" style="gap:clamp(24px,4vw,48px)">
            <div class="etat-vide">
              <h3>Photos du Centre</h3>
              <p class="tiny mb-0">
                Les photographies du lieu, des cultes et des événements doivent être
                fournies en haute définition. Aucune image de substitution n'est
                utilisée.
              </p>
            </div>
            <div class="etat-vide">
              <h3>Actualités liées à ses interventions</h3>
              <p class="tiny mb-0">
                Les annonces (campagnes, conventions, conférences) seront publiées
                ici dès qu'elles seront communiquées par le secrétariat.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">$cta</div>
      </section>
    </main>
""")


CORPS_PROGRAMMES = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Nos programmes</p>
          <h1>Venez vivre un culte avec nous.</h1>
          <p class="lead">
            Chaque semaine, nous nous rassemblons pour adorer Dieu, écouter sa
            Parole et prier les uns pour les autres. Voici nos rendez-vous.
          </p>
        </div>
      </section>

      <section class="section" id="cultes">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <p class="eyebrow">Cultes réguliers</p>
              <h2>Nos horaires</h2>
              <div class="programme">
$creneaux
              </div>
              <p class="tiny muted espace-haut">
                Les horaires exacts sont communiqués par le secrétariat du Centre.
              </p>
            </div>
            <div>
              <p class="eyebrow">Nous trouver</p>
              <h2>Le lieu</h2>
              <div class="carte">
                <p class="carte__numero">Adresse</p>
                <p><strong>$adresse</strong></p>
                <p class="mb-0">Ville : <strong>$ville</strong> — $pays</p>
                <p class="tiny muted espace-haut mb-0">
                  Un plan d'accès sera publié dès que l'adresse complète sera fournie.
                </p>
              </div>
              <div class="carte espace-haut">
                <p class="carte__numero">Contact</p>
                <p class="mb-0">Téléphone : <strong>$telephone</strong></p>
                <p class="mb-0">WhatsApp : <strong>$whatsapp</strong></p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Déroulement</p>
            <h2>Comment se passe un culte</h2>
            <p class="lead">Environ deux heures, dans une atmosphère simple et respectueuse.</p>
          </div>
          <div class="grille grille--4">
            <article class="carte">
              <p class="carte__numero">1</p><h3>Accueil</h3>
              <p class="tiny muted mb-0">Vous êtes reçu à l'entrée et orienté vers une place.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">2</p><h3>Louange</h3>
              <p class="tiny muted mb-0">Un temps de chants et d'adoration, ouvert à tous.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">3</p><h3>Parole</h3>
              <p class="tiny muted mb-0">L'enseignement du message, avec des notes si vous le souhaitez.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">4</p><h3>Prière</h3>
              <p class="tiny muted mb-0">Un temps de prière personnel pour ceux qui le désirent.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Temps forts</p>
            <h2>Programmes spéciaux et événements</h2>
            <p class="lead">
              Veillées, séminaires, conférences, campagnes spirituelles : chaque
              événement aura sa fiche — titre, description, image, date, heure,
              lieu, informations pratiques, inscription si nécessaire.
            </p>
          </div>
          <div class="agenda" data-agenda hidden></div>
          <div class="etat-vide" data-agenda-vide>
            <h3>Aucune affiche publiée pour l'instant</h3>
            <p class="tiny mb-0">
              Le secrétariat publie ici les veillées, séminaires, conventions et
              campagnes, avec leur affiche, dès qu'elles sont programmées.
            </p>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(24px,4vw,48px)">
            <div class="carte">
              <h2 style="font-size:1.6rem">C'est votre première fois ?</h2>
              <ul class="liste-propre mb-0">
                <li>Venez tel que vous êtes : aucune tenue particulière n'est exigée.</li>
                <li>Arrivez dix minutes avant pour être installé sans précipitation.</li>
                <li>Signalez-vous à l'accueil si vous souhaitez être accompagné.</li>
                <li>Les enfants sont les bienvenus.</li>
              </ul>
            </div>
            <div class="carte">
              <h2 style="font-size:1.6rem">Vous souhaitez visiter le Centre ?</h2>
              <p>Signalez votre venue : l'équipe vous accueillera et vous guidera.</p>
              <a class="btn btn--primary" href="nous-rejoindre.html#visite">Je souhaite visiter</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">$cta</div>
      </section>
    </main>
""")


CORPS_ENSEIGNEMENTS = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Prédications et enseignements</p>
          <h1>Écouter, comprendre, mettre en pratique.</h1>
          <p class="lead">
            La bibliothèque des messages publiés sur la chaîne du ministère.
            Chaque vidéo se lance uniquement si vous cliquez : aucun cookie n'est
            déposé avant votre accord.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="filtres" role="search">
            <label class="sr-only" for="recherche">Rechercher une prédication</label>
            <input id="recherche" type="search" placeholder="Rechercher un titre…" data-recherche>
            <button class="puce" type="button" data-filtre="tous" aria-pressed="true">Tout</button>
$puces
            <span class="compteur-resultats" data-compteur>$total messages</span>
          </div>

          <div class="grille grille--3" data-liste>
$videos
          </div>

          <div class="etat-vide espace-haut" data-aucun-resultat hidden>
            <h3>Aucun message ne correspond</h3>
            <p class="tiny mb-0">Essayez un autre mot-clé ou revenez à « Tout ».</p>
          </div>

          <p class="section__pied">
            <a class="btn btn--primary" href="$youtube" target="_blank" rel="noopener">
              Voir toute la chaîne YouTube
            </a>
          </p>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <p class="eyebrow">Sur quoi nous enseignons</p>
              <h2>Les grands axes</h2>
              <ul class="liste-propre">
                <li><strong>L'amour de Dieu</strong> — comprendre qu'on est aimé avant d'être méritant.</li>
                <li><strong>La vie de prière</strong> — prier simplement, avec constance.</li>
                <li><strong>La croissance spirituelle</strong> — passer de l'émotion à la transformation.</li>
                <li><strong>Le service</strong> — aimer concrètement, dans la famille et au travail.</li>
              </ul>
            </div>
            <div class="encart encart--or">
              <p class="verse">
                « Ta parole est une lampe à mes pieds, et une lumière sur mon sentier. »
                <cite>Psaume 119 : 105</cite>
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">$cta</div>
      </section>
    </main>
""")


CORPS_MEDIATHEQUE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Médiathèque</p>
          <h1>Les images du ministère.</h1>
          <p class="lead">
            Les visuels ci-dessous proviennent des vidéos officielles de la chaîne
            du ministère. Les photographies du Centre, des cultes et des événements
            seront ajoutées dès qu'elles seront fournies.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="filtres">
            <button class="puce" type="button" data-filtre="tous" aria-pressed="true">Tout</button>
$puces
            <span class="compteur-resultats" data-compteur>$total visuels</span>
          </div>

          <div class="galerie" data-liste>
$galerie
          </div>

          <div class="section__entete espace-haut">
            <p class="eyebrow">Affiches</p>
            <h2>Affiches des veillées et événements</h2>
          </div>
          <div class="galerie" data-affiches hidden></div>

          <div class="etat-vide espace-haut">
            <h3>Albums photographiques à venir</h3>
            <p class="tiny mb-0">
              Cultes, séminaires, conférences, veillées, actions sociales : chaque
              album sera publié après l'accord des personnes photographiées.
            </p>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete section__entete--centre">
            <h2>Chaque image a une origine vérifiable</h2>
            <p class="lead">
              Aucune photographie de substitution n'est utilisée sur ce site. Une
              image affichée ici provient soit d'une vidéo du ministère, soit d'un
              fichier fourni par le Centre.
            </p>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">$cta</div>
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


CORPS_TEMOIGNAGES = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Témoignages</p>
          <h1>Ce que Dieu a fait mérite d'être raconté.</h1>
          <p class="lead">
            Guérison, délivrance, provision, restauration familiale : partagez ce
            que vous avez vécu. Chaque témoignage est lu, vérifié, puis validé par
            l'équipe avant publication.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <h2>Partager mon témoignage</h2>
              <form class="formulaire" data-mailto="$email" data-api="temoignage" data-sujet="Témoignage — site du Centre">
                <div class="champ--duo">
                  <div class="champ">
                    <label for="t-nom">Nom ou pseudonyme</label>
                    <input id="t-nom" name="nom" type="text" required>
                  </div>
                  <div class="champ">
                    <label for="t-titre">Titre du témoignage</label>
                    <input id="t-titre" name="titre" type="text" required>
                  </div>
                </div>
                <div class="champ">
                  <label for="t-texte">Votre témoignage</label>
                  <textarea id="t-texte" name="texte" required minlength="40"></textarea>
                  <span class="aide">Racontez ce qui s'est passé, et ce que cela a changé pour vous.</span>
                </div>
                <div class="champ">
                  <label for="t-identite">Identité affichée</label>
                  <select id="t-identite" name="identite">
                    <option>Afficher mon nom</option>
                    <option>Afficher uniquement mon prénom</option>
                    <option>Rester anonyme</option>
                  </select>
                </div>
                <div class="champ">
                  <label style="display:flex;gap:10px;align-items:flex-start;font-weight:400">
                    <input type="checkbox" name="autorisation" required style="width:18px;height:18px;margin-top:4px;flex:0 0 auto">
                    <span class="tiny">J'autorise la publication de mon témoignage après validation par l'équipe du Centre.</span>
                  </label>
                </div>
                <div class="champ">
                  <label style="display:flex;gap:10px;align-items:flex-start;font-weight:400">
                    <input type="checkbox" name="photo" style="width:18px;height:18px;margin-top:4px;flex:0 0 auto">
                    <span class="tiny">Je souhaite joindre une photo (à ajouter en pièce jointe dans votre messagerie).</span>
                  </label>
                </div>
                <button class="btn btn--primary btn--lg" type="submit">Préparer mon message</button>
                <p class="note-formulaire" data-avis hidden role="status"></p>
                <p class="note-formulaire">
                  Aucun témoignage n'est publié automatiquement : le site ne fait
                  que préparer votre message.
                </p>
              </form>
            </div>
            <div>
              <div class="carte">
                <h3>Comment ça se passe</h3>
                <ol class="liste-propre mb-0">
                  <li>Vous envoyez votre message.</li>
                  <li>L'équipe le lit et vous contacte si besoin.</li>
                  <li>Après accord, il est publié sur cette page.</li>
                </ol>
              </div>
              <div class="encart encart--or espace-haut">
                <p class="verse">
                  « Revenez à votre maison, et racontez tout ce que Dieu a fait pour vous. »
                  <cite>Luc 8 : 39</cite>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Ils ont témoigné</p>
            <h2>Témoignages publiés</h2>
          </div>
          <div class="grille grille--2" data-temoignages hidden></div>
          <div class="etat-vide" data-temoignages-vide>
            <h3>Aucun témoignage publié pour l'instant</h3>
            <p class="tiny mb-0">
              Les témoignages validés apparaîtront ici, avec l'identité choisie par
              chacun. Rien n'est publié sans accord explicite.
            </p>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">$cta</div>
      </section>
    </main>
""")


CORPS_PRIERE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Demande de prière</p>
          <h1>Déposez ce qui pèse sur votre cœur.</h1>
          <p class="lead">
            Santé, famille, travail, mariage, études, finances : écrivez-nous.
            Une personne de l'équipe pastorale priera pour votre intention.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <h2>Écrire une demande</h2>
              <form class="formulaire" data-mailto="$email" data-api="priere" data-sujet="Demande de prière — site du Centre">
                <div class="champ--duo">
                  <div class="champ">
                    <label for="p-nom">Nom ou pseudonyme</label>
                    <input id="p-nom" name="nom" type="text" required>
                  </div>
                  <div class="champ">
                    <label for="p-contact">E-mail ou téléphone <span class="aide">(facultatif)</span></label>
                    <input id="p-contact" name="contact" type="text">
                  </div>
                </div>
                <div class="champ">
                  <label for="p-categorie">Catégorie</label>
                  <select id="p-categorie" name="categorie">
                    <option>Famille</option>
                    <option>Santé</option>
                    <option>Travail</option>
                    <option>Mariage</option>
                    <option>Études et concours</option>
                    <option>Finances</option>
                    <option>Vie spirituelle</option>
                    <option>Autre situation</option>
                  </select>
                </div>
                <div class="champ">
                  <label for="p-sujet">Sujet de prière</label>
                  <input id="p-sujet" name="sujet" type="text" placeholder="En quelques mots" required>
                </div>
                <div class="champ">
                  <label for="p-message">Votre demande</label>
                  <textarea id="p-message" name="message" required></textarea>
                </div>
                <div class="champ">
                  <label for="p-confidentialite">Confidentialité</label>
                  <select id="p-confidentialite" name="confidentialite">
                    <option>Strictement confidentielle (équipe pastorale uniquement)</option>
                    <option>Peut être partagée en réunion de prière, sans mon nom</option>
                  </select>
                </div>
                <div class="champ">
                  <label style="display:flex;gap:10px;align-items:flex-start;font-weight:400">
                    <input type="checkbox" name="consentement" required style="width:18px;height:18px;margin-top:4px;flex:0 0 auto">
                    <span class="tiny">J'accepte que ces informations soient transmises à l'équipe pastorale pour être priées.</span>
                  </label>
                </div>
                <button class="btn btn--primary btn--lg" type="submit">Préparer mon message</button>
                <p class="note-formulaire" data-avis hidden role="status"></p>
                <p class="note-formulaire">
                  Ce formulaire ouvre votre messagerie avec le message pré-rempli :
                  rien n'est stocké sur le site.
                </p>
              </form>
            </div>
            <div>
              <div class="carte">
                <h3>Ce que devient votre demande</h3>
                <ul class="liste-propre mb-0">
                  <li>Elle est lue par une personne de l'équipe pastorale.</li>
                  <li>Elle n'est jamais publiée ni rendue publique.</li>
                  <li>Elle n'est pas partagée sans votre accord.</li>
                  <li>Vous pouvez demander sa suppression à tout moment.</li>
                </ul>
              </div>
              <div class="encart encart--or espace-haut">
                <p class="verse">
                  « Ne vous inquiétez de rien ; mais en toute chose faites connaître
                  vos besoins à Dieu par des prières et des supplications, avec des
                  actions de grâces. »
                  <cite>Philippiens 4 : 6</cite>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--ink">
        <div class="wrap">
          <div class="section__entete section__entete--centre">
            <h2>La prière n'est pas un dernier recours.</h2>
            <p class="lead">
              Elle est le premier geste de celui qui choisit de faire confiance à Dieu.
            </p>
          </div>
        </div>
      </section>
    </main>
""")


CORPS_REJOINDRE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Nous rejoindre</p>
          <h1>Venir au Centre.</h1>
          <p class="lead">
            Adresse, horaires, contacts et itinéraire : tout ce qu'il faut pour
            préparer votre première visite.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <h2>Nous trouver</h2>
              <div class="carte">
                <p class="carte__numero">Adresse officielle</p>
                <p><strong>$adresse</strong></p>
                <p class="mb-0">Quartier : <strong>$quartier</strong></p>
                <p class="mb-0">Ville : <strong>$ville</strong> — $pays</p>
              </div>
              <div class="carte espace-haut">
                <p class="carte__numero">Contact</p>
                <p class="mb-0">Téléphone : <strong>$telephone</strong></p>
                <p class="mb-0">WhatsApp : <strong>$whatsapp</strong></p>
                <p class="mb-0">E-mail : <strong><a href="mailto:$email">$email</a></strong></p>
                <p class="tiny muted espace-haut mb-0">
                  L'adresse e-mail est provisoire et sera remplacée par l'adresse officielle.
                </p>
              </div>
              <div class="carte espace-haut">
                <h3>Plan d'accès</h3>
                <p class="tiny muted">
                  Nous sommes à Cocody Rivera 2, en face de l'imprimerie DA
                  Communication.
                </p>
                <a class="btn btn--ghost" target="_blank" rel="noopener"
                   href="https://www.google.com/maps/search/?api=1&amp;query=Cocody+Rivera+2+imprimerie+DA+Communication+Abidjan">
                  Ouvrir l'itinéraire dans Google Maps
                </a>
              </div>
            </div>

            <div>
              <h2>Horaires des cultes</h2>
              <div class="programme">
$creneaux
              </div>

              <div class="carte espace-haut" id="visite">
                <h3>Je souhaite visiter le Centre</h3>
                <p class="tiny muted">
                  Laissez vos coordonnées : l'équipe vous accueillera et vous
                  indiquera le lieu exact et l'heure.
                </p>
                <form class="formulaire" data-mailto="$email" data-sujet="Je souhaite visiter le Centre">
                  <div class="champ">
                    <label for="v-nom">Nom</label>
                    <input id="v-nom" name="nom" type="text" required>
                  </div>
                  <div class="champ">
                    <label for="v-tel">Téléphone ou WhatsApp</label>
                    <input id="v-tel" name="telephone" type="tel" required>
                  </div>
                  <div class="champ">
                    <label for="v-date">Date envisagée <span class="aide">(facultatif)</span></label>
                    <input id="v-date" name="date" type="date">
                  </div>
                  <div class="champ">
                    <label for="v-nb">Nombre de personnes</label>
                    <input id="v-nb" name="personnes" type="number" min="1" value="1">
                  </div>
                  <button class="btn btn--primary" type="submit">Préparer ma demande</button>
                  <p class="note-formulaire" data-avis hidden role="status"></p>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <h2>Écrire un message</h2>
              <form class="formulaire" data-mailto="$email" data-sujet="Message depuis le site du Centre">
                <div class="champ--duo">
                  <div class="champ">
                    <label for="c-nom">Nom</label>
                    <input id="c-nom" name="nom" type="text" autocomplete="name" required>
                  </div>
                  <div class="champ">
                    <label for="c-tel">Téléphone</label>
                    <input id="c-tel" name="tel" type="tel" autocomplete="tel">
                  </div>
                </div>
                <div class="champ">
                  <label for="c-email">E-mail</label>
                  <input id="c-email" name="email" type="email" autocomplete="email" required>
                </div>
                <div class="champ">
                  <label for="c-objet">Objet</label>
                  <select id="c-objet" name="objet">
                    <option>Question sur les cultes</option>
                    <option>Demande de visite</option>
                    <option>Accompagnement pastoral</option>
                    <option>Faire un don</option>
                    <option>Autre</option>
                  </select>
                </div>
                <div class="champ">
                  <label for="c-msg">Message</label>
                  <textarea id="c-msg" name="message" required></textarea>
                </div>
                <button class="btn btn--primary btn--lg" type="submit">Préparer mon message</button>
                <p class="note-formulaire" data-avis hidden role="status"></p>
              </form>
            </div>
            <div>
              <div class="carte">
                <h3>Nous écrire sur les réseaux</h3>
                <p class="tiny muted mb-0">Facebook : $facebook</p>
                <p class="tiny muted mb-0">Instagram : $instagram</p>
                <p class="tiny muted mb-0">TikTok : $tiktok</p>
                <p class="tiny muted mb-0">YouTube : <a href="$youtube" target="_blank" rel="noopener">chaîne du ministère</a></p>
              </div>
              <div class="encart encart--or espace-haut">
                <p class="verse">
                  « Car là où deux ou trois sont assemblés en mon nom, je suis au
                  milieu d'eux. »
                  <cite>Matthieu 18 : 20</cite>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
""")


CORPS_DONS = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Soutenir l'œuvre</p>
          <h1>Donner, c'est participer.</h1>
          <p class="lead">
            Vos dons soutiennent les cultes, les actions sociales et
            l'accompagnement des personnes. Chaque contribution a un usage concret.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--3">
            <article class="carte">
              <div class="carte__icone" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M11 18.5h2"/></svg>
              </div>
              <h3>Mobile Money</h3>
              <p class="tiny muted">Le numéro marchand du Centre sera publié ici.</p>
              <p class="tiny mb-0"><strong>$mobilemoney</strong></p>
            </article>
            <article class="carte">
              <div class="carte__icone carte__icone--or" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 9.5 12 4l9 5.5"/><path d="M5 10v7m4-7v7m6-7v7m4-7v7"/><path d="M3 20h18"/></svg>
              </div>
              <h3>Virement bancaire</h3>
              <p class="tiny muted">Les coordonnées bancaires officielles seront ajoutées.</p>
              <p class="tiny mb-0"><strong>$iban</strong></p>
            </article>
            <article class="carte">
              <div class="carte__icone" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 21s-7-4.6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.4-7 10-7 10Z"/></svg>
              </div>
              <h3>Sur place</h3>
              <p class="tiny muted">Une urne est disponible lors des cultes.</p>
              <p class="tiny mb-0"><strong>À chaque culte</strong></p>
            </article>
          </div>

          <div class="encart espace-haut">
            <h3>À quoi servent vos dons</h3>
            <ul class="liste-propre mb-0">
              <li>Le fonctionnement des cultes et des activités de l'église.</li>
              <li>L'accompagnement des personnes en difficulté.</li>
              <li>Les actions sociales et les projets du Centre.</li>
            </ul>
          </div>

          <div class="etat-vide espace-haut">
            <h3>Le paiement en ligne n'est pas encore activé</h3>
            <p class="tiny mb-0">
              Un paiement Mobile Money en ligne exige un compte marchand auprès d'un
              prestataire agréé et une vérification de la transaction côté serveur.
              Tant que ce dispositif n'est pas en place, ce site n'encaisse rien et
              n'enregistre aucune donnée bancaire.
            </p>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="align-items:center;gap:clamp(24px,4vw,48px)">
            <div class="encart encart--or" style="background:var(--surface)">
              <p class="verse">
                « Que chacun donne comme il l'a résolu en son cœur, sans tristesse
                ni contrainte ; car Dieu aime celui qui donne avec joie. »
                <cite>2 Corinthiens 9 : 7</cite>
              </p>
            </div>
            <div>
              <h2 style="font-size:1.7rem">Une question sur les dons ?</h2>
              <p class="muted">
                Pour un reçu, un don affecté à un projet ou une précision sur les
                moyens de paiement, contactez le secrétariat.
              </p>
              <a class="btn btn--ghost" href="nous-rejoindre.html">Contacter le secrétariat</a>
            </div>
          </div>
        </div>
      </section>
    </main>
""")


CORPS_CONFIDENTIALITE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Données personnelles</p>
          <h1>Politique de confidentialité</h1>
          <p class="lead">Dernière mise à jour : 31 octobre 2026.</p>
        </div>
      </section>

      <section class="section">
        <div class="wrap wrap--narrow">
          <h2>1. Responsable du traitement</h2>
          <p>
            <strong>$nom_maj</strong> — $adresse, $ville ($pays).
            Contact : <a href="mailto:$email">$email</a>.
          </p>

          <h2>2. Ce que ce site collecte</h2>
          <p>
            Ce site est un site de présentation. Il ne crée aucun compte, ne dépose
            aucun cookie de mesure d'audience et n'enregistre aucune donnée dans une
            base de données.
          </p>
          <ul class="liste-propre">
            <li>
              <strong>Formulaires.</strong> Les informations saisies (nom, contact,
              sujet, message) ne sont pas transmises à un serveur : elles servent à
              composer un message dans votre propre logiciel de messagerie. Vous
              décidez de l'envoyer.
            </li>
            <li>
              <strong>Demandes de prière.</strong> Une fois reçues par courriel,
              elles sont traitées de manière confidentielle, ne sont jamais publiées
              et ne servent à aucune fin publicitaire.
            </li>
            <li>
              <strong>Témoignages.</strong> Aucun témoignage n'est publié sans
              autorisation explicite et sans validation préalable.
            </li>
            <li>
              <strong>Polices de caractères.</strong> Le site charge des polices
              depuis Google Fonts : votre adresse IP est alors transmise à ce
              service. Un hébergement local des polices peut supprimer cet appel.
            </li>
            <li>
              <strong>Vidéos.</strong> Les lecteurs YouTube ne sont chargés qu'après
              un clic. Avant ce clic, aucune requête n'est faite vers YouTube.
            </li>
          </ul>

          <h2>3. Durées de conservation</h2>
          <p>
            Les demandes de prière et les messages reçus par courriel sont conservés
            le temps du suivi pastoral, puis supprimés sur demande. Les témoignages
            refusés ne sont pas conservés.
          </p>

          <h2>4. Vos droits</h2>
          <p>
            Vous pouvez demander l'accès, la rectification ou la suppression des
            informations vous concernant en écrivant à
            <a href="mailto:$email">$email</a>. Une réponse est apportée dans les
            meilleurs délais.
          </p>

          <h2>5. Sécurité</h2>
          <p>
            Les données sensibles (prière, situation personnelle) ne sont ni
            publiées, ni partagées, ni utilisées à des fins commerciales. L'accès est
            réservé aux personnes habilitées du Centre.
          </p>

          <h2>6. Hébergement</h2>
          <p class="tiny muted">
            L'hébergeur du site doit être renseigné ici (nom, adresse, contact) une
            fois le déploiement effectué.
          </p>
        </div>
      </section>
    </main>
""")


CORPS_LEGAL = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">Informations légales</p>
          <h1>Mentions légales</h1>
          <p class="lead">Dernière mise à jour : 31 octobre 2026.</p>
        </div>
      </section>

      <section class="section">
        <div class="wrap wrap--narrow">
          <h2>Éditeur du site</h2>
          <p>
            <strong>$nom_maj</strong><br>
            Adresse : $adresse<br>
            $ville — $pays<br>
            Téléphone : $telephone<br>
            E-mail : <a href="mailto:$email">$email</a>
          </p>
          <p>Responsable de la publication : <strong>$pasteur</strong>, pasteur du Centre.</p>
          <p class="tiny muted">
            Les mentions d'identification légale (numéro d'enregistrement, statut
            associatif ou cultuel) doivent être complétées par le Centre.
          </p>

          <h2>Données personnelles</h2>
          <p>
            Le traitement des données est décrit dans la
            <a href="confidentialite.html">politique de confidentialité</a>.
          </p>

          <h2>Propriété intellectuelle</h2>
          <p>
            Les textes, visuels et éléments graphiques de ce site sont la propriété
            du $nom, sauf mention contraire. Les vidéos restent la propriété de leurs
            auteurs et sont diffusées depuis la chaîne officielle du ministère.
          </p>

          <h2>Hébergement</h2>
          <p class="tiny muted">
            L'hébergeur du site doit être renseigné ici (nom, adresse, contact) une
            fois le déploiement effectué.
          </p>

          <h2>Litiges</h2>
          <p>
            Le présent site est soumis au droit ivoirien. En cas de difficulté, une
            solution amiable sera recherchée avant toute action contentieuse.
          </p>
        </div>
      </section>
    </main>
""")


CORPS_404 = Template("""    <main id="contenu">
      <section class="section" style="min-height:60vh;display:grid;align-items:center">
        <div class="wrap wrap--narrow centre">
          <p class="eyebrow" style="justify-content:center">Erreur 404</p>
          <h1>Cette page n'existe pas.</h1>
          <p class="lead" style="margin-inline:auto">
            Le lien est peut-être ancien, ou l'adresse mal saisie. Revenez à
            l'accueil, ou écrivez-nous si vous cherchiez quelque chose de précis.
          </p>
          <div class="hero__actions" style="justify-content:center">
            <a class="btn btn--primary btn--lg" href="index.html">Retour à l'accueil</a>
            <a class="btn btn--ghost btn--lg" href="nous-rejoindre.html">Nous écrire</a>
          </div>
        </div>
      </section>
    </main>
""")


CORPS_FICHE = Template("""    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
$fil
          <p class="eyebrow">$genre · $date</p>
          <h1>$titre</h1>
          <ul class="meta-liste">
            <li>Publié le <strong>$date</strong></li>
            <li>Catégorie : <strong>$genre</strong></li>
            <li>Par <strong>$intervenant</strong></li>
          </ul>
        </div>
      </section>

      <section class="section section--serre">
        <div class="wrap">
          <div class="fiche-grille">
            <div>
              <div class="fiche-lecteur">
                <button class="lecteur" type="button" data-video="$id" data-titre="$titre_attr"
                        aria-label="Lire la vidéo : $titre_attr">
                  <img class="vignette" src="$prefixe$vignette" alt="" width="1280" height="720">
                  <span class="lecteur__voile" aria-hidden="true"></span>
                  <span class="lecteur__badge" aria-hidden="true">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                  </span>
                  <span class="lecteur__legende">Cliquer pour lire</span>
                </button>
              </div>

              <h2 class="espace-haut">À propos de ce message</h2>
              <p>
                $resume
              </p>
              <div class="etat-vide" style="text-align:left">
                <p class="tiny mb-0">
                  Le résumé détaillé et les références bibliques de ce message seront
                  rédigés par l'équipe du Centre. Ils ne sont pas générés
                  automatiquement.
                </p>
              </div>

              <h3 class="espace-haut">Partager</h3>
              <ul class="partage">
                <li><a href="https://www.facebook.com/sharer/sharer.php?u=$url_partage" target="_blank" rel="noopener">Facebook</a></li>
                <li><a href="https://wa.me/?text=$texte_partage" target="_blank" rel="noopener">WhatsApp</a></li>
                <li><button type="button" data-copier="$url_partage">Copier le lien</button></li>
              </ul>
            </div>

            <aside>
              <div class="carte">
                <h3>Fiche</h3>
                <p class="tiny muted mb-0">Titre : $titre</p>
                <p class="tiny muted mb-0">Date : $date</p>
                <p class="tiny muted mb-0">Catégorie : $genre</p>
                <p class="tiny muted mb-0">Intervenant : $intervenant</p>
                <p class="tiny muted mb-0">Source : chaîne officielle du ministère</p>
              </div>
              <div class="carte espace-haut">
                <h3>Autres messages</h3>
                <ul class="footer-liens" style="color:var(--ink-2)">
$autres
                </ul>
              </div>
            </aside>
          </div>
        </div>
      </section>
    </main>
""")


CORPS_TEMOIGNAGES_PAGE = None  # marqueur de lecture : voir PAGES


def corps_enseignements():
    puces = "\n".join(
        '            <button class="puce" type="button" data-filtre="%s" aria-pressed="false">%s</button>'
        % (g, g)
        for g in GENRES
    )
    return CORPS_ENSEIGNEMENTS.substitute(
        fil=fil("Enseignements"),
        puces=puces,
        total=len(VIDEOS),
        videos="\n".join(carte_video(v) for v in VIDEOS),
        youtube=EGLISE["youtube"],
        cta=CTA_FINAL,
    )


def corps_mediatheque():
    puces = "\n".join(
        '            <button class="puce" type="button" data-filtre="%s" aria-pressed="false">%s</button>'
        % (g, g)
        for g in GENRES
    )
    figures = []
    for v in VIDEOS:
        figures.append(
            """            <figure data-genre="%s" data-titre="%s">
              <button type="button" data-image="%s" data-legende="%s — %s">
                <img src="%s" alt="%s" width="1280" height="800" loading="lazy">
              </button>
              <figcaption>%s — %s</figcaption>
            </figure>"""
            % (
                v["genre"],
                v["titre"].replace('"', "&quot;"),
                vignette(v),
                v["genre"],
                v["date"],
                vignette(v),
                ("Vignette de la vidéo : " + v["titre"]).replace('"', "&quot;"),
                v["genre"],
                v["date"],
            )
        )
    return CORPS_MEDIATHEQUE.substitute(
        fil=fil("Médiathèque"),
        puces=puces,
        total=len(VIDEOS),
        galerie="\n".join(figures),
        cta=CTA_FINAL,
    )


# ── Instanciation des pages ───────────────────────────────────────────

def corps_accueil():
    return CORPS_ACCUEIL.substitute(
        pays=EGLISE["pays"],
        carte_culte=carte_culte(),
        videos="\n".join(carte_video(v) for v in VIDEOS[:3]),
        pasteur=PROPHETE["nom"],
        role=PROPHETE["role"],
        cta=CTA_FINAL,
    )


def blocs_valeurs():
    return "\n".join(
        """            <article class="carte">
              <p class="carte__numero">%02d</p>
              <h3>%s</h3>
              <p class="tiny muted">%s</p>
              <p class="tiny" style="color:var(--gold-ink);font-weight:600;margin-bottom:0">%s</p>
            </article>""" % (i + 1, nom, definition, reference)
        for i, (nom, definition, reference) in enumerate(VALEURS)
    )


def blocs_departements():
    out = []
    for nom, responsable, mission in DEPARTEMENTS:
        resp = (
            "Responsable : <strong>%s</strong>" % responsable
            if responsable
            else 'Responsable : %s' % m(AC, "à confirmer")
        )
        out.append(
            """            <article class="carte">
              <h3 style="font-size:1.08rem">%s</h3>
              <p class="tiny muted">%s</p>
              <p class="tiny mb-0">%s</p>
            </article>""" % (nom, mission, resp)
        )
    return "\n".join(out)


def corps_centre():
    return CORPS_CENTRE.substitute(
        fil=fil("Le Centre"),
        vision=VISION,
        mission=MISSION,
        valeurs=blocs_valeurs(),
        departements=blocs_departements(),
        adresse=EGLISE["adresse"],
        quartier=EGLISE["quartier"],
        pays=EGLISE["pays"],
        pasteur=PROPHETE["nom"],
        role=PROPHETE["role"],
        nom_maj=EGLISE["nom_maj"],
        annee=m(EGLISE["annee_fondation"], "année à confirmer"),
        ville=m(EGLISE["ville"], "ville à confirmer"),
        cta=CTA_FINAL,
    )


def corps_prophete():
    return CORPS_PROPHETE.substitute(
        fil=fil("Le Prophète"),
        pasteur=PROPHETE["nom"],
        nom_court=PROPHETE["nom_court"],
        role=PROPHETE["role"],
        youtube=EGLISE["youtube"],
        videos="\n".join(carte_video(v) for v in VIDEOS[:3]),
        cta=CTA_FINAL,
    )


def corps_programmes():
    return CORPS_PROGRAMMES.substitute(
        fil=fil("Programmes"),
        creneaux=lignes_creneaux(),
        adresse=m(EGLISE["adresse"], "adresse à confirmer"),
        ville=m(EGLISE["ville"], "ville à confirmer"),
        pays=EGLISE["pays"],
        telephone=m(EGLISE["telephone"], "téléphone à confirmer"),
        whatsapp=m(EGLISE["whatsapp"], "WhatsApp à confirmer"),
        aConfirmer=m(AC, "à confirmer"),
        cta=CTA_FINAL,
    )


def corps_temoignages():
    return CORPS_TEMOIGNAGES.substitute(
        fil=fil("Témoignages"), email=EGLISE["email"], cta=CTA_FINAL
    )


def corps_priere():
    return CORPS_PRIERE.substitute(fil=fil("Prière"), email=EGLISE["email"])


def corps_rejoindre():
    return CORPS_REJOINDRE.substitute(
        fil=fil("Nous rejoindre"),
        creneaux=lignes_creneaux(),
        adresse=m(EGLISE["adresse"], "adresse à confirmer"),
        quartier=m(EGLISE["quartier"], "quartier à confirmer"),
        ville=m(EGLISE["ville"], "ville à confirmer"),
        pays=EGLISE["pays"],
        telephone=m(EGLISE["telephone"], "téléphone à confirmer"),
        whatsapp=m(EGLISE["whatsapp"], "WhatsApp à confirmer"),
        email=EGLISE["email"],
        facebook=m(EGLISE["facebook"], "page à confirmer"),
        instagram=m(EGLISE["instagram"], "compte à confirmer"),
        tiktok=m(EGLISE["tiktok"], "compte à confirmer"),
        youtube=EGLISE["youtube"],
    )


def corps_dons():
    return CORPS_DONS.substitute(
        fil=fil("Faire un don"),
        mobilemoney=m(AC, "à confirmer"),
        iban=m(AC, "à confirmer"),
    )


def corps_confidentialite():
    return CORPS_CONFIDENTIALITE.substitute(
        fil=fil("Confidentialité"),
        nom_maj=EGLISE["nom_maj"],
        nom=EGLISE["nom"],
        adresse=m(EGLISE["adresse"], "adresse à confirmer"),
        ville=m(EGLISE["ville"], "ville à confirmer"),
        pays=EGLISE["pays"],
        email=EGLISE["email"],
    )


def corps_legal():
    return CORPS_LEGAL.substitute(
        fil=fil("Mentions légales"),
        nom=EGLISE["nom"],
        nom_maj=EGLISE["nom_maj"],
        adresse=m(EGLISE["adresse"], "adresse à confirmer"),
        ville=m(EGLISE["ville"], "ville à confirmer"),
        pays=EGLISE["pays"],
        telephone=m(EGLISE["telephone"], "téléphone à confirmer"),
        email=EGLISE["email"],
        pasteur=PROPHETE["nom"],
    )


def pages_simples():
    return [
        ("index.html", "Accueil",
         "Centre des Amoureux de Dieu — une église où la Parole est enseignée avec clarté, où la prière est une respiration et où chacun est accueilli. Cultes, prédications, prière.",
         corps_accueil(), True, None),
        ("le-centre.html", "À propos",
         "Qui nous sommes : vision, valeurs et conduite du Centre des Amoureux de Dieu.",
         corps_centre(), True, None),
        ("le-prophete.html", "Le Prophète",
         "Présentation du Prophète Daniel Jeff Adou, pasteur du Centre des Amoureux de Dieu, et de son ministère.",
         corps_prophete(), True, None),
        ("programmes.html", "Nos programmes",
         "Horaires des cultes, programmes spéciaux, événements et informations pour une première visite.",
         corps_programmes(), True, None),
        ("enseignements.html", "Prédications",
         "Bibliothèque des prédications et enseignements du Centre des Amoureux de Dieu, avec recherche et filtres.",
         corps_enseignements(), True, None),
        ("mediatheque.html", "Médiathèque",
         "Galerie des visuels du ministère : cultes, enseignements, prière, événements.",
         corps_mediatheque(), True, None),
        ("temoignages.html", "Témoignages",
         "Partager un témoignage, et consulter les témoignages validés par l'équipe du Centre.",
         corps_temoignages(), True, None),
        ("priere.html", "Prière",
         "Envoyer une demande de prière à l'équipe pastorale, en toute confidentialité.",
         corps_priere(), True, None),
        ("nous-rejoindre.html", "Nous rejoindre",
         "Venir au Centre des Amoureux de Dieu : adresse, horaires, contacts, visite et formulaire de contact.",
         corps_rejoindre(), True, None),
        ("dons.html", "Faire un don",
         "Soutenir les cultes, l'accompagnement et les actions sociales du Centre des Amoureux de Dieu.",
         corps_dons(), False, None),
        ("mentions-legales.html", "Mentions légales",
         "Mentions légales, propriété intellectuelle et hébergement du site du Centre des Amoureux de Dieu.",
         corps_legal(), False, None),
        ("confidentialite.html", "Confidentialité",
         "Politique de confidentialité : quelles données, pour quoi, combien de temps, et vos droits.",
         corps_confidentialite(), False, None),
        ("404.html", "Page introuvable",
         "La page demandée n'existe pas.",
         CORPS_404.substitute(), False, None),
    ]


def fiche(v):
    """Fiche individuelle d'une prédication (URL partageable, données structurées)."""
    autres = [
        '<li><a href="%s.html">%s</a></li>' % (a["slug"], a["titre"])
        for a in VIDEOS
        if a["id"] != v["id"]
    ][:4]
    url = "%s/predications/%s.html" % (EGLISE["site"], v["slug"])
    corps = CORPS_FICHE.substitute(
        fil=fil(v["genre"], prefixe="../"),
        titre=v["titre"],
        titre_attr=v["titre"].replace('"', "&quot;"),
        genre=v["genre"],
        date=v["date"],
        id=v["id"],
        intervenant=PROPHETE["nom"],
        prefixe="../",
        vignette=vignette(v),
        resume=(
            "Message publié le %s sur la chaîne officielle du ministère. "
            "Cette fiche rassemble la vidéo, la date de publication et les "
            "informations de référence." % v["date"]
        ),
        url_partage=url,
        texte_partage=(v["titre"] + " — " + EGLISE["nom"]).replace(" ", "%20"),
        autres="\n".join(autres),
    )
    jsonld = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": v["titre"],
        "description": "Message du %s — %s." % (v["date"], PROPHETE["nom"]),
        "uploadDate": v["iso"],
        "url": url,
        "thumbnailUrl": "%s/%s" % (EGLISE["site"], vignette(v)),
        "embedUrl": "https://www.youtube-nocookie.com/embed/%s" % v["id"],
        "publisher": {"@type": "Organization", "name": EGLISE["nom"]},
    }
    nom_complet = "%s · %s" % (v["titre"], EGLISE["nom"])
    return page_html(
        "predications/%s.html" % v["slug"],
        v["titre"],
        "%s — message du %s publié par %s." % (v["titre"], v["date"], PROPHETE["nom"]),
        corps,
        index=True,
        jsonld=jsonld,
        prefixe="../",
    )


# ══════════════════════════════════════════════════════════════════════
# 4. ÉCRITURE
# ══════════════════════════════════════════════════════════════════════

OBSOLETES = ["cultes.html", "evenements.html", "contact.html"]


def ecrire():
    ecrits = []
    for page in pages_simples():
        fichier, titre, description, corps, index, jsonld = page
        html = page_html(fichier, titre, description, corps, index=index, jsonld=jsonld)
        with open(os.path.join(RACINE, fichier), "w", encoding="utf-8") as fh:
            fh.write(html)
        ecrits.append((fichier, len(html)))

    dossier = os.path.join(RACINE, "predications")
    os.makedirs(dossier, exist_ok=True)
    for v in VIDEOS:
        html = fiche(v)
        chemin = os.path.join(dossier, "%s.html" % v["slug"])
        with open(chemin, "w", encoding="utf-8") as fh:
            fh.write(html)
        ecrits.append(("predications/%s.html" % v["slug"], len(html)))

    for nom in OBSOLETES:
        chemin = os.path.join(RACINE, nom)
        if os.path.exists(chemin):
            os.remove(chemin)
    return ecrits


def sitemap():
    entrees = []
    for fichier, _, _, _, index, _ in pages_simples():
        if not index:
            continue
        entrees.append(
            "  <url>\n    <loc>%s/%s</loc>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (EGLISE["site"], "" if fichier == "index.html" else fichier,
               "1.0" if fichier == "index.html" else "0.7")
        )
    for v in VIDEOS:
        entrees.append(
            "  <url>\n    <loc>%s/predications/%s.html</loc>\n    <lastmod>%s</lastmod>\n    <priority>0.6</priority>\n  </url>"
            % (EGLISE["site"], v["slug"], v["iso"])
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entrees)
        + "\n</urlset>\n"
    )


MOTIF_MARQUEUR = re.compile(r'<span class="a-completer"[^>]*>(.*?)</span>', re.S)


def contenu_a_completer():
    """Document PRODUIT en relisant les pages écrites : il ne peut pas mentir."""
    total = 0
    blocs = []
    fichiers = []
    for nom in sorted(os.listdir(RACINE)):
        if nom.endswith(".html"):
            fichiers.append(nom)
    dossier = os.path.join(RACINE, "predications")
    if os.path.isdir(dossier):
        fichiers += ["predications/" + f for f in sorted(os.listdir(dossier)) if f.endswith(".html")]

    for fichier in fichiers:
        with open(os.path.join(RACINE, fichier), encoding="utf-8") as fh:
            html = fh.read()
        trouves = MOTIF_MARQUEUR.findall(html)
        if not trouves:
            continue
        total += len(trouves)
        blocs.append("### `%s`\n\n%s\n" % (fichier, "\n".join("- %s" % t.strip() for t in trouves)))

    doc = """# Contenu à fournir par le Centre des Amoureux de Dieu

Fichier **généré** par `outils/generer.py` en relisant les pages réellement
produites. Il liste chaque information encore marquée « à confirmer » (fond
doré pointillé sur le site).

Total : **%d marqueurs** sur le site.

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

%s
## 4. Après réception

1. Renseigner `EGLISE` et `CRENEAUX` dans `outils/generer.py`.
2. Lancer `python3 outils/generer.py`.
3. Quand plus aucun marqueur ne subsiste, retirer `data-etat="travail"` de la
   balise `<html>` dans le gabarit `T_PAGE` pour masquer le bandeau de travail.
""" % (total, "\n".join(blocs))
    return total, doc


if __name__ == "__main__":
    resultat = ecrire()
    with open(os.path.join(RACINE, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap())
    nb, doc = contenu_a_completer()
    with open(os.path.join(RACINE, "CONTENU-A-COMPLETER.md"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("marqueurs « à confirmer » : %d" % nb)
    for nom, taille in resultat:
        print("%-46s %7d octets" % (nom, taille))
    print("%-46s %7d octets" % ("sitemap.xml", os.path.getsize(os.path.join(RACINE, "sitemap.xml"))))

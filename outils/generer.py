#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du site vitrine du CENTRE DES AMOUREUX DE DIEU.

Un seul endroit à modifier pour les informations de l'église : le dictionnaire
EGLISE ci-dessous. Les valeurs marquées A_COMPLETER sont des textes que
l'église doit fournir ; le script les enveloppe dans un marqueur visuel
(<span class="a-completer">) et les liste dans CONTENU-A-COMPLETER.md.

Usage :
    python3 outils/generer.py
"""

import json
import os
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════════════════
# 1. INFORMATIONS DE L'ÉGLISE — la seule source de vérité du site
# ══════════════════════════════════════════════════════════════════════

EGLISE = {
    "nom": "Centre des Amoureux de Dieu",
    "nom_maj": "CENTRE DES AMOUREUX DE DIEU",
    "sigle": "CAD",
    "pays": "Côte d'Ivoire",
    "ville": "A_COMPLETER",           # ex. « Abidjan »
    "quartier": "A_COMPLETER",        # ex. « Cocody, Angré »
    "adresse": "A_COMPLETER",         # adresse complète / point de repère
    "telephone": "A_COMPLETER",       # ex. « +225 07 00 00 00 00 »
    "whatsapp": "A_COMPLETER",
    "email": "contact@centre-des-amoureux.org",   # à confirmer
    "email_marque": False,            # passer à False quand l'adresse est réelle
    "youtube": "https://www.youtube.com/@jeffadou3161",
    "youtube_nom": "Prophète Daniel Jeff Adou",
    "facebook": "A_COMPLETER",
    "tiktok": "A_COMPLETER",
    "pasteur": "Prophète Daniel Jeff Adou",
    "annee_fondation": "A_COMPLETER",
    "site": "https://centre-des-amoureux.org",   # domaine à confirmer
}

CRENEAUX = [
    # (jour, intitulé, heure)  — horaires à confirmer par l'église
    ("Dimanche", "Culte d'adoration", "A_COMPLETER"),
    ("Mercredi", "Culte de la Parole", "A_COMPLETER"),
    ("Vendredi", "Nuit de prière", "A_COMPLETER"),
]

VIDEOS = [
    ("SXql767Lo7w", "10 CHOSES A SAVOIR SUR L'ONCTION ROYALE | Prophète Daniel Jeff ADOU", "16 octobre 2026", "Enseignement"),
    ("2CHnQLRtN0Y", "L'huile, le cœur et le trône", "28 septembre 2026", "Enseignement"),
    ("OlT6R0wc0JQ", "L'HUILE LE COEUR ET LE TRONE (PARTIE 1)", "22 septembre 2026", "Enseignement"),
    ("-hKzzUDnh0E", "PRIONS ENSEMBLE", "24 septembre 2026", "Prière"),
    ("jrefqSertlc", "10 CHOSES A SAVOIR SUR L'ONCTION ROYALE", "12 octobre 2026", "Enseignement"),
    ("_fldckxVCDI", "Comment reconnaître un sorcier", "12 août 2026", "Enseignement"),
    ("h8dCZFevdI8", "Service prophétique", "12 août 2026", "Culte"),
    ("Vke4iYzemIs", "Tous les grands ont d'abord rêvé grand", "17 octobre 2026", "Exhortation"),
]

NAV = [
    ("index.html", "Accueil"),
    ("le-centre.html", "Le Centre"),
    ("cultes.html", "Cultes"),
    ("enseignements.html", "Enseignements"),
    ("evenements.html", "Événements"),
    ("priere.html", "Prière"),
    ("contact.html", "Contact"),
]

# ══════════════════════════════════════════════════════════════════════
# 2. GABARITS
# ══════════════════════════════════════════════════════════════════════


def marqueur(valeur, quoi="à confirmer"):
    """Enveloppe une valeur non encore fournie par l'église."""
    if valeur == "A_COMPLETER":
        return (
            '<span class="a-completer" data-a-completer="1" '
            'title="Information à fournir par le Centre">%s</span>' % quoi
        )
    return valeur


def m(valeur, quoi="à confirmer"):
    return marqueur(valeur, quoi)


NAV_ITEMS = "\n".join(
    '          <a href="%s"%s>%s</a>'
    % (href, ' aria-current="page"' if href == "{page}" else "", libelle)
    for href, libelle in NAV
)


def entete_page(page):
    liens = []
    for href, libelle in NAV:
        actif = ' aria-current="page"' if href == page else ""
        liens.append('          <a href="%s"%s>%s</a>' % (href, actif, libelle))
    liens.append(
        '          <a class="btn btn--primary" href="dons.html">Faire un don</a>'
    )
    nav_html = "\n".join(liens)
    return """    <a class="skip" href="#contenu">Aller au contenu</a>

    <div class="bandeau-travail" role="note">
      Version de travail — les informations surlignées doivent être fournies par le Centre.
    </div>

    <header class="site-header">
      <div class="wrap">
        <a class="marque" href="index.html" aria-label="%(nom)s — accueil">
          <span class="marque__tuile" aria-hidden="true">%(sigle)s</span>
          <span class="marque__texte">
            <span class="marque__nom">%(nom)s</span>
            <span class="marque__sous">%(pays)s</span>
          </span>
        </a>

        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-principal">
          <span class="nav-toggle__barre" aria-hidden="true"></span>
          <span class="sr-only">Ouvrir le menu</span>
        </button>

        <nav class="nav" id="nav-principal" data-ouvert="false" aria-label="Navigation principale">
%(nav)s
        </nav>
      </div>
    </header>
""" % {"nom": EGLISE["nom"], "sigle": EGLISE["sigle"], "pays": EGLISE["pays"], "nav": nav_html}


def pied_page():
    return """    <footer class="site-footer">
      <div class="wrap">
        <div class="footer-grille">
          <div>
            <a class="marque" href="index.html">
              <span class="marque__tuile" aria-hidden="true">%(sigle)s</span>
              <span class="marque__texte">
                <span class="marque__nom">%(nom)s</span>
                <span class="marque__sous">%(pays)s</span>
              </span>
            </a>
            <p class="espace-haut" style="max-width:34ch">
              Une maison de prière, de Parole et d'amour fraternel, ouverte à tous.
            </p>
            <p class="tiny" style="margin-top:18px">
              <a href="https://www.youtube.com/@jeffadou3161" rel="noopener" target="_blank">
                Chaîne YouTube du ministère
              </a>
            </p>
          </div>
          <div>
            <h3>Le Centre</h3>
            <ul class="footer-liens">
              <li><a href="le-centre.html">Qui nous sommes</a></li>
              <li><a href="le-centre.html#vision">Notre vision</a></li>
              <li><a href="cultes.html">Nos cultes</a></li>
              <li><a href="evenements.html">Événements</a></li>
            </ul>
          </div>
          <div>
            <h3>Ressources</h3>
            <ul class="footer-liens">
              <li><a href="enseignements.html">Enseignements</a></li>
              <li><a href="priere.html">Demande de prière</a></li>
              <li><a href="dons.html">Faire un don</a></li>
              <li><a href="contact.html">Nous contacter</a></li>
            </ul>
          </div>
          <div>
            <h3>Nous trouver</h3>
            <ul class="footer-liens">
              <li>Ville : %(ville)s</li>
              <li>Adresse : %(adresse)s</li>
              <li>Téléphone : %(telephone)s</li>
              <li><a href="mailto:%(email)s">%(email)s</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bas">
          <p class="mb-0">© <span data-annee>2026</span> %(nom)s. Tous droits réservés.</p>
          <ul>
            <li><a href="mentions-legales.html">Mentions légales</a></li>
            <li><a href="mentions-legales.html#donnees">Données personnelles</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
      </div>
    </footer>

    <script src="assets/js/site.js" defer></script>
  </body>
</html>
""" % {
        "nom": EGLISE["nom"],
        "sigle": EGLISE["sigle"],
        "pays": EGLISE["pays"],
        "ville": m(EGLISE["ville"]),
        "adresse": m(EGLISE["adresse"]),
        "telephone": m(EGLISE["telephone"]),
        "email": EGLISE["email"],
    }


def page_html(page, titre, description, corps, og_titre=None, index=True):
    nom_complet = "%s · %s" % (titre, EGLISE["nom"]) if titre != "Accueil" else "%s · %s" % (EGLISE["nom"], "Église à " + EGLISE["pays"])
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Church",
        "name": EGLISE["nom"],
        "alternateName": EGLISE["nom_maj"],
        "description": "Église du Centre des Amoureux de Dieu — cultes, enseignements, prière et vie fraternelle.",
        "url": EGLISE["site"],
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "CI",
        },
        "sameAs": [EGLISE["youtube"]],
    }
    robots = "index,follow" if index else "noindex,follow"
    return """<!doctype html>
<html lang="fr" data-etat="travail">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>%(titre_complet)s</title>
    <meta name="description" content="%(description)s">
    <meta name="robots" content="%(robots)s">
    <meta name="theme-color" content="#ED6C10">
    <link rel="canonical" href="%(site)s/%(page)s">
    <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="assets/img/favicon.svg">

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="%(nom)s">
    <meta property="og:locale" content="fr_FR">
    <meta property="og:title" content="%(og_titre)s">
    <meta property="og:description" content="%(description)s">
    <meta property="og:url" content="%(site)s/%(page)s">
    <meta property="og:image" content="%(site)s/assets/img/partage.png">
    <meta name="twitter:card" content="summary_large_image">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
    <script type="application/ld+json">
%(jsonld)s
    </script>
  </head>
  <body>
%(entete)s
%(corps)s
%(pied)s""" % {
        "titre_complet": nom_complet,
        "description": description,
        "robots": robots,
        "site": EGLISE["site"],
        "page": page,
        "nom": EGLISE["nom"],
        "og_titre": og_titre or titre,
        "jsonld": json.dumps(jsonld, ensure_ascii=False, indent=2),
        "entete": entete_page(page),
        "corps": corps,
        "pied": pied_page(),
    }


# ══════════════════════════════════════════════════════════════════════
# 3. FRAGMENTS RÉUTILISABLES
# ══════════════════════════════════════════════════════════════════════


def carte_video(v, i=0):
    vid, titre, date, genre = v
    return """            <article class="video-carte monte">
              <div class="video-carte__media">
                <button class="lecteur" type="button" data-video="%(vid)s" data-titre="%(titre_attr)s"
                        aria-label="Lire la vidéo : %(titre_attr)s">
                  <span class="lecteur__badge" aria-hidden="true">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                  </span>
                  <span class="lecteur__legende">Cliquer pour lire</span>
                </button>
              </div>
              <div class="video-carte__corps">
                <p class="video-carte__meta">%(genre)s · %(date)s</p>
                <h3 class="video-carte__titre">%(titre)s</h3>
              </div>
            </article>""" % {
        "vid": vid,
        "titre": titre,
        "titre_attr": titre.replace('"', "&quot;"),
        "date": date,
        "genre": genre,
    }


def lignes_creneaux():
    out = []
    for jour, intitule, heure in CRENEAUX:
        out.append(
            """          <div class="programme__ligne">
            <span class="programme__jour">%(jour)s</span>
            <span class="programme__nom">%(intitule)s</span>
            <span class="programme__heure">%(heure)s</span>
          </div>"""
            % {"jour": jour, "intitule": intitule, "heure": m(heure, "à confirmer")}
        )
    return "\n".join(out)


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
            % (jour, intitule, m(heure, "à confirmer"))
        )
    return """          <aside class="carte-culte monte monte--2" aria-label="Horaires des cultes">
            <p class="carte-culte__titre">
              <span class="pastille-vie" aria-hidden="true"></span>
              Nos rendez-vous
            </p>
%s
            <div class="carte-culte__pied">
              <span>%s</span>
              <a class="link-arrow" href="cultes.html">Voir les cultes</a>
            </div>
          </aside>""" % ("\n".join(lignes), m(EGLISE["ville"], "à confirmer"))


CTA_FINAL = """      <div class="wrap">
        <div class="cta-final">
          <h2>Vous êtes attendu, tel que vous êtes.</h2>
          <p>
            Que vous veniez pour la première fois ou que vous cherchiez une maison
            spirituelle, il y a une place pour vous au Centre des Amoureux de Dieu.
          </p>
          <div class="cta-final__actions">
            <a class="btn btn--primary btn--lg" href="cultes.html">Préparer ma visite</a>
            <a class="btn btn--sur-ink btn--lg" href="priere.html">Demander une prière</a>
          </div>
        </div>
      </div>"""


# ══════════════════════════════════════════════════════════════════════
# 4. PAGES
# ══════════════════════════════════════════════════════════════════════

CORPS_ACCUEIL = """    <main id="contenu">
      <section class="hero">
        <div class="wrap">
          <div class="hero__grille">
            <div>
              <p class="eyebrow monte">Église · %(pays)s</p>
              <h1 class="monte monte--2">
                Un lieu pour <em>aimer Dieu</em>,<br>et être aimé de Lui.
              </h1>
              <p class="lead monte monte--3">
                Le Centre des Amoureux de Dieu est une famille spirituelle où la
                Parole est enseignée avec clarté, où la prière est une respiration,
                et où chacun est accueilli avec dignité.
              </p>
              <div class="hero__actions monte monte--3">
                <a class="btn btn--primary btn--lg" href="cultes.html">Venez à un culte</a>
                <a class="btn btn--ghost btn--lg" href="enseignements.html">Écouter un enseignement</a>
              </div>
              <p class="hero__note monte monte--3">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-4.6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.4-7 10-7 10Z"/></svg>
                Ouvert à tous, sans condition et sans tenue exigée. Venez comme vous êtes.
              </p>
            </div>
%(carte_culte)s
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
            <h2>Les dernières vidéos</h2>
            <p class="lead">
              Retrouvez les prédications et temps de prière publiés sur la chaîne
              du ministère, à écouter et à partager.
            </p>
          </div>
          <div class="grille grille--3">
%(videos)s
          </div>
          <p class="section__pied">
            <a class="btn btn--ghost" href="enseignements.html">Tous les enseignements</a>
          </p>
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
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
%(cta)s
        </div>
      </section>
    </main>
""" % {
    "pays": EGLISE["pays"],
    "carte_culte": carte_culte(),
    "videos": "\n".join(carte_video(v) for v in VIDEOS[:3]),
    "cta": CTA_FINAL,
}


CORPS_CENTRE = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Le Centre</span>
          </nav>
          <p class="eyebrow">Qui nous sommes</p>
          <h1>Une église, une famille, une direction.</h1>
          <p class="lead">
            Le Centre des Amoureux de Dieu est une communauté chrétienne établie
            en %(pays)s. Nous croyons qu'une église est d'abord un lieu où l'on
            apprend à aimer Dieu et à aimer les autres.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,60px)">
            <div>
              <h2>Notre raison d'être</h2>
              <p>
                Rassembler des personnes de tous horizons autour de la Parole de
                Dieu, les accompagner dans leur marche spirituelle et les rendre
                capables d'aimer Dieu et leur prochain d'un amour sincère.
              </p>
              <p>
                Concrètement : des cultes réguliers, des enseignements accessibles,
                des temps de prière, et un accompagnement humain pour les moments
                de joie comme pour les épreuves.
              </p>
            </div>
            <div class="encart">
              <p class="verse">
                « Tu aimeras le Seigneur, ton Dieu, de tout ton cœur, de toute ton
                âme, et de toute ta pensée. C'est le premier et le plus grand
                commandement. Et voici le second, qui lui est semblable : Tu aimeras
                ton prochain comme toi-même. »
                <cite>Matthieu 22 : 37-39</cite>
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt" id="vision">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">Notre vision</p>
            <h2>Ce vers quoi nous marchons</h2>
          </div>
          <div class="grille grille--3">
            <article class="carte">
              <div class="carte__icone" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3v18M6 8h12"/><path d="M12 21c3.3 0 6-2.2 6-5H6c0 2.8 2.7 5 6 5Z"/></svg>
              </div>
              <h3>Une adoration sincère</h3>
              <p class="muted">Que notre louange soit vraie, et non une habitude.</p>
            </article>
            <article class="carte">
              <div class="carte__icone carte__icone--or" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5Z"/><path d="M8 8h8M8 12h5"/></svg>
              </div>
              <h3>Une Parole comprise</h3>
              <p class="muted">Que chacun reparte avec quelque chose de clair à vivre.</p>
            </article>
            <article class="carte">
              <div class="carte__icone" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9.5" r="2.4"/><path d="M3.5 20c0-3 2.5-5.2 5.5-5.2s5.5 2.2 5.5 5.2"/><path d="M16 14.6c2.6.3 4.5 2.3 4.5 5"/></svg>
              </div>
              <h3>Une famille unie</h3>
              <p class="muted">Que personne ne traverse seul ce que Dieu lui fait vivre.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="align-items:center;gap:clamp(28px,5vw,64px)">
            <div>
              <p class="eyebrow">Le pasteur</p>
              <h2>%(pasteur)s</h2>
              <p class="lead">
                Le Centre des Amoureux de Dieu est conduit par le %(pasteur)s, dont
                l'enseignement est diffusé sur la chaîne du ministère.
              </p>
              <p>
                Sa priorité : une parole compréhensible, fidèle au texte biblique,
                qui éclaire la vie réelle des personnes — avec la conviction que ce
                que Dieu dit change concrètement une existence.
              </p>
              <a class="link-arrow" href="%(youtube)s" target="_blank" rel="noopener">
                Écouter ses enseignements
              </a>
            </div>
            <div class="carte" style="text-align:center">
              <div class="carte__icone" style="margin-inline:auto;width:76px;height:76px;border-radius:50%%;background:linear-gradient(145deg,#ED2727,#ED6C10 55%%,#EF9C19);color:#fff">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="8" r="3.6"/><path d="M4.5 20.5c0-4 3.4-6.6 7.5-6.6s7.5 2.6 7.5 6.6"/></svg>
              </div>
              <h3 style="margin-bottom:4px">%(pasteur)s</h3>
              <p class="tiny muted">Pasteur du Centre des Amoureux de Dieu</p>
              <p class="tiny muted mb-0">
                Photo à venir — une image officielle doit être fournie par le Centre.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete section__entete--centre">
            <p class="eyebrow">Repères</p>
            <h2>Quelques informations</h2>
          </div>
          <div class="grille grille--4">
            <div class="carte">
              <p class="carte__numero">Église</p>
              <p class="mb-0"><strong>%(nom_maj)s</strong></p>
            </div>
            <div class="carte">
              <p class="carte__numero">Fondation</p>
              <p class="mb-0">%(annee)s</p>
            </div>
            <div class="carte">
              <p class="carte__numero">Pays</p>
              <p class="mb-0">%(pays)s</p>
            </div>
            <div class="carte">
              <p class="carte__numero">Ville</p>
              <p class="mb-0">%(ville)s</p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
%(cta)s
        </div>
      </section>
    </main>
""" % {
    "pays": EGLISE["pays"],
    "pasteur": EGLISE["pasteur"],
    "youtube": EGLISE["youtube"],
    "nom_maj": EGLISE["nom_maj"],
    "annee": m(EGLISE["annee_fondation"], "à confirmer"),
    "ville": m(EGLISE["ville"], "à confirmer"),
    "cta": CTA_FINAL,
}


CORPS_CULTES = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Cultes</span>
          </nav>
          <p class="eyebrow">Nos rendez-vous</p>
          <h1>Venez vivre un culte avec nous.</h1>
          <p class="lead">
            Chaque semaine, nous nous rassemblons pour adorer Dieu, écouter sa
            Parole et prier les uns pour les autres. Voici comment cela se passe.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <p class="eyebrow">Programme hebdomadaire</p>
              <h2>Nos horaires</h2>
              <div class="programme">
%(creneaux)s
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
                <p><strong>%(adresse)s</strong></p>
                <p class="mb-0">Ville : <strong>%(ville)s</strong> — %(pays)s</p>
                <p class="tiny muted espace-haut mb-0">
                  Un plan d'accès sera publié dès que l'adresse complète sera fournie.
                </p>
              </div>
              <div class="carte espace-haut">
                <p class="carte__numero">Contact</p>
                <p class="mb-0">Téléphone : <strong>%(telephone)s</strong></p>
                <p class="mb-0">WhatsApp : <strong>%(whatsapp)s</strong></p>
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
              <p class="carte__numero">1</p>
              <h3>Accueil</h3>
              <p class="tiny muted mb-0">Vous êtes reçu à l'entrée et orienté vers une place.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">2</p>
              <h3>Louange</h3>
              <p class="tiny muted mb-0">Un temps de chants et d'adoration, ouvert à tous.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">3</p>
              <h3>Parole</h3>
              <p class="tiny muted mb-0">L'enseignement du message, avec des notes si vous le souhaitez.</p>
            </article>
            <article class="carte">
              <p class="carte__numero">4</p>
              <h3>Prière</h3>
              <p class="tiny muted mb-0">Un temps de prière personnel pour ceux qui le désirent.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section">
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
              <h2 style="font-size:1.6rem">Besoin d'un accompagnement ?</h2>
              <p>
                Une visite, une écoute, une prière pour un sujet précis : l'équipe
                pastorale peut vous recevoir.
              </p>
              <a class="btn btn--primary" href="contact.html">Prendre contact</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
%(cta)s
        </div>
      </section>
    </main>
""" % {
    "creneaux": lignes_creneaux(),
    "adresse": m(EGLISE["adresse"], "à confirmer"),
    "ville": m(EGLISE["ville"], "à confirmer"),
    "pays": EGLISE["pays"],
    "telephone": m(EGLISE["telephone"], "à confirmer"),
    "whatsapp": m(EGLISE["whatsapp"], "à confirmer"),
    "cta": CTA_FINAL,
}


CORPS_ENSEIGNEMENTS = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Enseignements</span>
          </nav>
          <p class="eyebrow">La Parole enseignée</p>
          <h1>Écouter, comprendre, mettre en pratique.</h1>
          <p class="lead">
            Les messages et temps de prière publiés sur la chaîne du ministère.
            Chaque vidéo se lance uniquement si vous cliquez : aucun cookie n'est
            déposé avant votre accord.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--3">
%(videos)s
          </div>
          <p class="section__pied">
            <a class="btn btn--primary" href="%(youtube)s" target="_blank" rel="noopener">
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
        <div class="wrap">
%(cta)s
        </div>
      </section>
    </main>
""" % {
    "videos": "\n".join(carte_video(v) for v in VIDEOS),
    "youtube": EGLISE["youtube"],
    "cta": CTA_FINAL,
}


CORPS_EVENEMENTS = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Événements</span>
          </nav>
          <p class="eyebrow">Vie de l'église</p>
          <h1>Les prochains rendez-vous.</h1>
          <p class="lead">
            Retraites, veillées, conventions, actions sociales : les temps forts
            du Centre des Amoureux de Dieu sont annoncés ici.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="section__entete">
            <p class="eyebrow">À venir</p>
            <h2>Calendrier</h2>
          </div>
          <div class="grille grille--2">
            <article class="carte">
              <p class="carte__numero">Dimanche — chaque semaine</p>
              <h3>Culte d'adoration</h3>
              <p class="muted mb-0">
                Rendez-vous hebdomadaire de l'assemblée. Horaire :
                %(heure1)s.
              </p>
            </article>
            <article class="carte">
              <p class="carte__numero">Mercredi — chaque semaine</p>
              <h3>Culte de la Parole</h3>
              <p class="muted mb-0">
                Enseignement au milieu de la semaine. Horaire :
                %(heure2)s.
              </p>
            </article>
            <article class="carte">
              <p class="carte__numero">Vendredi — chaque semaine</p>
              <h3>Nuit de prière</h3>
              <p class="muted mb-0">
                Temps d'intercession. Horaire : %(heure3)s.
              </p>
            </article>
            <article class="carte" style="border-style:dashed">
              <p class="carte__numero">Temps forts</p>
              <h3>Les événements ponctuels</h3>
              <p class="muted mb-0">
                Le calendrier des événements exceptionnels sera publié ici dès
                qu'il sera communiqué par le secrétariat.
              </p>
            </article>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:center">
            <div>
              <p class="eyebrow">Ne rien manquer</p>
              <h2>Rester informé</h2>
              <p class="lead">
                Les annonces de dernière minute sont diffusées sur la chaîne du
                ministère. Les réseaux sociaux du Centre seront ajoutés ici.
              </p>
              <a class="btn btn--primary" href="%(youtube)s" target="_blank" rel="noopener">
                Suivre sur YouTube
              </a>
            </div>
            <div class="carte">
              <h3>Suivez-nous</h3>
              <p class="tiny muted">Facebook : %(facebook)s</p>
              <p class="tiny muted mb-0">TikTok : %(tiktok)s</p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
%(cta)s
        </div>
      </section>
    </main>
""" % {
    "heure1": m(CRENEAUX[0][2], "à confirmer"),
    "heure2": m(CRENEAUX[1][2], "à confirmer"),
    "heure3": m(CRENEAUX[2][2], "à confirmer"),
    "youtube": EGLISE["youtube"],
    "facebook": m(EGLISE["facebook"], "à confirmer"),
    "tiktok": m(EGLISE["tiktok"], "à confirmer"),
    "cta": CTA_FINAL,
}


CORPS_PRIERE = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Prière</span>
          </nav>
          <p class="eyebrow">Prière</p>
          <h1>Déposez ce qui pèse sur votre cœur.</h1>
          <p class="lead">
            Santé, famille, travail, direction de vie, action de grâce : écrivez-nous.
            Une personne de l'équipe pastorale priera pour votre intention.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <h2>Écrire une demande</h2>
              <form class="formulaire" data-mailto="%(email)s" data-sujet="Demande de prière — site du Centre">
                <div class="champ--duo">
                  <div class="champ">
                    <label for="prenom">Prénom</label>
                    <input id="prenom" name="prenom" type="text" autocomplete="given-name" required>
                  </div>
                  <div class="champ">
                    <label for="contact">Téléphone ou e-mail <span class="aide">(facultatif)</span></label>
                    <input id="contact" name="contact" type="text" autocomplete="email">
                  </div>
                </div>
                <div class="champ">
                  <label for="sujet">Sujet de prière</label>
                  <input id="sujet" name="sujet" type="text" placeholder="En quelques mots" required>
                </div>
                <div class="champ">
                  <label for="message">Votre message</label>
                  <textarea id="message" name="message" required></textarea>
                  <span class="aide">Vous pouvez écrire librement. Rien n'est publié.</span>
                </div>
                <div class="champ">
                  <label for="confidentialite">Confidentialité</label>
                  <select id="confidentialite" name="confidentialite">
                    <option>Demande confidentielle (équipe pastorale uniquement)</option>
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
                  <li>Elle n'est ni publiée, ni partagée sans votre accord.</li>
                  <li>Vous pouvez demander qu'elle soit supprimée à tout moment.</li>
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
""" % {"email": EGLISE["email"]}


CORPS_CONTACT = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Contact</span>
          </nav>
          <p class="eyebrow">Contact</p>
          <h1>Parlons-nous.</h1>
          <p class="lead">
            Une question sur les cultes, une demande de visite, un besoin
            d'accompagnement : écrivez-nous ou appelez le secrétariat.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="wrap">
          <div class="grille grille--2" style="gap:clamp(28px,5vw,56px);align-items:start">
            <div>
              <h2>Nous joindre</h2>
              <div class="grille" style="gap:14px">
                <div class="carte">
                  <p class="carte__numero">Adresse</p>
                  <p class="mb-0"><strong>%(adresse)s</strong></p>
                  <p class="mb-0">Ville : %(ville)s — %(pays)s</p>
                </div>
                <div class="carte">
                  <p class="carte__numero">Téléphone / WhatsApp</p>
                  <p class="mb-0"><strong>%(telephone)s</strong></p>
                  <p class="mb-0">WhatsApp : <strong>%(whatsapp)s</strong></p>
                </div>
                <div class="carte">
                  <p class="carte__numero">E-mail</p>
                  <p class="mb-0"><strong><a href="mailto:%(email)s">%(email)s</a></strong></p>
                  <p class="tiny muted mb-0">Adresse provisoire, à confirmer par le Centre.</p>
                </div>
              </div>
            </div>
            <div>
              <h2>Écrire un message</h2>
              <form class="formulaire" data-mailto="%(email)s" data-sujet="Message depuis le site du Centre">
                <div class="champ--duo">
                  <div class="champ">
                    <label for="nom">Nom</label>
                    <input id="nom" name="nom" type="text" autocomplete="name" required>
                  </div>
                  <div class="champ">
                    <label for="tel">Téléphone</label>
                    <input id="tel" name="tel" type="tel" autocomplete="tel">
                  </div>
                </div>
                <div class="champ">
                  <label for="email-exp">E-mail</label>
                  <input id="email-exp" name="email" type="email" autocomplete="email" required>
                </div>
                <div class="champ">
                  <label for="objet">Objet</label>
                  <select id="objet" name="objet">
                    <option>Question sur les cultes</option>
                    <option>Demande de visite</option>
                    <option>Accompagnement pastoral</option>
                    <option>Faire un don</option>
                    <option>Autre</option>
                  </select>
                </div>
                <div class="champ">
                  <label for="msg">Message</label>
                  <textarea id="msg" name="message" required></textarea>
                </div>
                <button class="btn btn--primary btn--lg" type="submit">Préparer mon message</button>
                <p class="note-formulaire" data-avis hidden role="status"></p>
              </form>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="wrap">
          <div class="section__entete section__entete--centre">
            <h2>Venir au Centre</h2>
            <p class="lead">
              Un plan d'accès interactif sera intégré dès que l'adresse exacte
              sera communiquée.
            </p>
          </div>
        </div>
      </section>
    </main>
""" % {
    "adresse": m(EGLISE["adresse"], "à confirmer"),
    "ville": m(EGLISE["ville"], "à confirmer"),
    "pays": EGLISE["pays"],
    "telephone": m(EGLISE["telephone"], "à confirmer"),
    "whatsapp": m(EGLISE["whatsapp"], "à confirmer"),
    "email": EGLISE["email"],
}


CORPS_DONS = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Faire un don</span>
          </nav>
          <p class="eyebrow">Soutenir l'œuvre</p>
          <h1>Donner, c'est participer.</h1>
          <p class="lead">
            Vos dons soutiennent les cultes, les actions sociales et
            l'accompagnement des personnes. Chaque contribution, quelle que soit
            sa taille, a un usage concret.
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
              <p class="tiny mb-0"><strong>%(mm)s</strong></p>
            </article>
            <article class="carte">
              <div class="carte__icone carte__icone--or" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 9.5 12 4l9 5.5"/><path d="M5 10v7m4-7v7m6-7v7m4-7v7"/><path d="M3 20h18"/></svg>
              </div>
              <h3>Virement bancaire</h3>
              <p class="tiny muted">Les coordonnées bancaires officielles seront ajoutées.</p>
              <p class="tiny mb-0"><strong>%(iban)s</strong></p>
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

          <p class="note-formulaire espace-haut">
            Aucun paiement en ligne n'est encaissé par ce site : il n'enregistre
            aucune donnée bancaire.
          </p>
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
              <a class="btn btn--ghost" href="contact.html">Contacter le secrétariat</a>
            </div>
          </div>
        </div>
      </section>
    </main>
""" % {
    "mm": m("A_COMPLETER", "à confirmer"),
    "iban": m("A_COMPLETER", "à confirmer"),
}


CORPS_LEGAL = """    <main id="contenu">
      <section class="entete-page">
        <div class="wrap wrap--narrow">
          <nav class="fil" aria-label="Fil d'Ariane">
            <a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Mentions légales</span>
          </nav>
          <p class="eyebrow">Informations légales</p>
          <h1>Mentions légales</h1>
          <p class="lead">Dernière mise à jour : %(date)s.</p>
        </div>
      </section>

      <section class="section">
        <div class="wrap wrap--narrow">
          <h2>Éditeur du site</h2>
          <p>
            <strong>%(nom_maj)s</strong><br>
            Adresse : %(adresse)s<br>
            %(ville)s — %(pays)s<br>
            Téléphone : %(telephone)s<br>
            E-mail : <a href="mailto:%(email)s">%(email)s</a>
          </p>
          <p>
            Responsable de la publication : <strong>%(pasteur)s</strong>, pasteur du Centre.
          </p>
          <p class="tiny muted">
            Les mentions d'identification légale (numéro d'enregistrement,
            statut associatif ou cultuel) doivent être complétées par le Centre.
          </p>

          <h2 id="donnees">Données personnelles</h2>
          <p>
            Ce site est un site de présentation. Il ne crée aucun compte, ne
            dépose aucun cookie de mesure d'audience et n'enregistre aucune
            donnée dans une base.
          </p>
          <ul class="liste-propre">
            <li>
              <strong>Formulaires de contact et de prière.</strong> Les informations
              que vous saisissez ne sont pas envoyées à un serveur : elles servent
              à composer un message dans votre propre logiciel de messagerie. Vous
              décidez de l'envoyer ou non.
            </li>
            <li>
              <strong>Demandes de prière.</strong> Une fois reçues par l'équipe
              pastorale, elles sont traitées de manière confidentielle et ne sont
              ni publiées ni transmises à des tiers.
            </li>
            <li>
              <strong>Vidéos.</strong> Les lecteurs YouTube ne sont chargés qu'après
              un clic. Avant ce clic, aucun contenu ni cookie de YouTube n'est
              sollicité. Après lecture, les règles de confidentialité de YouTube
              s'appliquent.
            </li>
            <li>
              <strong>Polices de caractères.</strong> Le site charge des polices
              depuis Google Fonts ; votre adresse IP est alors transmise à ce
              service. Une hébergement local des polices peut être mis en place
              pour supprimer cet appel.
            </li>
          </ul>
          <p>
            Pour exercer un droit d'accès, de rectification ou de suppression,
            écrivez à <a href="mailto:%(email)s">%(email)s</a>.
          </p>

          <h2>Propriété intellectuelle</h2>
          <p>
            Les textes, visuels et éléments graphiques de ce site sont la propriété
            du %(nom)s, sauf mention contraire. Les vidéos restent la propriété de
            leurs auteurs et sont diffusées depuis la chaîne officielle du ministère.
          </p>

          <h2>Hébergement</h2>
          <p class="tiny muted">
            L'hébergeur du site doit être renseigné ici (nom, adresse, contact) une
            fois le déploiement effectué.
          </p>

          <h2>Litiges</h2>
          <p>
            Le présent site est soumis au droit ivoirien. En cas de difficulté,
            une solution amiable sera recherchée avant toute action contentieuse.
          </p>
        </div>
      </section>
    </main>
""" % {
    "date": "31 octobre 2026",
    "nom": EGLISE["nom"],
    "nom_maj": EGLISE["nom_maj"],
    "adresse": m(EGLISE["adresse"], "à confirmer"),
    "ville": m(EGLISE["ville"], "à confirmer"),
    "pays": EGLISE["pays"],
    "telephone": m(EGLISE["telephone"], "à confirmer"),
    "email": EGLISE["email"],
    "pasteur": EGLISE["pasteur"],
}


CORPS_404 = """    <main id="contenu">
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
            <a class="btn btn--ghost btn--lg" href="contact.html">Nous écrire</a>
          </div>
        </div>
      </section>
    </main>
"""


PAGES = [
    (
        "index.html",
        "Accueil",
        "Centre des Amoureux de Dieu — une église où la Parole est enseignée avec clarté, où la prière est une respiration et où chacun est accueilli. Cultes, enseignements et demande de prière.",
        CORPS_ACCUEIL,
        True,
    ),
    (
        "le-centre.html",
        "Le Centre",
        "Qui nous sommes : vision, valeurs et conduite du Centre des Amoureux de Dieu.",
        CORPS_CENTRE,
        True,
    ),
    (
        "cultes.html",
        "Cultes",
        "Horaires des cultes, déroulement d'un culte et informations pour une première visite au Centre des Amoureux de Dieu.",
        CORPS_CULTES,
        True,
    ),
    (
        "enseignements.html",
        "Enseignements",
        "Les enseignements et temps de prière du Centre des Amoureux de Dieu, à écouter depuis la chaîne officielle du ministère.",
        CORPS_ENSEIGNEMENTS,
        True,
    ),
    (
        "evenements.html",
        "Événements",
        "Les rendez-vous et temps forts du Centre des Amoureux de Dieu.",
        CORPS_EVENEMENTS,
        True,
    ),
    (
        "priere.html",
        "Prière",
        "Envoyer une demande de prière à l'équipe pastorale du Centre des Amoureux de Dieu, en toute confidentialité.",
        CORPS_PRIERE,
        True,
    ),
    (
        "contact.html",
        "Contact",
        "Contacter le Centre des Amoureux de Dieu : adresse, téléphone, e-mail et formulaire.",
        CORPS_CONTACT,
        True,
    ),
    (
        "dons.html",
        "Faire un don",
        "Soutenir les cultes, l'accompagnement et les actions sociales du Centre des Amoureux de Dieu.",
        CORPS_DONS,
        False,
    ),
    (
        "mentions-legales.html",
        "Mentions légales",
        "Mentions légales, données personnelles et propriété intellectuelle du site du Centre des Amoureux de Dieu.",
        CORPS_LEGAL,
        False,
    ),
    (
        "404.html",
        "Page introuvable",
        "La page demandée n'existe pas.",
        CORPS_404,
        False,
    ),
]


# ══════════════════════════════════════════════════════════════════════
# 5. ÉCRITURE
# ══════════════════════════════════════════════════════════════════════


def ecrire():
    ecrits = []
    for fichier, titre, description, corps, index in PAGES:
        html = page_html(fichier, titre, description, corps, index=index)
        chemin = os.path.join(RACINE, fichier)
        with open(chemin, "w", encoding="utf-8") as fh:
            fh.write(html)
        ecrits.append((fichier, len(html)))
    return ecrits


def sitemap():
    entrees = []
    for fichier, _, _, _, index in PAGES:
        if not index:
            continue
        entrees.append(
            "  <url>\n    <loc>%s/%s</loc>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (
                EGLISE["site"],
                "" if fichier == "index.html" else fichier,
                "1.0" if fichier == "index.html" else "0.7",
            )
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'
        + "\n".join(entrees)
        + "\n</urlset>\n"
    ).replace("http://www.sitemap.org/schemas/sitemap/0.9", "http://www.sitemaps.org/schemas/sitemap/0.9")


def contenu_a_completer():
    """Liste les informations que l'église doit encore fournir.

    Le document est PRODUIT en relisant les pages générées : il ne peut donc
    pas annoncer un état différent de ce que le site affiche réellement.
    """
    import re

    motif = re.compile(r'<span class="a-completer"[^>]*>(.*?)</span>', re.S)
    total = 0
    blocs = []
    for fichier, _, _, _, _ in PAGES:
        if fichier == "404.html":
            continue
        with open(os.path.join(RACINE, fichier), encoding="utf-8") as fh:
            html = fh.read()
        trouves = motif.findall(html)
        if not trouves:
            continue
        total += len(trouves)
        blocs.append(
            "### `%s`\n\n%s\n" % (fichier, "\n".join("- %s" % t.strip() for t in trouves))
        )
    return total, """# Contenu à fournir par le Centre des Amoureux de Dieu

Ce fichier est **généré automatiquement** par `outils/generer.py` à partir des
pages réellement produites. Il liste chaque information encore marquée
« à confirmer » sur le site (fond doré pointillé).

Total : **%(total)d marqueurs** sur le site.

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

%(blocs)s
## 4. Comment remplacer

1. Ouvrir `outils/generer.py` et renseigner le dictionnaire `EGLISE`
   (et la liste `CRENEAUX` pour les horaires).
2. Lancer `python3 outils/generer.py`.
3. Les 10 pages et ce fichier sont régénérés. Quand plus aucun marqueur ne
   subsiste, retirer l'attribut `data-etat="travail"` de la balise `<html>`
   (dans la fonction `page_html`) pour masquer le bandeau de travail.
""" % {"total": total, "blocs": "\n".join(blocs)}


if __name__ == "__main__":
    resultat = ecrire()
    with open(os.path.join(RACINE, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap())
    nb, doc = contenu_a_completer()
    with open(os.path.join(RACINE, "CONTENU-A-COMPLETER.md"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("marqueurs « à confirmer » : %d" % nb)
    for nom, taille in resultat:
        print("%-26s %7d octets" % (nom, taille))
    print("%-26s %7d octets" % ("sitemap.xml", os.path.getsize(os.path.join(RACINE, "sitemap.xml"))))

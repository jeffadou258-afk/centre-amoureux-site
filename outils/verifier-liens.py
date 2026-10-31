#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification des liens du site du Centre des Amoureux de Dieu.

Contrôle trois choses, et sort en code 1 si l'une échoue :
  1. chaque lien interne (href, src) pointe vers un fichier réellement présent ;
  2. chaque ancre interne (#id) existe dans la page de destination ;
  3. les balises titre/description/canonical sont présentes et uniques.

Les liens externes sont listés mais non bloquants : une panne réseau ne doit
pas faire échouer un contrôle de contenu.
"""

import os
import re
import sys
from urllib.parse import urlparse

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sorted(f for f in os.listdir(RACINE) if f.endswith(".html"))

erreurs = []
liens_externes = set()
total_liens = 0


def ids_de(chemin):
    try:
        with open(chemin, encoding="utf-8") as fh:
            return set(re.findall(r'\sid="([^"]+)"', fh.read()))
    except OSError:
        return set()


for page in PAGES:
    chemin = os.path.join(RACINE, page)
    with open(chemin, encoding="utf-8") as fh:
        html = fh.read()

    # Balises obligatoires
    for balise, motif in (
        ("<title>", r"<title>.+?</title>"),
        ('<meta name="description"', r'<meta name="description" content="[^"]{20,}"'),
        ('<link rel="canonical"', r'<link rel="canonical" href="[^"]+"'),
        ('lang="fr"', r'<html lang="fr"'),
    ):
        if not re.search(motif, html, re.S):
            erreurs.append("%s : balise absente ou vide — %s" % (page, balise))

    if html.count("<h1") != 1:
        erreurs.append("%s : %d balise(s) <h1> (exactement 1 attendue)" % (page, html.count("<h1")))

    # Liens
    for attr, valeur in re.findall(r'\s(href|src)="([^"]+)"', html):
        total_liens += 1
        if valeur.startswith(("http://", "https://", "mailto:", "data:")):
            if valeur.startswith("http"):
                liens_externes.add(valeur)
            continue
        if valeur.startswith("#"):
            if valeur[1:] and valeur[1:] not in ids_de(chemin):
                erreurs.append("%s : ancre interne absente %s" % (page, valeur))
            continue
        cible, _, ancre = valeur.partition("#")
        if not cible:
            continue
        destination = os.path.join(RACINE, cible)
        if not os.path.exists(destination):
            erreurs.append("%s : cible introuvable %s (attribut %s)" % (page, cible, attr))
            continue
        if ancre and ancre not in ids_de(destination):
            erreurs.append("%s : ancre #%s absente de %s" % (page, ancre, cible))

# Fichiers indispensables
for obligatoire in (
    "index.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "assets/css/style.css",
    "assets/js/site.js",
    "assets/img/favicon.svg",
    "assets/img/partage.png",
):
    if not os.path.exists(os.path.join(RACINE, obligatoire)):
        erreurs.append("fichier indispensable absent : %s" % obligatoire)

print("Pages contrôlées      : %d" % len(PAGES))
print("Liens contrôlés       : %d" % total_liens)
print("Domaines externes     : %d" % len({urlparse(u).netloc for u in liens_externes}))
for domaine in sorted({urlparse(u).netloc for u in liens_externes}):
    print("  · %s" % domaine)
print("")

if erreurs:
    print("ÉCHECS (%d) :" % len(erreurs))
    for e in erreurs:
        print("  - %s" % e)
    sys.exit(1)

print("Aucun lien interne cassé, aucune ancre manquante, balises complètes.")

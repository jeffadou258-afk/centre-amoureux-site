#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle de contraste WCAG du site du Centre des Amoureux de Dieu.

Deux règles :
  1. le moteur de calcul est AUTO-TESTÉ sur des valeurs publiées avant usage ;
  2. on mesure les paires RÉELLEMENT utilisées (fond composité compris), et
     le script sort en code 1 si une paire de texte passe sous 4,5:1, ou une
     paire d'interface sous 3:1.

Les paires étiquetées « logo » sont exemptées par la norme (1.4.3 s'applique
au texte, pas aux logotypes) — elles restent affichées pour information.
"""

import sys

# ── Moteur ────────────────────────────────────────────────────────────────


def srgb(composante):
    c = composante / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexa):
    hexa = hexa.lstrip("#")
    r, g, b = (int(hexa[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


def ratio(c1, c2):
    l1, l2 = luminance(c1), luminance(c2)
    clair, sombre = max(l1, l2), min(l1, l2)
    return (clair + 0.05) / (sombre + 0.05)


def composer(hexa_avant, alpha, hexa_arriere):
    """Couleur résultante d'un aplat translucide sur un fond (sRGB non linéaire)."""
    av = hexa_avant.lstrip("#")
    ar = hexa_arriere.lstrip("#")
    sortie = []
    for i in (0, 2, 4):
        a = int(av[i : i + 2], 16)
        b = int(ar[i : i + 2], 16)
        sortie.append(round(a * alpha + b * (1 - alpha)))
    return "#%02X%02X%02X" % tuple(sortie)


# ── 1. Auto-test du moteur ────────────────────────────────────────────────

REFERENCES = [
    ("#000000", "#FFFFFF", 21.00),
    ("#777777", "#FFFFFF", 4.48),
    ("#767676", "#FFFFFF", 4.54),
]
for a, b, attendu in REFERENCES:
    obtenu = round(ratio(a, b), 2)
    if abs(obtenu - attendu) > 0.02:
        sys.exit(
            "ÉCHEC DE L'AUTO-TEST : %s/%s = %.2f attendu %.2f — tableau invalide."
            % (a, b, obtenu, attendu)
        )
print("Auto-test du moteur : 3/3 références exactes (21.00 · 4.48 · 4.54)")

# ── 2. Jetons du site (assets/css/style.css) ─────────────────────────────

NUIT = "#1B0F0A"
BRAISE = "#2B1710"
FEU = "#C4500A"
FEU_SURVOL = "#A84308"
OR = "#F2B544"
OR_PALE = "#F7D58C"
LIN = "#FBF6EF"
SABLE = "#F3E7D6"
ENCRE = "#22140E"
CENDRE = "#6B564C"
FEU_TEXTE = "#A5470A"
SUR_NUIT = "#F4E9DC"
SUR_NUIT_2 = "#C9B5A6"
BLANC = "#FFFFFF"
BORD_CHAMP = "#8A776D"

# (libellé, avant, arrière, seuil, exempté)
PAIRES = [
    ("texte sur lin", ENCRE, LIN, 4.5, None),
    ("texte atténué sur lin", CENDRE, LIN, 4.5, None),
    ("texte atténué sur sable", CENDRE, SABLE, 4.5, None),
    ("lien feu sur lin", FEU_TEXTE, LIN, 4.5, None),
    ("lien feu sur sable", FEU_TEXTE, SABLE, 4.5, None),
    ("texte sur blanc (champs)", ENCRE, BLANC, 4.5, None),
    ("bouton : blanc sur feu", BLANC, FEU, 4.5, None),
    ("bouton survolé : blanc sur feu foncé", BLANC, FEU_SURVOL, 4.5, None),
    ("texte clair sur nuit", SUR_NUIT, NUIT, 4.5, None),
    ("texte secondaire sur nuit", SUR_NUIT_2, NUIT, 4.5, None),
    ("texte secondaire sur braise", SUR_NUIT_2, BRAISE, 4.5, None),
    ("or sur nuit", OR, NUIT, 4.5, None),
    ("or pâle sur nuit", OR_PALE, NUIT, 4.5, None),
    ("or sur braise", OR, BRAISE, 4.5, None),
    ("bordure de champ sur blanc", BORD_CHAMP, BLANC, 3.0, None),
]



def evaluer(paires, titre):
    echecs = exempts = 0
    print("\n%s" % titre)
    print("%-44s %8s %6s  %s" % ("PAIRE", "RATIO", "SEUIL", "ÉTAT"))
    print("-" * 78)
    for libelle, avant, arriere, seuil, exemption in paires:
        r = ratio(avant, arriere)
        if exemption:
            etat = "exempté (%s)" % exemption
            exempts += 1
        elif r + 1e-9 >= seuil:
            etat = "conforme"
        else:
            etat = "ÉCHEC"
            echecs += 1
        print("%-44s %8.2f %6.1f  %s" % (libelle, r, seuil, etat))
    print("-" * 78)
    print(
        "%d paires · %d conformes · %d exemptées · %d échecs"
        % (len(paires), len(paires) - echecs - exempts, exempts, echecs)
    )
    return echecs


total_echecs = evaluer(PAIRES, "SITE (feu, or et lin)")
print("")
if total_echecs:
    print("ÉCHEC GLOBAL : %d paire(s) sous le seuil." % total_echecs)
sys.exit(1 if total_echecs else 0)

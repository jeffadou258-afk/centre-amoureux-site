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

# ── 2. Jetons du site ────────────────────────────────────────────────────

BRAND = "#ED6C10"
BRAND2 = "#EF9C19"
BRAND3 = "#ED2727"
BRAND_INK = "#A64C0B"
GOLD_INK = "#8D5C0F"
RED_INK = "#C52020"
INK = "#171717"
INK2 = "#3A3A3A"
MUTED = "#666666"
PAPER = "#FFFCF8"
SURFACE = "#FFFFFF"
SURFACE2 = "#F5F5F5"

TINT_BRAND_SUR_PAPIER = composer(BRAND, 0.10, PAPER)
TINT_BRAND_SUR_BLANC = composer(BRAND, 0.10, SURFACE)
TINT_GOLD_SUR_PAPIER = composer(BRAND2, 0.14, PAPER)
TINT_INK_SUR_PAPIER = composer(INK, 0.06, PAPER)

# (libellé, avant, arrière, seuil, exempté)
PAIRES = [
    # Texte courant sur fond clair
    ("texte principal sur papier", INK, PAPER, 4.5, None),
    ("texte principal sur blanc", INK, SURFACE, 4.5, None),
    ("texte secondaire sur papier", INK2, PAPER, 4.5, None),
    ("texte atténué sur papier", MUTED, PAPER, 4.5, None),
    ("texte atténué sur blanc", MUTED, SURFACE, 4.5, None),
    ("texte atténué sur gris clair", MUTED, SURFACE2, 4.5, None),
    ("texte atténué sur carte grise", MUTED, SURFACE2, 4.5, None),
    # Accents en texte
    ("lien orange sur papier", BRAND_INK, PAPER, 4.5, None),
    ("lien orange sur blanc", BRAND_INK, SURFACE, 4.5, None),
    ("orange sur pastille 10 % sur papier", BRAND_INK, TINT_BRAND_SUR_PAPIER, 4.5, None),
    ("orange sur pastille 10 % sur blanc", BRAND_INK, TINT_BRAND_SUR_BLANC, 4.5, None),
    ("doré sur papier", GOLD_INK, PAPER, 4.5, None),
    ("doré sur gris clair", GOLD_INK, SURFACE2, 4.5, None),
    ("doré sur pastille or", GOLD_INK, TINT_GOLD_SUR_PAPIER, 4.5, None),
    ("rouge sur papier", RED_INK, PAPER, 4.5, None),
    # Boutons et surfaces de marque
    ("encre sur bouton orange", INK, BRAND, 4.5, None),
    ("encre sur bouton doré", INK, BRAND2, 4.5, None),
    ("blanc sur bouton noir", SURFACE, INK, 4.5, None),
    ("blanc sur bandeau noir", SURFACE, INK, 4.5, None),
    # Sections sombres
    ("texte 82 % sur noir", composer("#FFFFFF", 0.82, INK), INK, 4.5, None),
    ("texte 78 % sur noir (pied)", composer("#FFFFFF", 0.78, INK), INK, 4.5, None),
    ("texte 62 % sur noir (mentions)", composer("#FFFFFF", 0.62, INK), INK, 4.5, None),
    ("lien doré sur noir", BRAND2, INK, 4.5, None),
    ("sous-titre doré sur noir", BRAND2, INK, 4.5, None),
    # Interfaces (3:1)
    ("bordure de champ sur papier", "#8A8A8A", PAPER, 3.0, None),
    ("bordure de champ sur blanc", "#8A8A8A", SURFACE, 3.0, None),
    ("bordure de bouton secondaire", "#8A8A8A", PAPER, 3.0, None),
    ("anneau de focus orange", BRAND_INK, PAPER, 3.0, None),
    ("pastille de titre de section", BRAND_INK, TINT_INK_SUR_PAPIER, 3.0, None),
    # Décor : bordures de carte et séparateurs, exemptés (ce ne sont pas des composants)
    ("bordure décorative de carte", "#D5C9B8", PAPER, 3.0, "décor"),
    ("séparateur décoratif", "#E6DED2", PAPER, 3.0, "décor"),
    # Logotype : exempté (1.4.3 ne couvre pas les logotypes)
    ("monogramme blanc sur dégradé", "#FFFFFF", BRAND, 4.5, "logo"),
    ("monogramme blanc sur or", "#FFFFFF", BRAND2, 4.5, "logo"),
]

echecs = 0
exempts = 0
print("\n%-44s %8s %6s  %s" % ("PAIRE", "RATIO", "SEUIL", "ÉTAT"))
print("-" * 78)
for libelle, avant, arriere, seuil, exemption in PAIRES:
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
    "%d paires mesurées · %d conformes · %d exemptées · %d échecs"
    % (len(PAIRES), len(PAIRES) - echecs - exempts, exempts, echecs)
)
sys.exit(1 if echecs else 0)

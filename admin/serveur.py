#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Administration du site du Centre des Amoureux de Dieu.

Petit serveur autonome (bibliothèque standard uniquement) qui permet au
secrétariat de :
  · publier les affiches des veillées et des événements (avec image) ;
  · recevoir et traiter les demandes de prière ;
  · valider ou refuser les témoignages.

Chaque enregistrement modifie la base SQLite locale (admin/donnees/admin.db)
puis RÉÉCRIT les fichiers JSON lus par le site public
(assets/data/agenda.json, affiches.json, temoignages.json). Le site reste donc
statique et déployable n'importe où ; seul ce serveur doit tourner quelque part
de persistent (VPS, Render, Fly…).

Sécurité : mot de passe haché (PBKDF2), session signée en HMAC dans un cookie
HttpOnly + SameSite=Strict, jeton CSRF sur chaque formulaire, validation des
types d'image par signature binaire, aucune écriture hors des dossiers prévus.

Usage :
    python3 admin/serveur.py                 # http://127.0.0.1:4400
    python3 admin/serveur.py --port 4401
    python3 admin/serveur.py --motdepasse '…'  # définir le mot de passe
"""

import argparse
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import sqlite3
import sys
import time
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, unquote

RACINE_SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_ADMIN = os.path.join(RACINE_SITE, "admin")
DOSSIER_DONNEES = os.path.join(DOSSIER_ADMIN, "donnees")
DOSSIER_AFFICHES = os.path.join(RACINE_SITE, "assets", "img", "affiches")
DOSSIER_EXPORT = os.path.join(RACINE_SITE, "assets", "data")
BASE = os.path.join(DOSSIER_DONNEES, "admin.db")
FICHIER_SECRET = os.path.join(DOSSIER_ADMIN, ".session-secret")

MAX_UPLOAD = 4 * 1024 * 1024          # 4 Mo par affiche
TYPES_IMAGE = {
    b"\xff\xd8\xff": "jpg",
    b"\x89PNG\r\n\x1a\n": "png",
    b"RIFF": "webp",                   # vérifié plus bas (RIFF + WEBP)
}
FORMATS_ACCEPTES = ("jpg", "jpeg", "png", "webp")

DROITS_DEFAUT = dict(
    nom="Administrateur",
    email="",
)


# ══════════════════════════════════════════════════════════════════════
# 1. BASE ET SÉCURITÉ
# ══════════════════════════════════════════════════════════════════════

def connexion():
    base = sqlite3.connect(BASE)
    base.row_factory = sqlite3.Row
    base.execute("PRAGMA foreign_keys = ON")
    return base


def initialiser():
    os.makedirs(DOSSIER_DONNEES, exist_ok=True)
    os.makedirs(DOSSIER_AFFICHES, exist_ok=True)
    os.makedirs(DOSSIER_EXPORT, exist_ok=True)
    with connexion() as base:
        base.executescript("""
        create table if not exists utilisateur (
          id integer primary key check (id = 1),
          identifiant text not null,
          empreinte text not null,
          sel text not null,
          maj_le text not null
        );
        create table if not exists affiches (
          id integer primary key autoincrement,
          titre text not null,
          categorie text not null default 'Veillée',
          date_iso text,
          heure text,
          lieu text,
          description text,
          image text,
          cree_le text not null
        );
        create table if not exists prieres (
          id integer primary key autoincrement,
          nom text,
          contact text,
          categorie text,
          sujet text,
          message text not null,
          confidentialite text,
          statut text not null default 'nouvelle',
          cree_le text not null
        );
        create table if not exists temoignages (
          id integer primary key autoincrement,
          nom text,
          identite text,
          titre text,
          texte text not null,
          statut text not null default 'en_attente',
          cree_le text not null
        );
        """)


def secret_session():
    if not os.path.exists(FICHIER_SECRET):
        with open(FICHIER_SECRET, "w", encoding="utf-8") as fh:
            fh.write(secrets.token_hex(32))
        os.chmod(FICHIER_SECRET, 0o600)
    with open(FICHIER_SECRET, encoding="utf-8") as fh:
        return fh.read().strip()


def hacher(motdepasse, sel=None):
    sel = sel or secrets.token_hex(16)
    empreinte = hashlib.pbkdf2_hmac("sha256", motdepasse.encode(), sel.encode(), 240_000)
    return empreinte.hex(), sel


def verifier(motdepasse, empreinte, sel):
    essai, _ = hacher(motdepasse, sel)
    return hmac.compare_digest(essai, empreinte)


def definir_motdepasse(motdepasse):
    empreinte, sel = hacher(motdepasse)
    with connexion() as base:
        base.execute(
            "insert into utilisateur (id, identifiant, empreinte, sel, maj_le) "
            "values (1, 'admin', ?, ?, ?) "
            "on conflict(id) do update set empreinte=excluded.empreinte, sel=excluded.sel, maj_le=excluded.maj_le",
            (empreinte, sel, horodatage()),
        )


def utilisateur_existe():
    with connexion() as base:
        return base.execute("select 1 from utilisateur where id = 1").fetchone() is not None


def horodatage():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Session : jeton signé « expire|nonce » ────────────────────────────

DUREE_SESSION = 12 * 3600


def creer_session():
    nonce = secrets.token_hex(12)
    expiration = int(time.time()) + DUREE_SESSION
    charge = "%d|%s" % (expiration, nonce)
    signature = hmac.new(secret_session().encode(), charge.encode(), hashlib.sha256).hexdigest()
    return "%s|%s" % (charge, signature)


def session_valide(valeur):
    if not valeur or valeur.count("|") != 2:
        return False
    expiration, nonce, signature = valeur.split("|")
    charge = "%s|%s" % (expiration, nonce)
    attendu = hmac.new(secret_session().encode(), charge.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, attendu):
        return False
    try:
        return int(expiration) > time.time()
    except ValueError:
        return False


# ══════════════════════════════════════════════════════════════════════
# 2. EXPORT VERS LE SITE PUBLIC
# ══════════════════════════════════════════════════════════════════════

def _ecrire_json(nom, donnees):
    chemin = os.path.join(DOSSIER_EXPORT, nom)
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(donnees, fh, ensure_ascii=False, indent=2)


def exporter():
    """Réécrit les trois fichiers lus par le site. Appelé après chaque écriture."""
    with connexion() as base:
        affiches = [dict(r) for r in base.execute(
            "select id, titre, categorie, date_iso, heure, lieu, description, image "
            "from affiches order by coalesce(date_iso,'9999') asc, id desc")]
        publiables = [dict(r) for r in base.execute(
            "select id, nom, identite, titre, texte, cree_le from temoignages "
            "where statut = 'publie' order by id desc")]
    _ecrire_json("agenda.json", {"maj": horodatage(), "elements": affiches})
    _ecrire_json("affiches.json", {"maj": horodatage(), "elements": [
        {"id": a["id"], "titre": a["titre"], "categorie": a["categorie"],
         "date_iso": a["date_iso"], "image": a["image"]} for a in affiches if a["image"]
    ]})
    _ecrire_json("temoignages.json", {"maj": horodatage(), "elements": publiables})


# ══════════════════════════════════════════════════════════════════════
# 3. RENDU DES PAGES
# ══════════════════════════════════════════════════════════════════════

def e(texte):
    return html.escape(str(texte if texte is not None else ""))


def date_lisible(iso):
    if not iso:
        return "Date à préciser"
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        return iso
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
            "août", "septembre", "octobre", "novembre", "décembre"]
    return "%d %s %d" % (d.day, mois[d.month - 1], d.year)


STYLE = """
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:Inter,system-ui,sans-serif;background:#fbf8f4;color:#171717;font-size:15px;line-height:1.6}
a{color:#a64c0b}
header.top{background:#171717;color:#fff;padding:14px 22px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
header.top a{color:#f3e7d8;text-decoration:none;font-weight:600;font-size:.9rem;padding:6px 12px;border-radius:999px}
header.top a.actif,header.top a:hover{background:rgba(255,255,255,.14);color:#fff}
header.top .espace{margin-left:auto}
main{max-width:1080px;margin:0 auto;padding:28px 22px 70px}
h1{font-size:1.55rem;margin:0 0 6px}
h2{font-size:1.15rem;margin:26px 0 12px}
.sous{color:#666;margin:0 0 22px;font-size:.92rem}
.carte{background:#fff;border:1px solid #e6ded2;border-radius:14px;padding:18px 20px;margin-bottom:14px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
label{display:block;font-weight:600;font-size:.85rem;margin:12px 0 5px}
input,textarea,select{width:100%;font:inherit;padding:10px 12px;border:1.5px solid #8a8a8a;border-radius:10px;background:#fff}
textarea{min-height:96px}
button{font:inherit;font-weight:600;padding:11px 20px;border-radius:999px;border:0;background:#ed6c10;color:#171717;cursor:pointer;margin-top:14px}
button:hover{filter:brightness(1.05)}
button.discret{background:#fff;border:1.5px solid #8a8a8a;color:#3a3a3a}
button.danger{background:#fff;border:1.5px solid #c52020;color:#c52020}
form.inline{display:inline-block;margin:0}
.tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:3px 9px;border-radius:999px;background:rgba(237,108,16,.12);color:#a64c0b}
.tag.vert{background:rgba(22,101,52,.12);color:#166534}
.tag.gris{background:rgba(23,23,23,.07);color:#3a3a3a}
.message{padding:12px 16px;border-radius:10px;background:#fdf3e6;border:1px solid #ed6c10;margin-bottom:16px}
.message.ok{background:#eef7f0;border-color:#166534}
.affiche-vignette{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:10px;background:#eee}
table{width:100%;border-collapse:collapse;font-size:.9rem}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid #eee}
th{font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:#666}
"""


def page(titre, corps, actif=""):
    liens = [
        ("/", "Tableau de bord"),
        ("/affiches", "Affiches & événements"),
        ("/prieres", "Demandes de prière"),
        ("/temoignages", "Témoignages"),
    ]
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' class="actif"' if h == actif else "", e(l))
        for h, l in liens
    )
    return """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s · Administration du Centre</title>
<style>%s</style></head>
<body>
<header class="top">
  <strong style="font-size:.95rem">Administration · Centre des Amoureux de Dieu</strong>
  %s
  <span class="espace"></span>
  <a href="/site" target="_blank">Voir le site</a>
  <a href="/deconnexion">Déconnexion</a>
</header>
<main>%s</main>
</body></html>""" % (e(titre), STYLE, nav, corps)


def page_connexion(message=""):
    return """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Connexion · Administration</title>
<style>%s
body{display:grid;place-items:center;min-height:100vh;background:#171717}
.boite{background:#fff;border-radius:18px;padding:34px;width:min(400px,92vw)}
</style></head>
<body>
<form class="boite" method="post" action="/connexion">
  <h1>Administration</h1>
  <p class="sous">Centre des Amoureux de Dieu</p>
  %s
  <label for="identifiant">Identifiant</label>
  <input id="identifiant" name="identifiant" value="admin" autocomplete="username" required>
  <label for="motdepasse">Mot de passe</label>
  <input id="motdepasse" name="motdepasse" type="password" autocomplete="current-password" required>
  <button type="submit">Se connecter</button>
</form>
</body></html>""" % (STYLE, ('<div class="message">%s</div>' % e(message)) if message else "")


# ══════════════════════════════════════════════════════════════════════
# 4. VUES
# ══════════════════════════════════════════════════════════════════════

def jeton_csrf(valeur_session):
    return hmac.new(secret_session().encode(), ("csrf:" + valeur_session).encode(),
                    hashlib.sha256).hexdigest()[:32]


def vue_tableau(base, session):
    nb_affiches = base.execute("select count(*) c from affiches").fetchone()["c"]
    nb_nouvelles = base.execute("select count(*) c from prieres where statut='nouvelle'").fetchone()["c"]
    nb_prieres = base.execute("select count(*) c from prieres").fetchone()["c"]
    nb_attente = base.execute("select count(*) c from temoignages where statut='en_attente'").fetchone()["c"]
    prochaines = base.execute(
        "select * from affiches where coalesce(date_iso,'') >= date('now') order by date_iso asc limit 4"
    ).fetchall()
    jeton = jeton_csrf(session)

    lignes = "".join(
        """<div class="carte" style="display:flex;gap:16px;align-items:center">
             <div style="flex:1">
               <span class="tag">%s</span>
               <div style="font-weight:600;margin-top:6px">%s</div>
               <div class="sous" style="margin:2px 0 0">%s %s</div>
             </div>
             <form class="inline" method="post" action="/affiches/supprimer">
               <input type="hidden" name="csrf" value="%s">
               <input type="hidden" name="id" value="%s">
               <button class="danger" type="submit">Retirer</button>
             </form>
           </div>""" % (e(a["categorie"]), e(a["titre"]), e(date_lisible(a["date_iso"])), e(a["heure"] or ""), jeton, a["id"])
        for a in prochaines
    ) or '<div class="carte sous">Aucune affiche à venir pour le moment.</div>'

    return page("Tableau de bord", """
      <h1>Tableau de bord</h1>
      <p class="sous">Tout ce que vous publiez ici apparaît sur le site public.</p>
      <div class="grille">
        <div class="carte"><div class="sous">Affiches publiées</div><div style="font-size:2rem;font-weight:700">%d</div></div>
        <div class="carte"><div class="sous">Demandes de prière</div><div style="font-size:2rem;font-weight:700">%d</div><div class="sous">%d nouvelle(s)</div></div>
        <div class="carte"><div class="sous">Témoignages à valider</div><div style="font-size:2rem;font-weight:700">%d</div></div>
      </div>
      <h2>Prochaines affiches</h2>
      %s
      <h2>Ajouter</h2>
      <p class="sous">Les affiches se publient depuis « Affiches & événements ». Les demandes de prière arrivent dans « Demandes de prière ».</p>
      <a href="/affiches"><button type="button">Publier une affiche</button></a>
    """ % (nb_affiches, nb_prieres, nb_nouvelles, nb_attente, lignes), actif="/")


def vue_affiches(base, session, message="", erreur=""):
    jeton = jeton_csrf(session)
    affiches = base.execute("select * from affiches order by coalesce(date_iso,'9999') asc").fetchall()
    cartes = "".join(
        """<div class="carte">
             %s
             <div style="font-weight:600;margin-top:10px">%s</div>
             <div class="sous" style="margin:2px 0 8px">%s · %s · %s</div>
             <form class="inline" method="post" action="/affiches/supprimer">
               <input type="hidden" name="csrf" value="%s">
               <input type="hidden" name="id" value="%s">
               <button class="danger" type="submit">Supprimer</button>
             </form>
           </div>""" % (
            ('<img class="affiche-vignette" src="../%s" alt="">' % e(a["image"])) if a["image"] else
            '<div class="affiche-vignette" style="display:grid;place-items:center;color:#999">sans image</div>',
            e(a["titre"]), e(date_lisible(a["date_iso"])), e(a["heure"] or "heure à préciser"),
            e(a["lieu"] or "lieu à préciser"), jeton, a["id"])
        for a in affiches
    ) or '<div class="carte sous">Aucune affiche pour le moment.</div>'

    return page("Affiches & événements", """
      <h1>Affiches &amp; événements</h1>
      <p class="sous">Publiez l'affiche d'une veillée, d'un séminaire, d'une convention. Elle apparaît immédiatement sur le site.</p>
      %s %s
      <div class="carte">
        <h2 style="margin-top:0">Nouvelle affiche</h2>
        <form method="post" action="/affiches" enctype="multipart/form-data">
          <input type="hidden" name="csrf" value="%s">
          <label for="titre">Titre</label>
          <input id="titre" name="titre" required placeholder="Veillée de prière — La puissance du nom de Jésus">
          <label for="categorie">Catégorie</label>
          <select id="categorie" name="categorie">
            <option>Veillée</option><option>Convention</option><option>Séminaire</option>
            <option>Campagne</option><option>Concert</option><option>Action sociale</option><option>Autre</option>
          </select>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label for="date_iso">Date</label><input id="date_iso" name="date_iso" type="date"></div>
            <div><label for="heure">Heure</label><input id="heure" name="heure" placeholder="19h00 – 22h00"></div>
          </div>
          <label for="lieu">Lieu</label>
          <input id="lieu" name="lieu" value="Cocody Rivera 2, en face de l'imprimerie DA Communication">
          <label for="description">Description</label>
          <textarea id="description" name="description" placeholder="Thème, intervenant, informations pratiques…"></textarea>
          <label for="image">Affiche (JPG, PNG ou WEBP — 4 Mo maximum)</label>
          <input id="image" name="image" type="file" accept="image/jpeg,image/png,image/webp">
          <button type="submit">Publier l'affiche</button>
        </form>
      </div>
      <h2>Affiches en ligne (%d)</h2>
      <div class="grille">%s</div>
    """ % (
        ('<div class="message ok">%s</div>' % e(message)) if message else "",
        ('<div class="message">%s</div>' % e(erreur)) if erreur else "",
        jeton, len(affiches), cartes), actif="/affiches")


def vue_prieres(base, session, message=""):
    jeton = jeton_csrf(session)
    lignes = []
    for p in base.execute("select * from prieres order by id desc limit 200"):
        statut = {"nouvelle": "tag", "traitee": "tag vert"}.get(p["statut"], "tag gris")
        lignes.append("""<div class="carte">
          <span class="%s">%s</span> <span class="tag gris">%s</span>
          <div style="font-weight:600;margin-top:8px">%s</div>
          <div class="sous" style="margin:2px 0 10px">%s · %s · %s</div>
          <p style="margin:0 0 10px">%s</p>
          <form class="inline" method="post" action="/prieres/statut">
            <input type="hidden" name="csrf" value="%s"><input type="hidden" name="id" value="%s">
            <input type="hidden" name="statut" value="%s">
            <button class="discret" type="submit">%s</button>
          </form>
          <form class="inline" method="post" action="/prieres/supprimer">
            <input type="hidden" name="csrf" value="%s"><input type="hidden" name="id" value="%s">
            <button class="danger" type="submit">Supprimer</button>
          </form>
        </div>""" % (
            statut, e(p["statut"]), e(p["categorie"] or "sans catégorie"),
            e(p["nom"] or "Anonyme"), e(p["contact"] or "sans contact"),
            e(p["confidentialite"] or "confidentiel"), e(p["cree_le"][:10]),
            e(p["message"]), jeton, p["id"],
            "traitee" if p["statut"] == "nouvelle" else "nouvelle",
            "Marquer comme traitée" if p["statut"] == "nouvelle" else "Rouvrir",
            jeton, p["id"]))

    return page("Demandes de prière", """
      <h1>Demandes de prière</h1>
      <p class="sous">Ces demandes ne sont jamais publiées sur le site. Elles restent dans cette administration.</p>
      %s
      %s
    """ % (('<div class="message ok">%s</div>' % e(message)) if message else "",
           "".join(lignes) or '<div class="carte sous">Aucune demande pour le moment.</div>'), actif="/prieres")


def vue_temoignages(base, session, message=""):
    jeton = jeton_csrf(session)
    lignes = []
    for t in base.execute("select * from temoignages order by id desc limit 200"):
        badge = {"publie": "tag vert", "en_attente": "tag", "refuse": "tag gris"}.get(t["statut"], "tag gris")
        actions = []
        if t["statut"] != "publie":
            actions.append("""<form class="inline" method="post" action="/temoignages/statut">
              <input type="hidden" name="csrf" value="%s"><input type="hidden" name="id" value="%s">
              <input type="hidden" name="statut" value="publie">
              <button class="discret" type="submit">Publier</button></form>""" % (jeton, t["id"]))
        if t["statut"] != "refuse":
            actions.append("""<form class="inline" method="post" action="/temoignages/statut">
              <input type="hidden" name="csrf" value="%s"><input type="hidden" name="id" value="%s">
              <input type="hidden" name="statut" value="refuse">
              <button class="danger" type="submit">Refuser</button></form>""" % (jeton, t["id"]))
        lignes.append("""<div class="carte">
          <span class="%s">%s</span>
          <div style="font-weight:600;margin-top:8px">%s</div>
          <div class="sous">%s · identité : %s · %s</div>
          <p style="margin:0 0 10px">%s</p>
          %s
        </div>""" % (badge, e(t["statut"]), e(t["titre"]), e(t["nom"] or "Anonyme"),
                        e(t["identite"] or "au choix de l'auteur"), e(t["cree_le"][:10]),
                        e(t["texte"]), " ".join(actions)))

    return page("Témoignages", """
      <h1>Témoignages</h1>
      <p class="sous">Rien n'est publié sans votre validation. « Publier » fait apparaître le témoignage sur le site.</p>
      %s
      %s
    """ % (('<div class="message ok">%s</div>' % e(message)) if message else "",
           "".join(lignes) or '<div class="carte sous">Aucun témoignage pour le moment.</div>'), actif="/temoignages")


# ══════════════════════════════════════════════════════════════════════
# 5. FORMULAIRES MULTIPART
# ══════════════════════════════════════════════════════════════════════

def analyser_multipart(corps, entete_type):
    """Rend {nom: (nom_fichier, type, contenu)} — parseur minimal mais strict."""
    m = re.search(r"boundary=([^\s;]+)", entete_type or "")
    if not m:
        return {}
    frontiere = ("--" + m.group(1).strip('"')).encode()
    champs = {}
    for bloc in corps.split(frontiere):
        if not bloc.strip() or bloc.strip() == b"--":
            continue
        if b"\r\n\r\n" not in bloc:
            continue
        entetes, contenu = bloc.split(b"\r\n\r\n", 1)
        contenu = contenu[:-2] if contenu.endswith(b"\r\n") else contenu
        nom = re.search(rb'name="([^"]*)"', entetes)
        if not nom:
            continue
        nom = nom.group(1).decode("utf-8", "replace")
        fichier = re.search(rb'filename="([^"]*)"', entetes)
        if fichier:
            champs[nom] = (fichier.group(1).decode("utf-8", "replace"), contenu)
        else:
            champs[nom] = (None, contenu)
    return champs


def type_image(donnees):
    if donnees.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if donnees.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if donnees[:4] == b"RIFF" and donnees[8:12] == b"WEBP":
        return "webp"
    return None


def enregistrer_image(nom_fichier, donnees):
    """Valide la signature binaire, renomme proprement, écrit dans assets/img/affiches."""
    extension = type_image(donnees)
    if not extension:
        raise ValueError("Le fichier n'est pas une image JPG, PNG ou WEBP reconnue.")
    if len(donnees) > MAX_UPLOAD:
        raise ValueError("L'affiche dépasse 4 Mo.")
    base = re.sub(r"[^a-z0-9]+", "-", (nom_fichier or "affiche").rsplit(".", 1)[0].lower()).strip("-")[:40]
    nom = "%s-%s.%s" % (base or "affiche", secrets.token_hex(4), extension)
    chemin = os.path.join(DOSSIER_AFFICHES, nom)
    if os.path.dirname(os.path.abspath(chemin)) != os.path.abspath(DOSSIER_AFFICHES):
        raise ValueError("Chemin refusé.")
    with open(chemin, "wb") as fh:
        fh.write(donnees)
    return "assets/img/affiches/" + nom


# ══════════════════════════════════════════════════════════════════════
# 6. SERVEUR HTTP
# ══════════════════════════════════════════════════════════════════════

ORIGINE_SITE = os.environ.get("CAD_ORIGINE", "http://127.0.0.1:4321")
VISITE_API = {}                     # ip -> [horodatages]
LIMITE_API = 30                     # requêtes par heure et par IP


def autoriser_api(ip):
    maintenant = time.time()
    historique = [t for t in VISITE_API.get(ip, []) if maintenant - t < 3600]
    if len(historique) >= LIMITE_API:
        VISITE_API[ip] = historique
        return False
    historique.append(maintenant)
    VISITE_API[ip] = historique
    return True


class Administration(BaseHTTPRequestHandler):
    serveur_version = "CAD-Admin/1.0"
    protocole = "HTTP/1.1"

    # ── Utilitaires ──────────────────────────────────────────────

    def envoyer(self, code, corps, type_entete="text/html; charset=utf-8", entetes=None):
        donnees = corps.encode("utf-8") if isinstance(corps, str) else corps
        self.send_response(code)
        self.send_header("Content-Type", type_entete)
        self.send_header("Content-Length", str(len(donnees)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
            "script-src 'none'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
        )
        for cle, valeur in (entetes or {}).items():
            self.send_header(cle, valeur)
        self.end_headers()
        self.wfile.write(donnees)

    def rediriger(self, vers, entetes=None):
        self.send_response(303)
        self.send_header("Location", vers)
        for cle, valeur in (entetes or {}).items():
            self.send_header(cle, valeur)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def cookie_session(self):
        brut = self.headers.get("Cookie", "")
        if not brut:
            return None
        biscuits = SimpleCookie()
        try:
            biscuits.load(brut)
        except Exception:
            return None
        return biscuits["cad_session"].value if "cad_session" in biscuits else None

    def connecte(self):
        return session_valide(self.cookie_session())

    def corps(self):
        try:
            taille = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return b""
        return self.rfile.read(taille) if taille > 0 else b""

    def champs(self):
        """Champs de formulaire (urlencoded ou multipart), jamais de confiance."""
        brut = self.corps()
        type_entete = self.headers.get("Content-Type", "")
        if type_entete.startswith("multipart/form-data"):
            return analyser_multipart(brut, type_entete)
        donnees = parse_qs(brut.decode("utf-8", "replace"), keep_blank_values=True)
        return {cle: (None, valeurs[0].encode()) for cle, valeurs in donnees.items()}

    def texte(self, champs, cle, maximum=2000):
        valeur = champs.get(cle)
        if not valeur:
            return ""
        return valeur[1].decode("utf-8", "replace").strip()[:maximum]

    def csrf_valide(self, champs):
        attendu = jeton_csrf(self.cookie_session() or "")
        return hmac.compare_digest(self.texte(champs, "csrf"), attendu)

    # ── Routage ──────────────────────────────────────────────────

    def do_GET(self):
        chemin = unquote(self.path.split("?")[0])
        if chemin == "/connexion":
            return self.envoyer(200, page_connexion())
        if chemin == "/deconnexion":
            return self.rediriger("/connexion", {
                "Set-Cookie": "cad_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Strict"
            })
        if chemin == "/site":
            return self.rediriger(ORIGINE_SITE)
        if chemin.startswith("/assets/"):
            return self.fichier_site(chemin)
        if not self.connecte():
            return self.rediriger("/connexion")

        with connexion() as base:
            if chemin == "/":
                return self.envoyer(200, vue_tableau(base, self.cookie_session()))
            if chemin == "/affiches":
                return self.envoyer(200, vue_affiches(base, self.cookie_session()))
            if chemin == "/prieres":
                return self.envoyer(200, vue_prieres(base, self.cookie_session()))
            if chemin == "/temoignages":
                return self.envoyer(200, vue_temoignages(base, self.cookie_session()))
        return self.envoyer(404, page("Introuvable", "<h1>Page introuvable</h1>"))

    def do_POST(self):
        chemin = unquote(self.path.split("?")[0])

        # ── API publique (site statique → administration) ──
        if chemin in ("/api/priere", "/api/temoignage"):
            return self.api(chemin)

        champs = self.champs()

        if chemin == "/connexion":
            with connexion() as base:
                ligne = base.execute("select * from utilisateur where id = 1").fetchone()
            if not ligne:
                return self.envoyer(200, page_connexion("Aucun mot de passe n'est encore défini."))
            identifiant = self.texte(champs, "identifiant")
            motdepasse = champs.get("motdepasse", (None, b""))[1].decode("utf-8", "replace")
            if identifiant != ligne["identifiant"] or not verifier(motdepasse, ligne["empreinte"], ligne["sel"]):
                time.sleep(0.6)      # ralentit les essais successifs
                return self.envoyer(401, page_connexion("Identifiant ou mot de passe incorrect."))
            valeur = creer_session()
            return self.rediriger("/", {
                "Set-Cookie": "cad_session=%s; Path=/; Max-Age=%d; HttpOnly; SameSite=Strict"
                              % (valeur, DUREE_SESSION)
            })

        if not self.connecte():
            return self.rediriger("/connexion")
        if not self.csrf_valide(champs):
            return self.envoyer(403, page("Refusé", "<h1>Jeton de formulaire invalide</h1>"
                                                "<p>Rechargez la page et recommencez.</p>"))

        session = self.cookie_session()

        if chemin == "/affiches":
            return self.creer_affiche(champs, session)
        if chemin == "/affiches/supprimer":
            with connexion() as base:
                base.execute("delete from affiches where id = ?", (self.texte(champs, "id"),))
            exporter()
            return self.rediriger("/affiches")

        if chemin in ("/prieres/statut", "/temoignages/statut"):
            table = "prieres" if chemin.startswith("/prieres") else "temoignages"
            statut = self.texte(champs, "statut")
            autorises = {"prieres": ("nouvelle", "traitee"),
                         "temoignages": ("publie", "refuse", "en_attente")}[table]
            if statut not in autorises:
                return self.envoyer(400, page("Erreur", "<h1>Statut inconnu</h1>"))
            with connexion() as base:
                base.execute("update %s set statut = ? where id = ?" % table,
                             (statut, self.texte(champs, "id")))
            exporter()
            return self.rediriger("/" + table)

        if chemin == "/prieres/supprimer":
            with connexion() as base:
                base.execute("delete from prieres where id = ?", (self.texte(champs, "id"),))
            return self.rediriger("/prieres")

        return self.envoyer(404, page("Introuvable", "<h1>Page introuvable</h1>"))

    def fichier_site(self, chemin):
        """Sert les fichiers du site (images d'affiches) sans sortir de la racine."""
        relatif = os.path.normpath(unquote(chemin).lstrip("/"))
        if not relatif.startswith("assets" + os.sep) and not relatif.startswith("assets/"):
            return self.envoyer(403, page("Refusé", "<h1>Chemin refusé</h1>"))
        absolu = os.path.join(RACINE_SITE, relatif)
        if not os.path.abspath(absolu).startswith(os.path.abspath(RACINE_SITE) + os.sep):
            return self.envoyer(403, page("Refusé", "<h1>Chemin refusé</h1>"))
        if not os.path.isfile(absolu):
            return self.envoyer(404, page("Introuvable", "<h1>Fichier introuvable</h1>"))
        types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                 ".webp": "image/webp", ".json": "application/json; charset=utf-8"}
        with open(absolu, "rb") as fh:
            donnees = fh.read()
        return self.envoyer(200, donnees, types.get(os.path.splitext(absolu)[1].lower(),
                                                    "application/octet-stream"))

    # ── Actions ──────────────────────────────────────────────────

    def creer_affiche(self, champs, session):
        titre = self.texte(champs, "titre", 160)
        if not titre:
            with connexion() as base:
                return self.envoyer(400, vue_affiches(base, session, erreur="Le titre est obligatoire."))
        image = None
        fichier = champs.get("image")
        try:
            if fichier and fichier[1]:
                image = enregistrer_image(fichier[0], fichier[1])
        except ValueError as erreur:
            with connexion() as base:
                return self.envoyer(400, vue_affiches(base, session, erreur=str(erreur)))
        date_iso = self.texte(champs, "date_iso", 10)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_iso or ""):
            date_iso = None
        with connexion() as base:
            base.execute(
                "insert into affiches (titre, categorie, date_iso, heure, lieu, description, image, cree_le) "
                "values (?,?,?,?,?,?,?,?)",
                (titre, self.texte(champs, "categorie", 40) or "Veillée", date_iso,
                 self.texte(champs, "heure", 60), self.texte(champs, "lieu", 200),
                 self.texte(champs, "description", 2000), image, horodatage()),
            )
        exporter()
        with connexion() as base:
            return self.envoyer(200, vue_affiches(base, session, message="Affiche publiée. Elle est en ligne."))

    def api(self, chemin):
        origine = self.headers.get("Origin", "")
        ip = self.client_address[0]
        entetes = {
            "Access-Control-Allow-Origin": ORIGINE_SITE if origine in ("", ORIGINE_SITE) else "",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Vary": "Origin",
        }
        entetes = {k: v for k, v in entetes.items() if v}
        if not autoriser_api(ip):
            return self.envoyer(429, json.dumps({"ok": False, "erreur": "Trop de demandes."}),
                                "application/json", entetes)
        champs = self.champs()
        if chemin == "/api/priere":
            message = self.texte(champs, "message", 4000)
            if len(message) < 5:
                return self.envoyer(400, json.dumps({"ok": False, "erreur": "Message trop court."}),
                                    "application/json", entetes)
            with connexion() as base:
                base.execute(
                    "insert into prieres (nom, contact, categorie, sujet, message, confidentialite, cree_le) "
                    "values (?,?,?,?,?,?,?)",
                    (self.texte(champs, "nom", 120) or "Anonyme", self.texte(champs, "contact", 160),
                     self.texte(champs, "categorie", 60), self.texte(champs, "sujet", 200),
                     message, self.texte(champs, "confidentialite", 120), horodatage()))
            return self.envoyer(200, json.dumps({"ok": True}), "application/json", entetes)

        texte = self.texte(champs, "texte", 4000)
        if len(texte) < 20:
            return self.envoyer(400, json.dumps({"ok": False, "erreur": "Témoignage trop court."}),
                                "application/json", entetes)
        with connexion() as base:
            base.execute(
                "insert into temoignages (nom, identite, titre, texte, statut, cree_le) values (?,?,?,?,?,?)",
                (self.texte(champs, "nom", 120) or "Anonyme", self.texte(champs, "identite", 80),
                 self.texte(champs, "titre", 180), texte, "en_attente", horodatage()))
        return self.envoyer(200, json.dumps({"ok": True}), "application/json", entetes)

    def do_OPTIONS(self):
        origine = self.headers.get("Origin", "")
        self.send_response(204)
        if origine and origine == ORIGINE_SITE:
            self.send_header("Access-Control-Allow-Origin", origine)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write("%s — %s\n" % (self.address_string(), format % args))


# ══════════════════════════════════════════════════════════════════════
# 7. DÉMARRAGE
# ══════════════════════════════════════════════════════════════════════

def main():
    analyseur = argparse.ArgumentParser(description="Administration du site du Centre")
    analyseur.add_argument("--port", type=int, default=4400)
    analyseur.add_argument("--motdepasse", help="Définit (ou remplace) le mot de passe")
    arguments = analyseur.parse_args()

    initialiser()
    exporter()

    if arguments.motdepasse:
        if len(arguments.motdepasse) < 8:
            sys.exit("Le mot de passe doit faire au moins 8 caractères.")
        definir_motdepasse(arguments.motdepasse)
        print("Mot de passe enregistré.")

    if not utilisateur_existe():
        provisoire = secrets.token_urlsafe(12)
        definir_motdepasse(provisoire)
        print("=" * 62)
        print("PREMIER DÉMARRAGE — mot de passe provisoire :")
        print("   %s" % provisoire)
        print("Changement : python3 admin/serveur.py --motdepasse 'le-vôtre'")
        print("=" * 62)

    serveur = ThreadingHTTPServer(("127.0.0.1", arguments.port), Administration)
    print("Administration : http://127.0.0.1:%d/" % arguments.port)
    print("Site public    : %s" % ORIGINE_SITE)
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt.")


if __name__ == "__main__":
    main()

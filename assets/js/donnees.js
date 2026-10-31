/* Contenus publiés depuis l'administration.
   Lit les fichiers JSON exportés par admin/serveur.py et remplit la page.
   Aucune donnée n'est inventée : si un fichier est vide, l'état vide de la
   page reste affiché. */

(function () {
  "use strict";

  var MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
    "août", "septembre", "octobre", "novembre", "décembre"];

  function dateLisible(iso) {
    if (!iso) return "Date à préciser";
    var morceaux = String(iso).split("-");
    if (morceaux.length !== 3) return iso;
    var jour = parseInt(morceaux[2], 10);
    var mois = parseInt(morceaux[1], 10);
    if (!jour || !mois) return iso;
    return jour + " " + MOIS[mois - 1] + " " + morceaux[0];
  }

  function charger(url) {
    return fetch(url, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).catch(function () {
      return { elements: [] };
    });
  }

  function echapper(t) {
    return String(t == null ? "" : t)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ── Programmes : agenda ─────────────────────────────────────── */
  var zoneAgenda = document.querySelector("[data-agenda]");
  if (zoneAgenda) {
    charger("assets/data/agenda.json").then(function (d) {
      var elements = d.elements || [];
      if (!elements.length) return;
      zoneAgenda.innerHTML = elements.map(function (a) {
        var img = a.image
          ? '<img src="' + echapper(a.image) + '" alt="" width="120" height="150" loading="lazy" ' +
            'style="width:88px;height:110px;object-fit:cover;border-radius:8px;flex:0 0 auto">'
          : "";
        return '<div class="agenda__item">' +
          '<span class="agenda__quand">' + echapper(dateLisible(a.date_iso)) +
          (a.heure ? "<br><span class=\"tiny muted\">" + echapper(a.heure) + "</span>" : "") + "</span>" +
          "<div>" +
            '<span class="tag" style="display:inline-block;font-size:.7rem;letter-spacing:.06em;' +
            'text-transform:uppercase;padding:2px 8px;border-radius:999px;background:rgba(237,108,16,.12);' +
            'color:#a64c0b;font-weight:700">' + echapper(a.categorie) + "</span>" +
            '<div style="font-weight:600;margin-top:6px">' + echapper(a.titre) + "</div>" +
            (a.description ? '<p class="tiny muted mb-0">' + echapper(a.description) + "</p>" : "") +
            (a.lieu ? '<p class="tiny muted mb-0">' + echapper(a.lieu) + "</p>" : "") +
          "</div>" + img + "</div>";
      }).join("");
      zoneAgenda.hidden = false;
      var vide = document.querySelector("[data-agenda-vide]");
      if (vide) vide.hidden = true;
    });
  }

  /* ── Médiathèque : affiches ──────────────────────────────────── */
  var zoneAffiches = document.querySelector("[data-affiches]");
  if (zoneAffiches) {
    charger("assets/data/affiches.json").then(function (d) {
      var elements = d.elements || [];
      if (!elements.length) return;
      zoneAffiches.innerHTML = elements.map(function (a) {
        var legende = a.categorie + " — " + dateLisible(a.date_iso);
        return '<figure data-genre="Affiche" data-titre="' + echapper(a.titre) + '">' +
          '<button type="button" data-image="' + echapper(a.image) + '" data-legende="' +
          echapper(a.titre + " — " + legende) + '">' +
          '<img src="' + echapper(a.image) + '" alt="' + echapper("Affiche : " + a.titre) +
          '" width="800" height="1000" loading="lazy"></button>' +
          '<figcaption>' + echapper(a.titre) + " — " + echapper(legende) + "</figcaption></figure>";
      }).join("");
      zoneAffiches.hidden = false;
      lierVisionneuse();
    });
  }

  /* ── Témoignages publiés ─────────────────────────────────────── */
  var zoneTemoins = document.querySelector("[data-temoignages]");
  if (zoneTemoins) {
    charger("assets/data/temoignages.json").then(function (d) {
      var elements = d.elements || [];
      if (!elements.length) return;
      zoneTemoins.innerHTML = elements.map(function (t) {
        var nom = t.nom || "Anonyme";
        if (/anonym/i.test(t.identite || "")) nom = "Anonyme";
        else if (/pr[ée]nom/i.test(t.identite || "")) nom = String(nom).split(" ")[0];
        return '<article class="carte">' +
          '<p class="carte__numero">' + echapper(dateLisible(t.cree_le ? t.cree_le.slice(0, 10) : "")) + "</p>" +
          "<h3 style=\"font-size:1.1rem\">" + echapper(t.titre) + "</h3>" +
          '<p class="muted">' + echapper(t.texte) + "</p>" +
          '<p class="tiny mb-0"><strong>' + echapper(nom) + "</strong></p></article>";
      }).join("");
      zoneTemoins.hidden = false;
      var vide = document.querySelector("[data-temoignages-vide]");
      if (vide) vide.hidden = true;
    });
  }

  /* ── Visionneuse des affiches (le dialogue existe sur la page) ── */
  function lierVisionneuse() {
    var boite = document.querySelector("[data-visionneuse]");
    if (!boite || typeof boite.showModal !== "function") return;
    var image = boite.querySelector("[data-visionneuse-image]");
    var legende = boite.querySelector("[data-visionneuse-legende]");
    document.querySelectorAll("[data-affiches] [data-image]").forEach(function (bouton) {
      bouton.addEventListener("click", function () {
        image.src = bouton.dataset.image;
        image.alt = bouton.dataset.legende || "";
        if (legende) legende.textContent = bouton.dataset.legende || "";
        boite.showModal();
      });
    });
  }
})();

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
        return '<div class="agenda__item">' +
          '<span class="agenda__quand">' + echapper(dateLisible(a.date_iso)) +
          (a.heure ? "<br>" + echapper(a.heure) : "") + "</span>" +
          "<div><strong>" + echapper(a.titre) + "</strong>" +
          (a.description ? "<br>" + echapper(a.description) : "") +
          (a.lieu ? "<br><em>" + echapper(a.lieu) + "</em>" : "") + "</div>" +
          (a.image ? '<img src="' + echapper(a.image) + '" alt="" width="88" height="110" loading="lazy" style="width:88px;height:110px;object-fit:cover;border-radius:4px">' : "<span></span>") +
          "</div>";
      }).join("");
      zoneAgenda.hidden = false;
    });
  }

  /* ── Médiathèque : affiches publiées depuis l'administration ─── */
  var zoneAffiches = document.querySelector("[data-affiches]");
  if (zoneAffiches) {
    charger("assets/data/affiches.json").then(function (d) {
      var elements = d.elements || [];
      if (!elements.length) return;
      zoneAffiches.innerHTML = elements.map(function (a) {
        var legende = a.titre + ", " + dateLisible(a.date_iso);
        return '<button type="button" data-image="' + echapper(a.image) + '" data-legende="' + echapper(legende) + '">' +
          '<img src="' + echapper(a.image) + '" alt="' + echapper("Affiche : " + a.titre) +
          '" width="800" height="1000" loading="lazy"></button>';
      }).join("");
      zoneAffiches.hidden = false;
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
        if (/anonym|rien/i.test(t.identite || "")) nom = "Anonyme";
        else if (/pr[ée]nom/i.test(t.identite || "")) nom = String(nom).split(" ")[0];
        return '<article class="temoignage"><h3>' + echapper(t.titre) + "</h3>" +
          "<p>" + echapper(t.texte) + "</p><footer>" + echapper(nom) + ", " +
          echapper(dateLisible(t.cree_le ? t.cree_le.slice(0, 10) : "")) + "</footer></article>";
      }).join("");
      var bloc = document.querySelector("[data-temoignages-bloc]");
      if (bloc) bloc.hidden = false;
    });
  }
})();

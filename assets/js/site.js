/* CENTRE DES AMOUREUX DE DIEU — interactions du site
   Aucune dépendance, aucun traceur. Le lecteur YouTube n'est chargé
   qu'après un clic explicite (aucun cookie tiers avant consentement). */

(function () {
  "use strict";

  /* ── 1. En-tête : ombre après défilement ────────────────────────── */
  var entete = document.querySelector(".site-header");
  if (entete) {
    var majEntete = function () {
      entete.dataset.scrolled = window.scrollY > 8 ? "true" : "false";
    };
    majEntete();
    window.addEventListener("scroll", majEntete, { passive: true });
  }

  /* ── 2. Navigation mobile ───────────────────────────────────────── */
  var bascule = document.querySelector(".nav-toggle");
  var nav = document.getElementById("nav-principal");
  if (bascule && nav) {
    var fermer = function () {
      nav.dataset.ouvert = "false";
      bascule.setAttribute("aria-expanded", "false");
    };
    bascule.addEventListener("click", function () {
      var ouvert = nav.dataset.ouvert === "true";
      nav.dataset.ouvert = ouvert ? "false" : "true";
      bascule.setAttribute("aria-expanded", ouvert ? "false" : "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) fermer();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") fermer();
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 960) fermer();
    });
  }

  /* ── 3. Lecteur YouTube paresseux ───────────────────────────────
     Chaque vignette est un <button class="lecteur" data-video="ID">.
     Au clic : on remplace le bouton par une iframe youtube-nocookie. */
  document.querySelectorAll(".lecteur").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      var id = bouton.dataset.video;
      if (!id) return;
      var iframe = document.createElement("iframe");
      iframe.src =
        "https://www.youtube-nocookie.com/embed/" +
        encodeURIComponent(id) +
        "?autoplay=1&rel=0&modestbranding=1&hl=fr";
      iframe.title = bouton.dataset.titre || "Vidéo d'enseignement";
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;
      iframe.loading = "lazy";
      bouton.replaceWith(iframe);
    });
  });

  /* ── 4. Formulaire : composition d'un message (sans serveur) ─────
     Tant qu'aucun point d'envoi n'est branché, le formulaire ne fait
     pas semblant d'envoyer : il compose un message que le visiteur
     envoie lui-même, et le dit clairement. */
  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var donnees = new FormData(form);
      var lignes = [];
      donnees.forEach(function (valeur, cle) {
        if (cle === "consentement" || !valeur) return;
        var etiquette =
          (form.querySelector('[name="' + cle + '"]') || {}).labels &&
          form.querySelector('[name="' + cle + '"]').labels[0]
            ? form.querySelector('[name="' + cle + '"]').labels[0].textContent.trim()
            : cle;
        lignes.push(etiquette + " : " + valeur);
      });
      var sujet = form.dataset.sujet || "Message depuis le site";
      var corps = lignes.join("\n");
      var href =
        "mailto:" +
        form.dataset.mailto +
        "?subject=" +
        encodeURIComponent(sujet) +
        "&body=" +
        encodeURIComponent(corps);
      var avis = form.querySelector("[data-avis]");
      if (avis) {
        avis.hidden = false;
        avis.textContent =
          "Votre messagerie va s'ouvrir avec le message pré-rempli. Vérifiez-le puis envoyez-le.";
      }
      window.location.href = href;
    });
  });

  /* ── 5. Année du pied de page ───────────────────────────────────── */
  document.querySelectorAll("[data-annee]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();

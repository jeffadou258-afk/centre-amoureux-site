/* Centre des Amoureux de Dieu — interactions du site.
   Aucune dépendance, aucun traceur. Le lecteur YouTube n'est chargé
   qu'après un clic. */

(function () {
  "use strict";

  /* ── 1. En-tête : fond plein après défilement ───────────────────── */
  var entete = document.querySelector(".site-header");
  if (entete) {
    var majEntete = function () {
      entete.dataset.scrolled = window.scrollY > 24 ? "true" : "false";
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
      if (window.innerWidth > 1080) fermer();
    });
  }

  /* ── 3. Lecteur YouTube au clic ─────────────────────────────────── */
  document.querySelectorAll(".lecteur").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      var id = bouton.dataset.video;
      if (!id) return;
      var iframe = document.createElement("iframe");
      iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) +
        "?autoplay=1&rel=0&modestbranding=1&hl=fr";
      iframe.title = bouton.dataset.titre || "Prédication";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;
      bouton.replaceWith(iframe);
    });
  });

  /* ── 4. Formulaires : envoi au Centre ───────────────────────────────
     Si l'administration est branchée (CAD_API), le formulaire envoie
     réellement. Sinon il prépare un message WhatsApp adressé au Centre,
     que le visiteur envoie lui-même. */
  document.querySelectorAll("form[data-whatsapp]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var avis = form.querySelector("[data-avis]");
      var dire = function (t) {
        if (!avis) return;
        avis.hidden = false;
        avis.textContent = t;
      };

      var api = window.CAD_API || "";
      var ressource = form.dataset.api;
      if (api && ressource) {
        var envoi = new FormData(form);
        var bouton = form.querySelector('button[type="submit"]');
        var libelle = bouton ? bouton.textContent : "";
        if (bouton) { bouton.disabled = true; bouton.textContent = "Envoi…"; }
        fetch(api.replace(/\/$/, "") + "/api/" + ressource, { method: "POST", body: envoi })
          .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
          .then(function (r) {
            if (!r.ok) throw new Error("refus");
            form.reset();
            dire("Merci, votre message est bien arrivé au Centre.");
          })
          .catch(function () {
            dire("L'envoi n'a pas abouti. Réessayez dans un instant, ou appelez le +225 07 87 59 32 89.");
          })
          .then(function () {
            if (bouton) { bouton.disabled = false; bouton.textContent = libelle; }
          });
        return;
      }

      var lignes = [(form.dataset.sujet || "Message") + " (site du Centre)"];
      new FormData(form).forEach(function (valeur, cle) {
        var champ = form.querySelector('[name="' + cle + '"]');
        if (!valeur || (champ && champ.type === "checkbox")) return;
        var etiquette = champ && champ.labels && champ.labels[0] ? champ.labels[0].textContent.trim() : cle;
        lignes.push(etiquette + " : " + valeur);
      });
      window.open("https://wa.me/" + form.dataset.whatsapp + "?text=" + encodeURIComponent(lignes.join("\n")),
        "_blank", "noopener");
      dire("WhatsApp s'ouvre avec votre message prêt à partir : il ne vous reste qu'à l'envoyer.");
    });
  });

  /* ── 5. Année du pied de page ───────────────────────────────────── */
  document.querySelectorAll("[data-annee]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* ── 6. Prochain culte (accueil) ────────────────────────────────────
     Abidjan est à l'heure UTC toute l'année. Culte : dimanche 14h–18h30. */
  var compte = document.querySelector("[data-compte]");
  if (compte) {
    var majCompte = function () {
      var maintenant = new Date();
      var debut = new Date(Date.UTC(maintenant.getUTCFullYear(), maintenant.getUTCMonth(),
        maintenant.getUTCDate(), 14, 0, 0));
      var jours = (7 - maintenant.getUTCDay()) % 7;
      debut.setUTCDate(debut.getUTCDate() + jours);
      var fin = new Date(debut.getTime() + 4.5 * 3600 * 1000);
      if (maintenant >= fin) {
        debut.setUTCDate(debut.getUTCDate() + 7);
      } else if (maintenant >= debut) {
        compte.innerHTML = "<strong>Le culte a commencé.</strong> Il vous attend jusqu'à 18h30.";
        return;
      }
      var reste = Math.max(0, debut - maintenant);
      var j = Math.floor(reste / 86400000);
      var h = Math.floor((reste % 86400000) / 3600000);
      var m = Math.floor((reste % 3600000) / 60000);
      var texte = j > 0 ? j + " j " + h + " h" : (h > 0 ? h + " h " + m + " min" : m + " min");
      compte.innerHTML = "Prochain culte dimanche à 14h00 · <strong>dans " + texte + "</strong>";
    };
    majCompte();
    setInterval(majCompte, 30000);
  }

  /* ── 7. Événements passés : retirés le lendemain de leur fin ───────── */
  var aujourdhui = new Date().toISOString().slice(0, 10);
  document.querySelectorAll("[data-fin]").forEach(function (el) {
    if (el.dataset.fin && el.dataset.fin < aujourdhui) el.dataset.passe = "true";
  });
})();

/* ── 8. Filtres et recherche (prédications) ──────────────────────── */
(function () {
  "use strict";
  var liste = document.querySelector("[data-liste]");
  if (!liste) return;
  var elements = function () {
    return Array.prototype.slice.call(liste.querySelectorAll("[data-genre]"));
  };
  var boutons = document.querySelectorAll("[data-filtre]");
  var recherche = document.querySelector("[data-recherche]");
  var compteur = document.querySelector("[data-compteur]");
  var aucun = document.querySelector("[data-aucun-resultat]");
  var courant = "tous";
  var normaliser = function (t) {
    return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  };
  var appliquer = function () {
    var q = normaliser(recherche ? recherche.value : "");
    var visibles = 0;
    elements().forEach(function (el) {
      var ok = (courant === "tous" || el.dataset.genre === courant) &&
        (!q || normaliser(el.dataset.titre).indexOf(q) !== -1);
      el.hidden = !ok;
      if (ok) visibles++;
    });
    if (compteur) compteur.textContent = visibles + (visibles > 1 ? " messages" : " message");
    if (aucun) aucun.hidden = visibles !== 0;
  };
  boutons.forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      courant = bouton.dataset.filtre;
      boutons.forEach(function (b) { b.setAttribute("aria-pressed", b === bouton ? "true" : "false"); });
      appliquer();
    });
  });
  if (recherche) recherche.addEventListener("input", appliquer);
  appliquer();
})();

/* ── 9. Visionneuse (médiathèque) ────────────────────────────────── */
(function () {
  "use strict";
  var boite = document.querySelector("[data-visionneuse]");
  if (!boite || typeof boite.showModal !== "function") return;
  var image = boite.querySelector("[data-visionneuse-image]");
  var legende = boite.querySelector("[data-visionneuse-legende]");
  window.CAD_ouvrirImage = function (src, texte) {
    image.src = src;
    image.alt = texte || "";
    if (legende) legende.textContent = texte || "";
    boite.showModal();
  };
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-image]");
    if (b) window.CAD_ouvrirImage(b.dataset.image, b.dataset.legende);
  });
  boite.addEventListener("click", function (e) {
    if (e.target === boite) boite.close();
  });
})();

/* ── 10. Copier le lien d'une prédication ────────────────────────── */
(function () {
  "use strict";
  document.querySelectorAll("[data-copier]").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      var lien = bouton.dataset.copier;
      var ancien = bouton.textContent;
      var ok = function () {
        bouton.textContent = "Lien copié";
        setTimeout(function () { bouton.textContent = ancien; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(lien).then(ok, function () { window.prompt("Copiez ce lien :", lien); });
      } else {
        window.prompt("Copiez ce lien :", lien);
      }
    });
  });
})();

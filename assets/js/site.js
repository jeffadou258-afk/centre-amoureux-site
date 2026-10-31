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
      if (window.innerWidth > 1180) fermer();
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

      /* Si l'administration est branchée, le formulaire ENVOIE réellement.
         Sinon il compose un message : il ne fait jamais semblant d'envoyer. */
      var api = window.CAD_API || "";
      var ressource = form.dataset.api;
      var avisEnvoi = form.querySelector("[data-avis]");
      if (api && ressource) {
        var envoi = new FormData(form);
        envoi.delete("consentement");
        var bouton = form.querySelector('button[type="submit"]');
        var libelle = bouton ? bouton.textContent : "";
        if (bouton) {
          bouton.disabled = true;
          bouton.textContent = "Envoi en cours…";
        }
        fetch(api.replace(/\/$/, "") + "/api/" + ressource, { method: "POST", body: envoi })
          .then(function (reponse) {
            return reponse.json().catch(function () {
              return { ok: false };
            });
          })
          .then(function (reponse) {
            if (!reponse.ok) throw new Error(reponse.erreur || "refus");
            form.reset();
            if (avisEnvoi) {
              avisEnvoi.hidden = false;
              avisEnvoi.textContent = "Message reçu. Il sera traité par l'équipe du Centre.";
            }
          })
          .catch(function () {
            if (avisEnvoi) {
              avisEnvoi.hidden = false;
              avisEnvoi.textContent =
                "L'envoi a échoué. Réessayez dans un instant ; si cela persiste, écrivez à l'adresse indiquée.";
            }
          })
          .then(function () {
            if (bouton) {
              bouton.disabled = false;
              bouton.textContent = libelle;
            }
          });
        return;
      }

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

/* ── 6. Filtres et recherche (enseignements, médiathèque) ────────── */
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

  var normaliser = function (texte) {
    return (texte || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  };

  var appliquer = function () {
    var requete = recherche ? normaliser(recherche.value.trim()) : "";
    var visibles = 0;

    elements().forEach(function (el) {
      var bonGenre = courant === "tous" || el.dataset.genre === courant;
      var bonTexte = !requete || normaliser(el.dataset.titre).indexOf(requete) > -1;
      var visible = bonGenre && bonTexte;
      el.hidden = !visible;
      if (visible) visibles += 1;
    });

    if (compteur) {
      compteur.textContent = visibles + (visibles > 1 ? " résultats" : " résultat");
    }
    if (aucun) aucun.hidden = visibles !== 0;
  };

  boutons.forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      courant = bouton.dataset.filtre;
      boutons.forEach(function (b) {
        b.setAttribute("aria-pressed", b === bouton ? "true" : "false");
      });
      appliquer();
    });
  });

  if (recherche) recherche.addEventListener("input", appliquer);

  /* Une vignette peut être masquée avant même le premier rendu */
  appliquer();
})();

/* ── 7. Visionneuse de la médiathèque ────────────────────────────── */
(function () {
  "use strict";

  var boite = document.querySelector("[data-visionneuse]");
  if (!boite || typeof boite.showModal !== "function") return;

  var image = boite.querySelector("[data-visionneuse-image]");
  var legende = boite.querySelector("[data-visionneuse-legende]");

  document.querySelectorAll("[data-image]").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      image.src = bouton.dataset.image;
      image.alt = bouton.dataset.legende || "";
      if (legende) legende.textContent = bouton.dataset.legende || "";
      boite.showModal();
    });
  });

  boite.addEventListener("click", function (e) {
    if (e.target === boite) boite.close();
  });
})();

/* ── 8. Copier le lien d'une prédication ─────────────────────────── */
(function () {
  "use strict";

  document.querySelectorAll("[data-copier]").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      var lien = bouton.dataset.copier;
      var ancien = bouton.textContent;
      var confirmer = function () {
        bouton.textContent = "Lien copié";
        setTimeout(function () {
          bouton.textContent = ancien;
        }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(lien).then(confirmer, function () {
          window.prompt("Copiez ce lien :", lien);
        });
      } else {
        window.prompt("Copiez ce lien :", lien);
      }
    });
  });
})();

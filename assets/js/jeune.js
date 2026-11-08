/* Inscription au jeûne de novembre 2026.
   Valider = entrer dans le groupe WhatsApp du jeûne.
   - Si la base Supabase du site est configurée (assets/js/config.js),
     l'inscription est d'abord ENREGISTRÉE (table inscriptions_jeune),
     puis le visiteur est conduit dans le groupe.
   - Sinon, le visiteur est conduit directement dans le groupe. */
(function () {
  "use strict";
  var form = document.getElementById("form-jeune");
  if (!form) return;
  var groupe = document.getElementById("jeune-groupe");
  var lien = document.getElementById("lien-groupe");
  var avis = form.querySelector("[data-avis]");
  var bouton = form.querySelector('button[type="submit"]');
  var conf = window.CAD_SUPABASE || {};

  function dire(texte) {
    avis.hidden = false;
    avis.textContent = texte;
  }
  function entrerDansLeGroupe() {
    groupe.hidden = false; /* bouton de secours si WhatsApp ne s'ouvre pas */
    window.location.href = lien.href;
  }
  function nettoyer(v) {
    return String(v || "").replace(/\s+/g, " ").trim();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var d = new FormData(form);
    var ligne = {
      nom: nettoyer(d.get("nom")),
      prenom: nettoyer(d.get("prenom")),
      quartier: nettoyer(d.get("quartier")),
      telephone: nettoyer(d.get("telephone")),
      programme: form.dataset.programme,
      consentement: true
    };

    if (!(conf.url && conf.anonKey)) {
      dire("Merci " + ligne.prenom + " ! Ouverture du groupe WhatsApp du jeûne…");
      entrerDansLeGroupe();
      return;
    }

    var libelle = bouton.textContent;
    bouton.disabled = true;
    bouton.textContent = "Enregistrement…";
    fetch(conf.url.replace(/\/$/, "") + "/rest/v1/inscriptions_jeune", {
      method: "POST",
      headers: {
        apikey: conf.anonKey,
        Authorization: "Bearer " + conf.anonKey,
        "Content-Type": "application/json",
        Prefer: "return=minimal"
      },
      body: JSON.stringify(ligne)
    })
      .then(function (r) {
        if (r.status === 201 || r.status === 409) {
          dire(
            (r.status === 201
              ? "Merci " + ligne.prenom + ", votre inscription est enregistrée."
              : "Ce numéro est déjà inscrit.") + " Ouverture du groupe WhatsApp…"
          );
          entrerDansLeGroupe();
        } else {
          throw new Error("refus " + r.status);
        }
      })
      .catch(function () {
        /* L'inscription a échoué : on ne bloque pas l'entrée dans le groupe. */
        dire("Votre inscription n'a pas pu être enregistrée, mais vous pouvez rejoindre le groupe.");
        groupe.hidden = false;
      })
      .then(function () {
        bouton.disabled = false;
        bouton.textContent = libelle;
      });
  });
})();

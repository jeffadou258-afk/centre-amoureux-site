/* Inscription au jeûne de novembre 2026.
   - Si la base Supabase du site est configurée (assets/js/config.js),
     l'inscription est ENREGISTRÉE dans la table inscriptions_jeune.
   - Sinon, le formulaire prépare un message WhatsApp vers le Centre :
     il ne fait jamais semblant d'enregistrer.
   Dans les deux cas, le bouton du groupe WhatsApp apparaît ensuite. */
(function () {
  "use strict";
  var form = document.getElementById("form-jeune");
  if (!form) return;
  var groupe = document.getElementById("jeune-groupe");
  var avis = form.querySelector("[data-avis]");
  var bouton = form.querySelector('button[type="submit"]');
  var conf = window.CAD_SUPABASE || {};

  function dire(texte) {
    avis.hidden = false;
    avis.textContent = texte;
  }
  function montrerGroupe() {
    groupe.hidden = false;
    groupe.scrollIntoView({ behavior: "smooth", block: "center" });
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

    if (conf.url && conf.anonKey) {
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
          if (r.status === 201) {
            form.reset();
            dire("Merci " + ligne.prenom + ", votre inscription est enregistrée.");
            montrerGroupe();
          } else if (r.status === 409) {
            dire("Ce numéro est déjà inscrit au jeûne. Il ne vous reste qu'à rejoindre le groupe.");
            montrerGroupe();
          } else {
            throw new Error("refus " + r.status);
          }
        })
        .catch(function () {
          dire("L'inscription n'a pas pu être enregistrée. Réessayez dans un instant ou contactez le +225 07 87 59 32 89.");
        })
        .then(function () {
          bouton.disabled = false;
          bouton.textContent = libelle;
        });
      return;
    }

    /* Pas de base branchée : message WhatsApp pré-rempli vers le Centre. */
    var texte =
      "Inscription au jeûne de 14 jours (9 au 22 novembre 2026)\n" +
      "Nom : " + ligne.nom + "\n" +
      "Prénom : " + ligne.prenom + "\n" +
      "Quartier : " + ligne.quartier + "\n" +
      "Numéro : " + ligne.telephone;
    window.open("https://wa.me/" + form.dataset.whatsapp + "?text=" + encodeURIComponent(texte), "_blank", "noopener");
    dire("WhatsApp s'ouvre avec votre inscription : envoyez le message pour la confirmer, puis rejoignez le groupe ci-dessous.");
    montrerGroupe();
  });
})();

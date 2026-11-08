/* Configuration du site — un seul endroit à modifier au déploiement.
   CAD_API : adresse de l'administration (serveur admin/serveur.py).
   Vide = les formulaires restent en mode « composer un message » (mailto).
   Renseigner par exemple : window.CAD_API = "https://admin.centre-des-amoureux.org"; */
window.CAD_API = "";

/* Base Supabase du SITE (projet dédié, voir base-de-donnees/README.md).
   Seule la clé « anon public » va ici — JAMAIS la clé service_role.
   Vide = l'inscription au jeûne passe par un message WhatsApp. */
window.CAD_SUPABASE = { url: "", anonKey: "" };

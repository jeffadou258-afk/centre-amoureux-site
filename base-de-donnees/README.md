# Base de données du SITE — projet Supabase dédié

Objectif : les données du **site vitrine** (demandes de prière, témoignages, agenda)
vivent dans un projet Supabase **séparé** de celui de l'application pastorale
(`dzxtlwzuhogvprlibaow`), pour qu'aucune donnée citoyen ne croise les données d'église.

## Ce qui est prêt ici

| Fichier | Rôle | État |
|---|---|---|
| `schema.sql` | Tables `prieres`, `temoignages`, `affiches`, `equipe`, `depots_recents`, `inscriptions_jeune` + RLS + anti-abus | **écrit, PAS encore exécuté** (aucun projet n'existe) |

Le schéma reprend exactement les colonnes des tables SQLite de `admin/serveur.py`
(`prieres`, `temoignages`, `affiches`), transposées en PostgreSQL.

## Étapes (2 minutes, côté propriétaire)

1. **Créer le projet** — https://supabase.com/dashboard → *New project*
   - Nom : `centre-amoureux-site`
   - Région : `eu-west-1` (Irlande, même région que Pastorale)
   - **Database password** : choisis-le et **garde-le de côté — je n'en ai pas besoin.**
   - Plan : Free. ⚠️ Le plan gratuit autorise **2 projets actifs par organisation** :
     si le tableau de bord refuse, il faut soit mettre un ancien projet en pause,
     soit passer en Pro, soit créer une seconde organisation.
2. **Exécuter le schéma** — onglet *SQL Editor* → coller `schema.sql` → **Run**
3. **Récupérer deux valeurs** — *Project Settings → API*
   - `Project URL`
   - `anon public` key
4. **Me les transmettre sans les écrire dans le chat** : créer le fichier
   `~/centre-amoureux-site/.env.local` contenant

   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_ANON_KEY=eyJ...
   SUPABASE_SERVICE_ROLE_KEY=eyJ...
   ```

   Le `service_role` sert aux opérations d'administration (créer les comptes de
   l'équipe, migrer les JSON existants). Il ne doit **jamais** partir dans le site
   public — il restera côté serveur, et `.env.local` est exclu de git.

## Ce que je ferai ensuite

- vérifier le schéma réellement en place (requête sur `information_schema`, pas une supposition) ;
- migrer les données actuelles de `assets/data/*.json` et du SQLite `admin/donnees/admin.db` ;
- brancher les formulaires du site (prière, témoignage) sur ce projet ;
- laisser l'administration actuelle en lecture, puis la retirer.

## Règle de sécurité appliquée

- dépôt public = **insertion seule**, statut imposé par la base (`nouvelle`, `en_attente`) :
  personne ne peut publier un témoignage depuis le site ;
- lecture réservée aux comptes listés dans `public.equipe` (aucune auto-inscription) ;
- 5 dépôts par heure et par empreinte d'adresse ;
- aucune donnée personnelle dans le site statique : les JSON exportés ne contiennent
  que ce qui est publié.

## Inscriptions au jeûne (ajout du 08/11/2026)

La page `jeune.html` enregistre les inscriptions dans `inscriptions_jeune` dès que
`window.CAD_SUPABASE` est renseigné dans `assets/js/config.js` (URL du projet + clé
`anon public`). Tant que ce n'est pas fait, le formulaire prépare un message WhatsApp
vers le Centre, puis affiche le bouton du groupe : aucune inscription n'est perdue
et rien ne fait semblant d'être enregistré.

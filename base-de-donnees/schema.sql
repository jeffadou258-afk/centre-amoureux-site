-- =====================================================================
-- Centre des Amoureux de Dieu — base de données du SITE (projet dédié)
-- À exécuter dans le projet Supabase NEUF, jamais dans celui de Pastorale.
-- Éditeur SQL du tableau de bord → coller tout ce fichier → Run.
-- NON EXÉCUTÉ à ce jour : aucun projet n'existe encore.
-- =====================================================================

-- 1. Schéma minimal, dérivé des tables réelles de admin/serveur.py (SQLite)
--    → mêmes champs, mêmes règles, transposés en PostgreSQL.

create table if not exists public.prieres (
  id              uuid primary key default gen_random_uuid(),
  nom             text,
  contact         text,
  categorie       text,
  sujet           text,
  message         text not null check (char_length(btrim(message)) between 10 and 4000),
  confidentialite text not null default 'equipe'
                    check (confidentialite in ('equipe', 'public')),
  statut          text not null default 'nouvelle'
                    check (statut in ('nouvelle', 'en_priere', 'traitee', 'archivee')),
  consentement    boolean not null default false,
  cree_le         timestamptz not null default now(),
  maj_le          timestamptz not null default now()
);

create table if not exists public.temoignages (
  id         uuid primary key default gen_random_uuid(),
  nom        text,
  identite   text not null default 'anonyme'
               check (identite in ('anonyme', 'prenom', 'nom_complet')),
  titre      text,
  texte      text not null check (char_length(btrim(texte)) between 20 and 8000),
  statut     text not null default 'en_attente'
               check (statut in ('en_attente', 'publie', 'refuse')),
  consentement boolean not null default false,
  cree_le    timestamptz not null default now(),
  maj_le     timestamptz not null default now()
);

-- Affiches / agenda : données PUBLIQUES (elles s'affichent sur le site).
create table if not exists public.affiches (
  id          uuid primary key default gen_random_uuid(),
  titre       text not null,
  categorie   text not null default 'Veillée',
  date_iso    date,
  heure       text,
  lieu        text,
  description text,
  image       text,
  publique    boolean not null default true,
  cree_le     timestamptz not null default now()
);

-- 2. Équipe : qui peut LIRE les demandes. Aucune auto-inscription :
--    les lignes s'ajoutent à la main, en SQL, par le propriétaire.
create table if not exists public.equipe (
  email   text primary key,
  role    text not null default 'lecteur' check (role in ('lecteur', 'admin')),
  cree_le timestamptz not null default now()
);

create or replace function public.est_equipe()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.equipe e
    where lower(e.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

-- 3. RLS : le dépôt est public, la lecture ne l'est pas.

alter table public.prieres    enable row level security;
alter table public.temoignages enable row level security;
alter table public.affiches   enable row level security;
alter table public.equipe     enable row level security;

-- Prieres : insertion seule pour le public, statut imposé (aucune auto-promotion).
create policy "prieres_depot_public" on public.prieres
  for insert to anon, authenticated
  with check (statut = 'nouvelle' and consentement = true);

create policy "prieres_lecture_equipe" on public.prieres
  for select to authenticated using (public.est_equipe());

create policy "prieres_maj_equipe" on public.prieres
  for update to authenticated using (public.est_equipe()) with check (public.est_equipe());

-- Temoignages : même principe ; seul le statut change côté équipe.
create policy "temoignages_depot_public" on public.temoignages
  for insert to anon, authenticated
  with check (statut = 'en_attente' and consentement = true);

create policy "temoignages_lecture_equipe" on public.temoignages
  for select to authenticated using (public.est_equipe());

create policy "temoignages_maj_equipe" on public.temoignages
  for update to authenticated using (public.est_equipe()) with check (public.est_equipe());

-- Affiches : lecture publique des seules affiches publiques ; écriture réservée.
create policy "affiches_lecture_publique" on public.affiches
  for select to anon, authenticated using (publique = true);

create policy "affiches_ecriture_equipe" on public.affiches
  for all to authenticated using (public.est_equipe()) with check (public.est_equipe());

-- Equipe : personne ne la lit par l'API ; elle ne sert qu'à est_equipe().
create policy "equipe_lecture_soi" on public.equipe
  for select to authenticated
  using (lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')));

-- 4. Index utiles au tableau de bord.
create index if not exists prieres_statut_cree on public.prieres (statut, cree_le desc);
create index if not exists temoignages_statut_cree on public.temoignages (statut, cree_le desc);
create index if not exists affiches_date on public.affiches (date_iso desc nulls last);

-- 5. Anti-abus minimal : borne de dépôt par adresse (le site a déjà un
--    limiteur côté client ; ceci protège la base si le formulaire est appelé direct).
create table if not exists public.depots_recents (
  id       bigserial primary key,
  ip_hash  text not null,
  nature   text not null check (nature in ('priere', 'temoignage')),
  cree_le  timestamptz not null default now()
);
alter table public.depots_recents enable row level security;

create or replace function public.enregistrer_depot(p_ip_hash text, p_nature text)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  recents integer;
begin
  select count(*) into recents
  from public.depots_recents d
  where d.ip_hash = p_ip_hash and d.cree_le > now() - interval '1 hour';

  if recents >= 5 then
    return false;
  end if;

  insert into public.depots_recents (ip_hash, nature) values (p_ip_hash, p_nature);
  return true;
end;
$$;

-- Nettoyage périodique (à lancer par un cron Supabase, une fois par jour) :
-- delete from public.depots_recents where cree_le < now() - interval '7 days';

-- 6. Inscriptions aux programmes (jeûne de novembre 2026, puis suivants).
--    Dépôt public en insertion seule ; lecture réservée à l'équipe.
--    Un même numéro ne s'inscrit qu'une fois par programme (réponse 409 côté site).
create table if not exists public.inscriptions_jeune (
  id           uuid primary key default gen_random_uuid(),
  programme    text not null default 'jeune-14-jours-nov-2026'
                 check (char_length(programme) between 3 and 60),
  nom          text not null check (char_length(btrim(nom)) between 1 and 80),
  prenom       text not null check (char_length(btrim(prenom)) between 1 and 80),
  quartier     text not null check (char_length(btrim(quartier)) between 1 and 80),
  telephone    text not null check (telephone ~ '^[+0-9 .()-]{8,20}$'),
  consentement boolean not null default false,
  cree_le      timestamptz not null default now(),
  unique (programme, telephone)
);

alter table public.inscriptions_jeune enable row level security;

create policy "inscriptions_depot_public" on public.inscriptions_jeune
  for insert to anon, authenticated
  with check (consentement = true);

create policy "inscriptions_lecture_equipe" on public.inscriptions_jeune
  for select to authenticated using (public.est_equipe());

create policy "inscriptions_suppression_equipe" on public.inscriptions_jeune
  for delete to authenticated using (public.est_equipe());

create index if not exists inscriptions_programme_cree
  on public.inscriptions_jeune (programme, cree_le desc);

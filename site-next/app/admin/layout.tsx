import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { config } from "@/lib/config";

export const metadata: Metadata = { title: "Administration", robots: { index: false, follow: false } };
export const dynamic = "force-dynamic";

const LIENS = [
  { href: "/admin", libelle: "Tableau de bord" },
  { href: "/admin/predications/tous-les-grands-ont-reve-grand", libelle: "Prédications" },
  { href: "/admin/prieres", libelle: "Prières et témoignages" },
];

/**
 * L'administration réelle passera par Supabase Auth + l'API de Hermes, qui
 * vérifie les droits à chaque appel. Tant que ce n'est pas branché, seul un
 * APERÇU en lecture seule existe, et uniquement en local (CAD_ADMIN_APERCU=1,
 * jamais en production). Il n'y a ici aucune fausse connexion.
 */
export default function LayoutAdmin({ children }: { children: React.ReactNode }) {
  if (!config.adminApercu) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-nuit px-6 text-center text-sur-nuit">
        <h1 className="m-0 font-titre text-4xl font-black uppercase">Administration</h1>
        <p className="m-0 max-w-[32em] text-creme">La connexion de l’administration sera ouverte dès que l’API sécurisée sera en service.</p>
        <Link href="/" className="font-bold text-or">Revenir au site →</Link>
      </main>
    );
  }
  return (
    <div className="flex min-h-screen flex-wrap bg-[#F6F2EC]">
      <nav aria-label="Administration" className="box-border flex max-w-[280px] flex-[1_1_240px] flex-col gap-1 bg-nuit px-4 py-6 text-creme">
        <Image src="/img/cad-logo-blanc.png" alt="Centre des Amoureux de Dieu" width={800} height={350} className="mx-2 mb-6 h-[38px] w-auto self-start" />
        {LIENS.map((l) => (
          <Link key={l.href} href={l.href} className="flex min-h-11 items-center rounded-[10px] px-3 font-semibold text-creme no-underline hover:bg-[#2A2019] hover:text-sur-nuit">{l.libelle}</Link>
        ))}
        <p className="mx-3 mt-6 rounded-xl border border-dashed border-bordure-nuit p-3 text-xs leading-normal text-gris-clair">
          Aperçu local, lecture seule. Les enregistrements seront actifs avec l’API de Hermes.
        </p>
      </nav>
      <main className="box-border flex min-w-0 flex-[999_1_560px] flex-col gap-7 px-5 py-8 sm:px-10">{children}</main>
    </div>
  );
}

import Link from "next/link";
import Image from "next/image";
import { classesBouton } from "@/components/ui";
import { MenuMobile } from "@/components/menu-mobile";
import { NavigationPrincipale, EnveloppeEntete } from "@/components/entete-client";

export const NAVIGATION = [
  { href: "/le-centre", libelle: "Le Centre" },
  { href: "/le-prophete", libelle: "Le Prophète" },
  { href: "/programmes", libelle: "Programmes" },
  { href: "/predications", libelle: "Prédications" },
  { href: "/temoignages", libelle: "Témoignages" },
  { href: "/priere", libelle: "Prière" },
  { href: "/nous-rejoindre", libelle: "Nous rejoindre" },
];

export function Entete() {
  return (
    <EnveloppeEntete>
      <a href="#contenu" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-ivoire focus:px-4 focus:py-2 focus:text-encre">
        Aller au contenu
      </a>
      <header className="relative mx-auto flex max-w-[1200px] items-center gap-6 px-5 py-3 sm:px-8">
        <Link href="/" aria-label="Centre des Amoureux de Dieu — accueil" className="shrink-0">
          <Image src="/img/cad-logo-blanc.png" alt="Centre des Amoureux de Dieu" width={800} height={350} priority className="h-8 w-auto sm:h-10" />
        </Link>
        <NavigationPrincipale liens={NAVIGATION} />
        <Link href="/dons" className={`${classesBouton("flamme")} ml-auto hidden sm:inline-flex lg:ml-0`}>Faire un don</Link>
        <MenuMobile liens={[...NAVIGATION, { href: "/dons", libelle: "Faire un don" }]} />
      </header>
    </EnveloppeEntete>
  );
}

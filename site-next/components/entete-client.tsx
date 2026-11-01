"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

/** En-tête collant : transparent en haut de page, voilé et flouté dès qu'on descend. */
export function EnveloppeEntete({ children }: { children: React.ReactNode }) {
  const [defile, setDefile] = useState(false);
  useEffect(() => {
    const maj = () => setDefile(window.scrollY > 12);
    maj();
    window.addEventListener("scroll", maj, { passive: true });
    return () => window.removeEventListener("scroll", maj);
  }, []);
  return (
    <div
      className={`sticky top-0 z-40 text-sur-nuit transition-[background-color,box-shadow,backdrop-filter] duration-500 ${
        defile ? "bg-nuit/85 shadow-[0_1px_0_#2E241C] backdrop-blur-xl" : "bg-nuit"
      }`}
    >
      <div className="filet-marque" />
      {children}
    </div>
  );
}

export function NavigationPrincipale({ liens }: { liens: { href: string; libelle: string }[] }) {
  const chemin = usePathname();
  return (
    <nav aria-label="Navigation principale" className="ml-auto hidden lg:block">
      <ul className="m-0 flex list-none gap-6 p-0 text-[13.5px] font-semibold">
        {liens.map((l) => {
          const actif = chemin === l.href || chemin.startsWith(l.href + "/");
          return (
            <li key={l.href}>
              <Link href={l.href} aria-current={actif ? "page" : undefined} className={`lien-trace inline-block py-1.5 no-underline ${actif ? "text-or" : "text-sur-nuit hover:text-or"}`}>
                {l.libelle}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

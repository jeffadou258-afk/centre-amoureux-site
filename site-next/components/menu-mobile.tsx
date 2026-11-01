"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

export function MenuMobile({ liens }: { liens: { href: string; libelle: string }[] }) {
  const [ouvert, setOuvert] = useState(false);
  const chemin = usePathname();
  useEffect(() => setOuvert(false), [chemin]);
  useEffect(() => {
    if (!ouvert) return;
    const fermer = (e: KeyboardEvent) => e.key === "Escape" && setOuvert(false);
    document.addEventListener("keydown", fermer);
    return () => document.removeEventListener("keydown", fermer);
  }, [ouvert]);

  return (
    <div className="lg:hidden">
      <button
        type="button"
        aria-expanded={ouvert}
        aria-controls="menu-principal"
        aria-label={ouvert ? "Fermer le menu" : "Ouvrir le menu"}
        onClick={() => setOuvert((o) => !o)}
        className="flex h-11 w-11 items-center justify-center rounded-xl border-[1.5px] border-bordure-nuit bg-transparent text-sur-nuit"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          {ouvert ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
        </svg>
      </button>
      {ouvert && (
        <nav id="menu-principal" style={{ ["--d" as string]: "0ms" }} aria-label="Navigation principale" className="entree absolute inset-x-0 top-full z-40 border-t border-nuit-ligne bg-nuit px-5 pb-6 shadow-2xl">
          <ul className="m-0 list-none p-0">
            {liens.map((l) => (
              <li key={l.href} className="border-b border-nuit-ligne">
                <Link href={l.href} className="flex min-h-[50px] items-center text-[15px] font-semibold text-sur-nuit no-underline">{l.libelle}</Link>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
}

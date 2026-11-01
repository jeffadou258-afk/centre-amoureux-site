"use client";

import { useRef, useState, useEffect } from "react";

/** Rangée horizontale à défilement aimanté, avec flèches précédent / suivant. */
export function Carrousel({ children, libelle }: { children: React.ReactNode; libelle: string }) {
  const piste = useRef<HTMLDivElement>(null);
  const [bords, setBords] = useState({ debut: true, fin: false });

  useEffect(() => {
    const el = piste.current;
    if (!el) return;
    const maj = () => setBords({ debut: el.scrollLeft < 8, fin: el.scrollLeft + el.clientWidth > el.scrollWidth - 8 });
    maj();
    el.addEventListener("scroll", maj, { passive: true });
    window.addEventListener("resize", maj);
    return () => { el.removeEventListener("scroll", maj); window.removeEventListener("resize", maj); };
  }, []);

  const aller = (sens: 1 | -1) => {
    const el = piste.current;
    if (el) el.scrollBy({ left: sens * el.clientWidth * 0.8, behavior: "smooth" });
  };

  const fleche = "flex h-11 w-11 items-center justify-center rounded-full border-[1.5px] border-[#D4C6B6] bg-white text-encre transition hover:border-encre disabled:opacity-35 disabled:hover:border-[#D4C6B6]";
  return (
    <div className="flex flex-col gap-5">
      <div ref={piste} role="region" aria-label={libelle} tabIndex={0} className="carrousel -mx-5 flex scroll-px-5 gap-5 overflow-x-auto px-5 pb-2 sm:-mx-8 sm:scroll-px-8 sm:px-8">
        {children}
      </div>
      <div className="flex gap-2">
        <button type="button" className={fleche} onClick={() => aller(-1)} disabled={bords.debut} aria-label="Messages précédents">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M15 5l-7 7 7 7" /></svg>
        </button>
        <button type="button" className={fleche} onClick={() => aller(1)} disabled={bords.fin} aria-label="Messages suivants">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M9 5l7 7-7 7" /></svg>
        </button>
      </div>
    </div>
  );
}

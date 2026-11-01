"use client";

import { useState } from "react";

type Valeur = { nom: string; definition: string; reference: string };

/** Les six valeurs : on choisit à gauche, la définition s'affiche en grand à droite. */
export function Valeurs({ valeurs }: { valeurs: readonly Valeur[] }) {
  const [actif, setActif] = useState(0);
  const v = valeurs[actif];
  return (
    <div className="grid gap-8 md:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] md:gap-14">
      <div role="tablist" aria-label="Nos valeurs" aria-orientation="vertical" className="flex flex-wrap gap-2 md:flex-col md:gap-0">
        {valeurs.map((x, i) => (
          <button
            key={x.nom}
            role="tab"
            id={`valeur-${i}`}
            aria-selected={i === actif}
            aria-controls="valeur-panneau"
            tabIndex={i === actif ? 0 : -1}
            onClick={() => setActif(i)}
            onKeyDown={(e) => {
              const n = valeurs.length;
              if (["ArrowDown", "ArrowRight"].includes(e.key)) { e.preventDefault(); setActif((actif + 1) % n); document.getElementById(`valeur-${(actif + 1) % n}`)?.focus(); }
              if (["ArrowUp", "ArrowLeft"].includes(e.key)) { e.preventDefault(); setActif((actif - 1 + n) % n); document.getElementById(`valeur-${(actif - 1 + n) % n}`)?.focus(); }
            }}
            className={`group relative cursor-pointer rounded-full border-[1.5px] px-4 py-2 text-left text-sm font-semibold transition md:rounded-none md:border-0 md:border-b md:border-ligne md:px-0 md:py-4 md:text-[17px] ${
              i === actif ? "border-encre bg-encre text-white md:bg-transparent md:text-encre" : "border-ligne bg-white text-gris hover:text-encre md:bg-transparent"
            }`}
          >
            <span className={`absolute -left-5 top-1/2 hidden h-2 w-2 -translate-y-1/2 rounded-full bg-flamme transition-transform duration-300 md:block ${i === actif ? "scale-100" : "scale-0"}`} aria-hidden="true" />
            {x.nom}
          </button>
        ))}
      </div>
      <div id="valeur-panneau" role="tabpanel" aria-labelledby={`valeur-${actif}`} className="relative flex min-h-[220px] flex-col justify-center gap-4 overflow-hidden rounded-3xl bg-nuit p-8 text-sur-nuit sm:p-10">
        <div className="braises opacity-60" aria-hidden="true" />
        <div key={actif} className="entree relative flex flex-col gap-4" style={{ ["--d" as string]: "0ms" }}>
          <p className="m-0 font-titre text-2xl font-bold text-or">{v.nom}</p>
          <p className="m-0 font-verset text-[clamp(1.35rem,2.4vw,1.8rem)] leading-snug">{v.definition}</p>
          <p className="m-0 text-[13px] font-semibold text-creme">{v.reference}</p>
        </div>
      </div>
    </div>
  );
}

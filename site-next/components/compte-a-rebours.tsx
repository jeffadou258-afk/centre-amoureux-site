"use client";

import { useEffect, useState } from "react";

/**
 * Compte à rebours jusqu'au prochain culte du dimanche (14h00 – 18h30, heure
 * d'Abidjan = UTC toute l'année). Pendant le culte, affiche « en ce moment ».
 * Rendu vide côté serveur pour éviter tout décalage d'horloge à l'hydratation.
 */
const DEBUT_H = 14;
const FIN_H = 18.5;

function etat(maintenant: Date) {
  const j = maintenant.getUTCDay();
  const h = maintenant.getUTCHours() + maintenant.getUTCMinutes() / 60;
  if (j === 0 && h >= DEBUT_H && h < FIN_H) return { enCours: true as const };
  const cible = new Date(Date.UTC(maintenant.getUTCFullYear(), maintenant.getUTCMonth(), maintenant.getUTCDate(), DEBUT_H));
  let ecart = (7 - j) % 7;
  if (ecart === 0 && h >= DEBUT_H) ecart = 7;
  cible.setUTCDate(cible.getUTCDate() + ecart);
  const s = Math.max(0, Math.floor((cible.getTime() - maintenant.getTime()) / 1000));
  return { enCours: false as const, j: Math.floor(s / 86400), h: Math.floor((s % 86400) / 3600), m: Math.floor((s % 3600) / 60), s: s % 60 };
}

const deux = (n: number) => String(n).padStart(2, "0");

export function CompteARebours() {
  const [maintenant, setMaintenant] = useState<Date | null>(null);
  useEffect(() => {
    setMaintenant(new Date());
    const t = setInterval(() => setMaintenant(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  if (!maintenant) {
    return <p className="m-0 text-sm text-creme">Culte chaque dimanche, de 14h00 à 18h30.</p>;
  }
  const e = etat(maintenant);
  if (e.enCours) {
    return (
      <p className="m-0 flex items-center gap-3 text-sm font-semibold text-sur-nuit">
        <span className="pulsation inline-block h-2.5 w-2.5 rounded-full bg-[#3BD16F]" aria-hidden="true" />
        Le culte a lieu en ce moment, jusqu’à 18h30. Vous pouvez encore venir.
      </p>
    );
  }
  const unites: [number, string][] = [[e.j, "jours"], [e.h, "heures"], [e.m, "min"], [e.s, "s"]];
  return (
    <div className="flex flex-col gap-2">
      <p className="m-0 text-[13px] text-gris-clair">Prochain culte, dimanche 14h00</p>
      <p className="m-0 flex items-baseline gap-4" aria-live="off" aria-label={`Dans ${e.j} jours, ${e.h} heures et ${e.m} minutes`}>
        {unites.map(([v, u]) => (
          <span key={u} className="flex items-baseline gap-1">
            <span className="font-titre text-[28px] font-bold tabular-nums leading-none text-sur-nuit">{u === "jours" ? v : deux(v)}</span>
            <span className="text-xs text-gris-clair">{u}</span>
          </span>
        ))}
      </p>
    </div>
  );
}

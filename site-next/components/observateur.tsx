"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

/** Fait apparaître les blocs marqués `data-apparition` quand ils entrent à l'écran. */
export function ObservateurApparition() {
  const chemin = usePathname();
  useEffect(() => {
    const blocs = document.querySelectorAll<HTMLElement>("[data-apparition]:not(.visible)");
    if (!("IntersectionObserver" in window)) {
      blocs.forEach((b) => b.classList.add("visible"));
      return;
    }
    const obs = new IntersectionObserver(
      (entrees) => {
        for (const e of entrees) {
          if (e.isIntersecting) {
            e.target.classList.add("visible");
            obs.unobserve(e.target);
          }
        }
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 },
    );
    blocs.forEach((b) => obs.observe(b));
    return () => obs.disconnect();
  }, [chemin]);
  return null;
}

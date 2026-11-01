"use client";

import Image from "next/image";
import { useState } from "react";

/**
 * Lecteur chargé AU CLIC seulement (youtube-nocookie.com) : aucun appel à
 * YouTube, aucun traceur tant que le visiteur n'a pas choisi de regarder.
 */
export function LecteurYoutube({ id, titre, vignette }: { id: string; titre: string; vignette: string }) {
  const [actif, setActif] = useState(false);
  if (actif) {
    return (
      <iframe
        className="aspect-video w-full rounded-[20px] border-0 bg-black"
        src={`https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1&rel=0`}
        title={titre}
        allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
        allowFullScreen
      />
    );
  }
  return (
    <button type="button" onClick={() => setActif(true)} className="group relative block w-full cursor-pointer overflow-hidden rounded-[20px] border-0 bg-black p-0" aria-label={`Lire la vidéo : ${titre}`}>
      <Image src={vignette} alt="" width={1280} height={720} priority className="block aspect-video w-full object-cover opacity-90 group-hover:opacity-100" />
      <span className="absolute inset-0 flex items-center justify-center">
        <span className="flex h-20 w-20 items-center justify-center rounded-full bg-flamme">
          <svg width="28" height="28" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l13-7.5z" fill="#1A0E05" /></svg>
        </span>
      </span>
      <span className="absolute bottom-4 left-4 rounded-full bg-black/70 px-3 py-1 text-xs font-semibold text-white">La vidéo YouTube se charge au clic</span>
    </button>
  );
}

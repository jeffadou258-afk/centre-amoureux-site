import Link from "next/link";

export default function Introuvable() {
  return (
    <main className="flex min-h-[70vh] flex-col items-center justify-center gap-4 bg-nuit px-6 text-center text-sur-nuit">
      <p className="m-0 text-[13px] font-bold uppercase tracking-[0.14em] text-or">Page introuvable</p>
      <h1 className="m-0 font-titre text-5xl font-black uppercase">Cette page n’existe pas</h1>
      <Link href="/" className="font-bold text-or">Revenir à l’accueil →</Link>
    </main>
  );
}

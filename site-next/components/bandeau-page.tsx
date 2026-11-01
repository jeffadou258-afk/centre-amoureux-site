import { Conteneur, Surtitre } from "@/components/ui";

export function BandeauPage({ surtitre, titre, texte, children }: { surtitre: string; titre: string; texte?: string; children?: React.ReactNode }) {
  return (
    <section className="bg-nuit text-sur-nuit">
      <Conteneur className="flex flex-col gap-4 pb-12 pt-10">
        <Surtitre surNuit>{surtitre}</Surtitre>
        <h1 className="m-0 font-titre text-[clamp(2.1rem,8vw,4.5rem)] font-black uppercase leading-[0.95] tracking-[-0.02em] [overflow-wrap:anywhere] hyphens-auto">{titre}</h1>
        {texte && <p className="m-0 max-w-[40em] text-[17px] leading-relaxed text-creme">{texte}</p>}
        {children}
      </Conteneur>
    </section>
  );
}

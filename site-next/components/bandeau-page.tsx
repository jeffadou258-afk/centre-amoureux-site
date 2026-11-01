import { Conteneur, Surtitre } from "@/components/ui";

export function BandeauPage({ surtitre, titre, texte, children }: { surtitre: string; titre: string; texte?: string; children?: React.ReactNode }) {
  return (
    <section className="relative overflow-hidden bg-nuit text-sur-nuit">
      <div className="braises opacity-70" aria-hidden="true" />
      <Conteneur className="relative flex flex-col gap-4 pb-14 pt-12">
        <div className="entree" style={{ ["--d" as string]: "0ms" }}><Surtitre surNuit>{surtitre}</Surtitre></div>
        <h1 className="m-0 max-w-[20em] text-[clamp(1.85rem,4.4vw,3rem)] font-bold leading-[1.05] [overflow-wrap:anywhere] hyphens-auto">
          <span className="ligne-titre"><span>{titre}</span></span>
        </h1>
        {texte && <p className="entree m-0 max-w-[38em] text-base leading-relaxed text-creme" style={{ ["--d" as string]: "350ms" }}>{texte}</p>}
        {children && <div className="entree" style={{ ["--d" as string]: "500ms" }}>{children}</div>}
      </Conteneur>
    </section>
  );
}

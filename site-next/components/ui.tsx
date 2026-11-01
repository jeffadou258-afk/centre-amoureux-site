import Link from "next/link";

type Variante = "flamme" | "encre" | "contour-nuit" | "contour";

const VARIANTES: Record<Variante, string> = {
  flamme: "bg-flamme text-sur-flamme hover:bg-[#F27A22] hover:text-sur-flamme hover:shadow-[0_8px_24px_-8px_#ED6C10] font-bold",
  encre: "bg-encre text-white hover:bg-black hover:text-white font-semibold",
  "contour-nuit": "border-[1.5px] border-bordure-nuit text-sur-nuit hover:border-or hover:text-sur-nuit font-semibold",
  contour: "border-[1.5px] border-[#D4C6B6] bg-white text-encre hover:border-encre hover:text-encre font-semibold",
};

export function classesBouton(variante: Variante = "flamme", grand = false) {
  return `inline-flex items-center justify-center gap-2 rounded-full no-underline transition duration-300 hover:-translate-y-0.5 active:translate-y-0 ${
    grand ? "min-h-12 px-6 text-[15px]" : "min-h-10 px-5 text-[13.5px]"
  } ${VARIANTES[variante]}`;
}

export function Bouton({
  href, children, variante = "flamme", grand = false, externe = false,
}: { href: string; children: React.ReactNode; variante?: Variante; grand?: boolean; externe?: boolean }) {
  const classes = classesBouton(variante, grand);
  if (externe) return <a href={href} className={classes} target="_blank" rel="noopener">{children}</a>;
  return <Link href={href} className={classes}>{children}</Link>;
}

/** Petit repère au-dessus d'un titre : un trait de flamme et le nom de la rubrique. */
export function Surtitre({ children, surNuit = false }: { children: React.ReactNode; surNuit?: boolean }) {
  return (
    <p className={`m-0 flex items-center gap-2.5 text-[13px] font-semibold ${surNuit ? "text-or" : "text-flamme-encre"}`}>
      <span className="h-[2px] w-6 rounded-full bg-current" aria-hidden="true" />
      {children}
    </p>
  );
}

export function TitreSection({ children, as: Balise = "h2", className = "" }: { children: React.ReactNode; as?: "h1" | "h2"; className?: string }) {
  return (
    <Balise className={`m-0 font-titre font-bold leading-[1.08] text-[clamp(1.6rem,2.8vw,2.3rem)] ${className}`}>
      {children}
    </Balise>
  );
}

export function AConfirmer({ children = "à confirmer" }: { children?: React.ReactNode }) {
  return <span className="a-confirmer">{children}</span>;
}

export function Conteneur({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`mx-auto w-full max-w-[1200px] px-5 sm:px-8 ${className}`}>{children}</div>;
}

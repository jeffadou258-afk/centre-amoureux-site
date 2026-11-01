import Link from "next/link";

type Variante = "flamme" | "encre" | "contour-nuit" | "contour";

const VARIANTES: Record<Variante, string> = {
  flamme: "bg-flamme text-sur-flamme hover:bg-[#F27A22] hover:text-sur-flamme font-extrabold",
  encre: "bg-encre text-ivoire hover:bg-black hover:text-ivoire font-bold",
  "contour-nuit": "border-[1.5px] border-bordure-nuit text-sur-nuit hover:border-or hover:text-sur-nuit font-bold",
  contour: "border-[1.5px] border-[#D4C6B6] bg-white text-encre hover:border-encre hover:text-encre font-bold",
};

export function classesBouton(variante: Variante = "flamme", grand = false) {
  return `inline-flex items-center justify-center gap-2 rounded-full no-underline transition-colors ${
    grand ? "min-h-[52px] px-7 text-base" : "min-h-11 px-5 text-sm"
  } ${VARIANTES[variante]}`;
}

export function Bouton({
  href, children, variante = "flamme", grand = false, externe = false,
}: { href: string; children: React.ReactNode; variante?: Variante; grand?: boolean; externe?: boolean }) {
  const classes = classesBouton(variante, grand);
  if (externe) return <a href={href} className={classes} target="_blank" rel="noopener">{children}</a>;
  return <Link href={href} className={classes}>{children}</Link>;
}

export function Surtitre({ children, surNuit = false }: { children: React.ReactNode; surNuit?: boolean }) {
  return (
    <p className={`m-0 text-[13px] font-bold uppercase tracking-[0.14em] ${surNuit ? "text-or" : "text-flamme-encre"}`}>
      {children}
    </p>
  );
}

export function TitreSection({ children, as: Balise = "h2", className = "" }: { children: React.ReactNode; as?: "h1" | "h2"; className?: string }) {
  return (
    <Balise className={`m-0 font-titre font-black uppercase leading-none tracking-[-0.02em] text-[clamp(2rem,4vw,3rem)] ${className}`}>
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

import { Entete } from "@/components/entete";
import { PiedDePage } from "@/components/pied-de-page";
import { ObservateurApparition } from "@/components/observateur";
import { getSite } from "@/lib/donnees";

export default async function LayoutSite({ children }: { children: React.ReactNode }) {
  const site = await getSite();
  return (
    <>
      <Entete />
      <main id="contenu">{children}</main>
      <PiedDePage site={site} />
      <ObservateurApparition />
    </>
  );
}

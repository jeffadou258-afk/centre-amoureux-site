import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getPredication } from "@/lib/donnees";
import { dateLongue } from "@/lib/format";

const champ = "min-h-[52px] w-full rounded-xl border-[1.5px] border-champ bg-white px-4 text-base";

export default async function EditeurPredication({ params }: { params: Promise<{ slug: string }> }) {
  const p = await getPredication((await params).slug);
  if (!p) notFound();
  return (
    <>
      <div className="flex flex-col gap-1.5">
        <Link href="/admin" className="text-sm font-bold">← Tableau de bord</Link>
        <h1 className="m-0 font-titre text-3xl font-black uppercase">Modifier la prédication</h1>
      </div>
      <div className="flex flex-wrap items-start gap-6">
        <form className="flex min-w-0 flex-[999_1_480px] flex-col gap-5 rounded-2xl bg-white p-7" aria-describedby="lecture-seule">
          <div className="flex flex-col gap-1.5"><label htmlFor="e-titre" className="font-bold">Titre</label><input id="e-titre" defaultValue={p.titre} className={`${champ} text-[17px] font-semibold`} /></div>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="flex flex-col gap-1.5"><label htmlFor="e-type" className="font-bold">Type</label><select id="e-type" defaultValue={p.type} className={`${champ} px-3`}><option>Enseignement</option><option>Exhortation</option><option>Prière</option><option>Culte</option></select></div>
            <div className="flex flex-col gap-1.5"><label htmlFor="e-date" className="font-bold">Date</label><input id="e-date" type="date" defaultValue={p.date} className={champ} /></div>
            <div className="flex flex-col gap-1.5"><label htmlFor="e-orateur" className="font-bold">Orateur</label><input id="e-orateur" defaultValue={p.orateur} className={champ} /></div>
          </div>
          <div className="flex flex-col gap-1.5"><label htmlFor="e-yt" className="font-bold">Lien de la vidéo YouTube</label><input id="e-yt" type="url" defaultValue={`https://www.youtube.com/watch?v=${p.youtube_id}`} className={champ} /></div>
          <div className="flex flex-col gap-1.5"><label htmlFor="e-serie" className="font-bold">Série <span className="font-medium text-gris">(facultatif)</span></label><input id="e-serie" defaultValue={p.serie ?? ""} className={champ} /></div>
          <div className="flex flex-col gap-1.5"><label htmlFor="e-resume" className="font-bold">Résumé pour les visiteurs</label><textarea id="e-resume" rows={5} defaultValue={p.resume ?? ""} placeholder="Trois à cinq phrases : ce que le message enseigne et à qui il s’adresse." className={`${champ} py-3`} /></div>
          <div className="flex flex-col gap-1.5"><label htmlFor="e-versets" className="font-bold">Versets cités</label><input id="e-versets" defaultValue={p.versets.join(" ; ")} placeholder="Ex. : Genèse 37 : 5 ; Habacuc 2 : 2" className={champ} /></div>
        </form>
        <aside className="flex max-w-[380px] flex-[1_1_320px] flex-col gap-4">
          <div className="flex flex-col gap-3.5 rounded-2xl bg-white p-6">
            <h2 className="m-0 text-[17px] font-extrabold">Publication</h2>
            <button type="button" disabled aria-describedby="lecture-seule" className="min-h-[52px] cursor-not-allowed rounded-full border-0 bg-flamme font-extrabold text-sur-flamme opacity-50">Enregistrer</button>
            <p id="lecture-seule" className="m-0 text-[13px] leading-normal text-gris">Aperçu en lecture seule : l’enregistrement sera actif avec l’API de Hermes (<code>PATCH /v1/admin/predications</code>). La page publique sera alors mise à jour en moins d’une minute.</p>
          </div>
          <div className="flex flex-col gap-2.5 rounded-2xl bg-white p-5">
            <h2 className="m-0 text-[15px] font-extrabold">Aperçu de la carte</h2>
            <Image src={p.vignette} alt="" width={640} height={360} className="aspect-video w-full rounded-xl object-cover" />
            <span className="text-xs font-semibold text-gris">{p.type} · {dateLongue(p.date)}</span>
            <span className="font-titre text-[19px] font-extrabold uppercase leading-tight">{p.titre}</span>
          </div>
        </aside>
      </div>
    </>
  );
}

export default function Moderation() {
  return (
    <>
      <div className="flex flex-col gap-1.5">
        <h1 className="m-0 font-titre text-3xl font-black uppercase">Prières et témoignages</h1>
        <p className="m-0 text-sm text-gris">Visibles seulement par les rôles autorisés. Les demandes de prière ne sont jamais publiées.</p>
      </div>
      <section className="flex max-w-[640px] flex-col gap-3 rounded-2xl bg-white p-7">
        <span className="text-xs font-bold uppercase tracking-[0.12em] text-gris">État réel</span>
        <span className="font-titre text-[22px] font-extrabold">Aucune demande ni témoignage pour l’instant</span>
        <span className="leading-normal text-texte-2">Les envois du site arriveront ici dès que l’API de Hermes sera branchée (<code>GET /v1/admin/prieres</code>, <code>GET /v1/admin/temoignages</code>). Rien n’est simulé.</span>
      </section>
    </>
  );
}

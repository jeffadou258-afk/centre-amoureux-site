import Image from "next/image";
import Link from "next/link";
import { Bouton, Conteneur, Surtitre, TitreSection } from "@/components/ui";
import { CartePredicationVedette, LignePredication } from "@/components/predications";
import { getEvenementsAVenir, getPredications, getSite } from "@/lib/donnees";
import { MISSION, PROPHETE, VALEURS, VISION } from "@/lib/contenu";
import { blocDate, periode } from "@/lib/format";

export default async function Accueil() {
  const [site, predications, evenements] = await Promise.all([getSite(), getPredications(), getEvenementsAVenir()]);
  const [vedette, ...autres] = predications;
  const affiche = evenements.find((e) => e.mise_en_avant && e.affiche);

  return (
    <>
      {/* Héros */}
      <section className="bg-nuit text-sur-nuit">
        <Conteneur className="grid items-center gap-14 pb-16 pt-10 md:grid-cols-2 md:pb-20 md:pt-14">
          <div className="flex flex-col gap-6">
            <Surtitre surNuit>Église · {site.adresse.split(",")[0]}, Abidjan · depuis {site.fondation}</Surtitre>
            <h1 className="m-0 font-titre text-[clamp(2.75rem,6vw,5rem)] font-black uppercase leading-[0.95] tracking-[-0.02em]">
              Une armée d’amoureux <span className="text-flamme">passionnés</span> pour Dieu.
            </h1>
            <p className="m-0 max-w-[34em] text-lg leading-relaxed text-creme">{VISION}</p>
            <div className="flex flex-wrap gap-3">
              <Bouton href="/nous-rejoindre" grand>Préparer ma visite</Bouton>
              <Bouton href="/predications" variante="contour-nuit" grand>Regarder les prédications</Bouton>
            </div>
          </div>
          <div className="relative flex justify-center">
            <Image src="/img/prophete-bras-croises.jpg" alt={PROPHETE.nom} width={720} height={960} priority sizes="(min-width: 768px) 440px, 100vw" className="aspect-[3/4] w-full max-w-[440px] rounded-3xl object-cover" />
            <div className="absolute bottom-6 left-0 flex max-w-[260px] flex-col gap-0.5 rounded-2xl bg-ivoire px-5 py-4 text-encre sm:left-4">
              <span className="text-xs font-bold uppercase tracking-[0.12em] text-flamme-encre">Conduit par</span>
              <span className="font-titre text-xl font-extrabold">{PROPHETE.nom}</span>
            </div>
          </div>
        </Conteneur>
        <div className="border-t border-nuit-ligne">
          <Conteneur className="grid gap-6 py-6 sm:grid-cols-2 lg:grid-cols-4">
            {site.horaires.map((h) => (
              <div key={h.jour} className="flex flex-col gap-1">
                <span className="text-xs font-bold uppercase tracking-[0.12em] text-gris-clair">{h.jour} · {h.libelle}</span>
                <span className="font-titre text-2xl font-extrabold">{h.heures}</span>
                {h.precision && <span className="text-[13px] text-gris-clair">{h.precision}</span>}
              </div>
            ))}
            <div className="flex flex-col gap-1">
              <span className="text-xs font-bold uppercase tracking-[0.12em] text-gris-clair">Adresse</span>
              <span className="font-bold">{site.adresse}</span>
            </div>
            <div className="flex items-center">
              <Link href="/nous-rejoindre" className="font-bold text-or">Itinéraire et première visite →</Link>
            </div>
          </Conteneur>
        </div>
      </section>

      {/* Thème du mois */}
      {site.theme_du_mois && (
        <section>
          <Conteneur className="grid items-center gap-14 py-20 md:grid-cols-2">
            {affiche?.affiche && (
              <Image src={affiche.affiche} alt={`Affiche : ${affiche.titre}, ${periode(affiche.debut, affiche.fin)}${affiche.heure ? ` ${affiche.heure}` : ""}`} width={872} height={1080} sizes="(min-width: 768px) 480px, 100vw" className="w-full max-w-[480px] justify-self-center rounded-[20px]" />
            )}
            <div className="flex flex-col gap-5">
              <Surtitre>Thème du mois · {site.theme_du_mois.mois}</Surtitre>
              <TitreSection className="text-[clamp(2.1rem,4vw,3.25rem)]">{site.theme_du_mois.titre}</TitreSection>
              <ol className="m-0 mt-2 list-none border-t border-ligne p-0">
                {evenements.slice(0, 4).map((e) => {
                  const d = blocDate(e.debut);
                  return (
                    <li key={e.slug} className="grid grid-cols-[120px_1fr] gap-4 border-b border-ligne py-4 sm:grid-cols-[140px_1fr]">
                      <span className="font-titre text-[15px] font-extrabold text-flamme-encre">
                        {e.fin ? `${d.numero} – ${blocDate(e.fin).numero} ${d.mois.toLowerCase()}` : `${d.jour.charAt(0)}${d.jour.slice(1).toLowerCase()} ${d.numero} ${d.mois.toLowerCase()}`}
                      </span>
                      <span className="text-[15px] leading-normal">
                        <strong>{e.titre}</strong>
                        {e.heure && <> · {e.heure}</>}
                        {e.details && <> · {e.details}</>}
                      </span>
                    </li>
                  );
                })}
              </ol>
              <div className="flex flex-wrap items-center gap-4">
                <Bouton href="/programmes" variante="encre">Tout le programme</Bouton>
                {site.theme_du_mois.suivant && (
                  <span className="text-sm text-gris">
                    En {site.theme_du_mois.suivant.mois.split(" ")[0].toLowerCase()} : <em className="font-verset text-[19px] text-encre">{site.theme_du_mois.suivant.titre}</em>
                  </span>
                )}
              </div>
            </div>
          </Conteneur>
        </section>
      )}

      {/* Prédications */}
      {vedette && (
        <section className="bg-sable">
          <Conteneur className="flex flex-col gap-8 py-20">
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div className="flex flex-col gap-3">
                <Surtitre>Prédications</Surtitre>
                <TitreSection>La Parole de la semaine</TitreSection>
              </div>
              <Link href="/predications" className="font-bold">Toutes les prédications →</Link>
            </div>
            <div className="grid gap-6 lg:grid-cols-3">
              <div className="lg:col-span-2"><CartePredicationVedette p={vedette} /></div>
              <div className="flex min-w-0 flex-col gap-4">
                {autres.slice(0, 3).map((p) => <LignePredication key={p.slug} p={p} />)}
                <p className="m-0 text-[13px] text-gris">La vidéo ne se charge qu’au clic, sans traceur.</p>
              </div>
            </div>
          </Conteneur>
        </section>
      )}

      {/* Le Prophète */}
      <section>
        <Conteneur className="grid items-center gap-14 py-20 md:grid-cols-2">
          <Image src="/img/prophete-face.jpg" alt={`Portrait du ${PROPHETE.nom}`} width={720} height={960} sizes="(min-width: 768px) 460px, 100vw" className="aspect-[4/5] w-full max-w-[460px] rounded-3xl object-cover" />
          <div className="flex flex-col gap-5">
            <Surtitre>Le Prophète</Surtitre>
            <TitreSection>{PROPHETE.nomCourt}</TitreSection>
            <p className="m-0 text-[17px] leading-[1.7] text-texte-2">
              Le Centre des Amoureux de Dieu est conduit par le {PROPHETE.nom}, dont l’enseignement est diffusé chaque semaine sur la chaîne du ministère.
            </p>
            <blockquote className="m-0 mt-2 font-verset text-[28px] italic leading-snug">
              « Pour nous, nous l’aimons, parce qu’il nous a aimés le premier. »
              <footer className="mt-2.5 font-texte text-[13px] font-bold not-italic tracking-[0.1em] text-flamme-encre">1 JEAN 4 : 19</footer>
            </blockquote>
            <Link href="/le-prophete" className="font-bold">Découvrir son ministère →</Link>
          </div>
        </Conteneur>
      </section>

      {/* Mission et valeurs */}
      <section className="border-y border-ligne bg-white">
        <Conteneur className="flex flex-col gap-8 py-20">
          <div className="flex max-w-[760px] flex-col gap-3">
            <Surtitre>Notre mission</Surtitre>
            <p className="m-0 text-xl font-medium leading-relaxed">{MISSION}</p>
          </div>
          <ul className="m-0 grid list-none border-t border-ligne p-0 sm:grid-cols-2 lg:grid-cols-3">
            {VALEURS.map((v) => (
              <li key={v.nom} className="flex flex-col gap-1.5 border-b border-ligne py-6 pr-6">
                <span className="font-titre text-[22px] font-extrabold">{v.nom}</span>
                <span className="text-[15px] leading-normal text-texte-2">{v.definition}</span>
                <span className="text-[13px] font-bold text-flamme-encre">{v.reference}</span>
              </li>
            ))}
          </ul>
        </Conteneur>
      </section>

      {/* Prière */}
      <section className="bg-nuit text-sur-nuit">
        <Conteneur className="grid items-center gap-10 py-20 md:grid-cols-2">
          <div className="flex flex-col gap-4">
            <Surtitre surNuit>Prière</Surtitre>
            <TitreSection className="text-[clamp(2rem,4vw,3.25rem)]">Un fardeau à déposer ?</TitreSection>
            <p className="m-0 text-[17px] leading-relaxed text-creme">Écrivez librement. Votre demande reste confidentielle et n’est jamais publiée.</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Bouton href="/priere" grand>Envoyer une demande de prière</Bouton>
            <Bouton href="/temoignages" variante="contour-nuit" grand>Partager un témoignage</Bouton>
          </div>
        </Conteneur>
      </section>
    </>
  );
}

import Image from "next/image";
import Link from "next/link";
import { Bouton, Conteneur, Surtitre, TitreSection } from "@/components/ui";
import { CartePredication, CartePredicationVedette } from "@/components/predications";
import { CompteARebours } from "@/components/compte-a-rebours";
import { Carrousel } from "@/components/carrousel";
import { Valeurs } from "@/components/valeurs";
import { getEvenementsAVenir, getPredications, getSite } from "@/lib/donnees";
import { MISSION, PROPHETE, VALEURS, VISION } from "@/lib/contenu";
import { blocDate, periode } from "@/lib/format";
import type { Evenement } from "@/lib/api/contrats";

function dateEvenement(e: Evenement) {
  const d = blocDate(e.debut);
  const mois = d.mois.toLowerCase();
  return e.fin ? `${d.numero} – ${blocDate(e.fin).numero} ${mois}` : `${d.numero} ${mois}`;
}

const d = (ms: number) => ({ ["--d" as string]: `${ms}ms` });

export default async function Accueil() {
  const [site, predications, evenements] = await Promise.all([getSite(), getPredications(), getEvenementsAVenir()]);
  const [vedette, ...autres] = predications;
  const affiche = evenements.find((e) => e.mise_en_avant && e.affiche);
  const quartier = site.adresse.split(",")[0];

  return (
    <>
      {/* ── Héros ─────────────────────────────────────────────────────── */}
      <section className="relative -mt-px overflow-hidden bg-nuit text-sur-nuit">
        <div className="braises" aria-hidden="true" />
        <Conteneur className="relative grid items-center gap-12 pb-16 pt-10 md:grid-cols-[minmax(0,7fr)_minmax(0,5fr)] md:pb-24 md:pt-16">
          <div className="flex flex-col gap-6">
            <div className="entree" style={d(0)}>
              <Surtitre surNuit>Église à {quartier}, Abidjan, depuis {site.fondation}</Surtitre>
            </div>
            <h1 className="m-0 text-[clamp(2rem,4.2vw,3.25rem)] font-bold leading-[1.04]">
              <span className="ligne-titre" style={{ ["--i" as string]: 0 }}><span>Une armée d’amoureux</span></span>
              <span className="ligne-titre" style={{ ["--i" as string]: 1 }}><span>passionnés pour Dieu,</span></span>
              <span className="ligne-titre" style={{ ["--i" as string]: 2 }}><span className="bg-gradient-to-r from-or via-flamme to-[#F0503A] bg-clip-text text-transparent">équipés pour impacter.</span></span>
            </h1>
            <p className="entree m-0 max-w-[34em] text-base leading-relaxed text-creme" style={d(550)}>{VISION}</p>
            <div className="entree flex flex-wrap gap-3" style={d(700)}>
              <Bouton href="/nous-rejoindre" grand>Préparer ma visite</Bouton>
              <Bouton href="/predications" variante="contour-nuit" grand>Regarder les prédications</Bouton>
            </div>
            <div className="entree mt-2 max-w-md rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur-md" style={d(850)}>
              <CompteARebours />
            </div>
          </div>
          <div className="entree relative justify-self-center" style={d(300)}>
            <div className="absolute -inset-3 rounded-[32px] border border-or/30" aria-hidden="true" />
            <div className="relative overflow-hidden rounded-[28px]">
              <Image src="/img/prophete-bras-croises.jpg" alt={PROPHETE.nom} width={720} height={960} priority sizes="(min-width: 768px) 420px, 100vw" className="zoom-lent aspect-[3/4] w-full max-w-[420px] object-cover" />
              <div className="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-nuit/90 to-transparent" aria-hidden="true" />
              <div className="absolute bottom-5 left-5 right-5 flex flex-col">
                <span className="text-xs text-or">Conduit par</span>
                <span className="font-titre text-lg font-bold">{PROPHETE.nom}</span>
              </div>
            </div>
          </div>
        </Conteneur>
      </section>

      {/* ── Bandeau défilant du programme ─────────────────────────────── */}
      {evenements.length > 0 && (
        <div className="overflow-hidden border-y border-[#C9560A] bg-flamme py-3 text-sur-flamme">
          <div className="defilant">
            {[0, 1].map((copie) => (
              <ul key={copie} aria-hidden={copie === 1 || undefined} className="m-0 flex shrink-0 list-none items-center gap-10 p-0 pr-10 text-sm font-semibold">
                {evenements.map((e) => (
                  <li key={e.slug} className="flex items-center gap-3 whitespace-nowrap">
                    <span className="font-titre font-bold">{dateEvenement(e)}</span>
                    <span>{e.titre}</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" className="ml-7 opacity-60"><path d="M12 2c1 4 5 6 5 11a5 5 0 0 1-10 0c0-3 2-4 2-7 2 1 3 3 3 5 1-2 0-6 0-9z" fill="currentColor" /></svg>
                  </li>
                ))}
              </ul>
            ))}
          </div>
        </div>
      )}

      {/* ── Thème du mois ─────────────────────────────────────────────── */}
      {site.theme_du_mois && (
        <section>
          <Conteneur className="grid items-center gap-12 py-20 md:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] md:gap-16">
            {affiche?.affiche && (
              <div data-apparition className="group justify-self-center [perspective:1200px]">
                <Image
                  src={affiche.affiche}
                  alt={`Affiche : ${affiche.titre}, ${periode(affiche.debut, affiche.fin)}${affiche.heure ? ` ${affiche.heure}` : ""}`}
                  width={872} height={1080} sizes="(min-width: 768px) 420px, 100vw"
                  className="w-full max-w-[420px] rounded-3xl shadow-[0_30px_60px_-25px_rgba(18,12,8,.55)] transition-transform duration-700 ease-[cubic-bezier(.16,1,.3,1)] group-hover:[transform:rotateY(-6deg)_rotateX(3deg)_scale(1.02)]"
                />
              </div>
            )}
            <div className="flex flex-col gap-5">
              <div data-apparition className="flex flex-col gap-4">
                <Surtitre>Thème de {site.theme_du_mois.mois.split(" ")[0].toLowerCase()}</Surtitre>
                <TitreSection>{site.theme_du_mois.titre}</TitreSection>
              </div>
              <ol className="relative m-0 mt-2 list-none p-0 before:absolute before:bottom-3 before:left-[5px] before:top-3 before:w-px before:bg-ligne">
                {evenements.slice(0, 4).map((e, i) => (
                  <li key={e.slug} data-apparition style={d(i * 90)} className="relative grid grid-cols-[96px_1fr] gap-4 py-3.5 pl-7 sm:grid-cols-[120px_1fr]">
                    <span className="absolute left-0 top-[22px] h-[11px] w-[11px] rounded-full border-2 border-flamme bg-white" aria-hidden="true" />
                    <span className="font-titre text-sm font-bold text-flamme-encre">{dateEvenement(e)}</span>
                    <span className="text-sm leading-normal">
                      <strong className="font-semibold">{e.titre}</strong>
                      {e.heure && <span className="text-gris">, {e.heure}</span>}
                      {e.details && <span className="block text-gris">{e.details}</span>}
                    </span>
                  </li>
                ))}
              </ol>
              <div data-apparition className="flex flex-wrap items-center gap-4">
                <Bouton href="/programmes" variante="encre">Tout le programme</Bouton>
                {site.theme_du_mois.suivant && (
                  <span className="text-sm text-gris">
                    En {site.theme_du_mois.suivant.mois.split(" ")[0].toLowerCase()} : <em className="font-verset text-[17px] text-encre">{site.theme_du_mois.suivant.titre}</em>
                  </span>
                )}
              </div>
            </div>
          </Conteneur>
        </section>
      )}

      {/* ── Prédications ──────────────────────────────────────────────── */}
      {vedette && (
        <section className="overflow-hidden bg-sable">
          <Conteneur className="flex flex-col gap-10 py-20">
            <div data-apparition className="flex flex-wrap items-end justify-between gap-4">
              <div className="flex flex-col gap-3">
                <Surtitre>Prédications</Surtitre>
                <TitreSection>La Parole de la semaine</TitreSection>
              </div>
              <Link href="/predications" className="lien-trace text-sm font-semibold text-encre">Toutes les prédications</Link>
            </div>
            <div data-apparition className="grid items-center gap-8 lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)]">
              <CartePredicationVedette p={vedette} />
              <div className="flex flex-col gap-3">
                <p className="m-0 text-[13px] text-gris">Le message le plus récent</p>
                <p className="m-0 font-titre text-xl font-bold leading-snug">{vedette.titre}</p>
                <p className="m-0 text-sm leading-relaxed text-texte-2">
                  Par le {vedette.orateur}. La vidéo se charge seulement quand vous appuyez sur lecture, sans traceur publicitaire.
                </p>
                <div className="mt-2"><Bouton href={`/predications/${vedette.slug}`}>Regarder le message</Bouton></div>
              </div>
            </div>
            {autres.length > 0 && (
              <div data-apparition>
                <Carrousel libelle="Autres prédications">
                  {autres.map((p) => <CartePredication key={p.slug} p={p} className="w-[78%] shrink-0 sm:w-[44%] lg:w-[30%]" />)}
                </Carrousel>
              </div>
            )}
          </Conteneur>
        </section>
      )}

      {/* ── Le Prophète ───────────────────────────────────────────────── */}
      <section>
        <Conteneur className="grid items-center gap-12 py-20 md:grid-cols-2 md:gap-16">
          <div data-apparition className="relative justify-self-center">
            <div className="absolute -bottom-4 -right-4 h-2/3 w-2/3 rounded-3xl bg-gradient-to-br from-or to-flamme opacity-90" aria-hidden="true" />
            <Image src="/img/prophete-face.jpg" alt={`Portrait du ${PROPHETE.nom}`} width={720} height={960} sizes="(min-width: 768px) 420px, 100vw" className="relative aspect-[4/5] w-full max-w-[420px] rounded-3xl object-cover" />
          </div>
          <div data-apparition style={d(120)} className="flex flex-col gap-5">
            <Surtitre>Le Prophète</Surtitre>
            <TitreSection>{PROPHETE.nomCourt}</TitreSection>
            <p className="m-0 text-base leading-[1.75] text-texte-2">
              Le Centre des Amoureux de Dieu est conduit par le {PROPHETE.nom}, dont l’enseignement est diffusé chaque semaine sur la chaîne du ministère.
            </p>
            <blockquote className="m-0 mt-1 border-l-2 border-flamme pl-5 font-verset text-[clamp(1.3rem,2.2vw,1.65rem)] italic leading-snug">
              « Pour nous, nous l’aimons, parce qu’il nous a aimés le premier. »
              <footer className="mt-2 font-texte text-[13px] font-semibold not-italic text-flamme-encre">1 Jean 4 : 19</footer>
            </blockquote>
            <div><Bouton href="/le-prophete" variante="contour">Découvrir son ministère</Bouton></div>
          </div>
        </Conteneur>
      </section>

      {/* ── Mission et valeurs ────────────────────────────────────────── */}
      <section className="border-t border-ligne bg-sable">
        <Conteneur className="flex flex-col gap-12 py-20">
          <div data-apparition className="flex max-w-[720px] flex-col gap-4">
            <Surtitre>Notre mission</Surtitre>
            <p className="m-0 text-[clamp(1.05rem,1.6vw,1.25rem)] font-medium leading-relaxed">{MISSION}</p>
          </div>
          <div data-apparition className="pl-0 md:pl-5">
            <Valeurs valeurs={VALEURS} />
          </div>
        </Conteneur>
      </section>

      {/* ── Prière + venir ────────────────────────────────────────────── */}
      <section className="relative overflow-hidden bg-nuit text-sur-nuit">
        <div className="braises opacity-80" aria-hidden="true" />
        <Conteneur className="relative grid gap-12 py-20 md:grid-cols-2 md:gap-16">
          <div data-apparition className="flex flex-col gap-4">
            <Surtitre surNuit>Prière</Surtitre>
            <TitreSection>Un fardeau à déposer ?</TitreSection>
            <p className="m-0 max-w-[30em] text-base leading-relaxed text-creme">Écrivez librement. Votre demande reste confidentielle et n’est jamais publiée.</p>
            <div className="mt-2 flex flex-wrap gap-3">
              <Bouton href="/priere" grand>Envoyer une demande de prière</Bouton>
              <Bouton href="/temoignages" variante="contour-nuit" grand>Partager un témoignage</Bouton>
            </div>
          </div>
          <div data-apparition style={d(120)} className="flex flex-col gap-5 rounded-3xl border border-white/10 bg-white/[0.04] p-7 backdrop-blur-md">
            <p className="m-0 font-titre text-lg font-bold">Venir au Centre</p>
            <ul className="m-0 flex list-none flex-col gap-3 p-0">
              {site.horaires.map((h) => (
                <li key={h.jour} className="flex flex-wrap items-baseline justify-between gap-2 border-b border-white/10 pb-3 text-sm">
                  <span className="text-creme">{h.jour}, {h.libelle.toLowerCase()}{h.precision && <span className="text-gris-clair"> ({h.precision})</span>}</span>
                  <span className="font-titre font-bold tabular-nums">{h.heures}</span>
                </li>
              ))}
            </ul>
            <p className="m-0 text-sm text-creme">{site.adresse}, {site.ville}</p>
            <Link href="/nous-rejoindre" className="lien-trace self-start text-sm font-semibold text-or hover:text-or">Itinéraire et première visite</Link>
          </div>
        </Conteneur>
      </section>
    </>
  );
}

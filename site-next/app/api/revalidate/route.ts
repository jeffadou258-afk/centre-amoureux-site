import { revalidateTag } from "next/cache";
import { timingSafeEqual } from "node:crypto";
import { config } from "@/lib/config";

/** Appelé par le backend de Hermes après chaque publication (serveur à serveur). */
export async function POST(req: Request) {
  const fourni = req.headers.get("authorization")?.replace(/^Bearer\s+/i, "") ?? "";
  const attendu = config.revalidateSecret;
  const ok = attendu.length >= 32 && fourni.length === attendu.length && timingSafeEqual(Buffer.from(fourni), Buffer.from(attendu));
  if (!ok) return Response.json({ ok: false }, { status: 401 });
  const corps = (await req.json().catch(() => null)) as { etiquettes?: unknown } | null;
  const etiquettes = Array.isArray(corps?.etiquettes) ? corps.etiquettes.filter((e): e is string => typeof e === "string" && /^[a-z:0-9-]{1,80}$/.test(e)) : [];
  etiquettes.forEach((e) => revalidateTag(e));
  return Response.json({ ok: true, rafraichies: etiquettes });
}

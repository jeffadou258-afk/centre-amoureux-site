import "server-only";

/** Configuration serveur. Aucune de ces valeurs n'est envoyée au navigateur. */
export const config = {
  apiUrl: (process.env.CAD_API_URL ?? "").replace(/\/+$/, ""),
  revalidateSecret: process.env.CAD_REVALIDATE_SECRET ?? "",
  adminApercu: process.env.CAD_ADMIN_APERCU === "1" && process.env.NODE_ENV !== "production",
};

export const apiBranchee = () => config.apiUrl.length > 0;

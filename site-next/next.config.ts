import type { NextConfig } from "next";

const dev = process.env.NODE_ENV === "development";

// Next.js injecte des scripts en ligne : 'unsafe-inline' reste nécessaire
// tant que la CSP à nonce n'est pas en place (prévu, cf. document d'architecture).
const csp = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline'${dev ? " 'unsafe-eval'" : ""} https://challenges.cloudflare.com`,
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data: blob:",
  "font-src 'self'",
  "connect-src 'self'",
  "frame-src https://www.youtube-nocookie.com https://challenges.cloudflare.com",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  dev ? "" : "upgrade-insecure-requests",
].filter(Boolean).join("; ");

// Anciennes adresses du site statique : on ne casse aucun lien déjà partagé.
const anciennes: [string, string][] = [
  ["/index.html", "/"],
  ["/le-centre.html", "/le-centre"],
  ["/le-prophete.html", "/le-prophete"],
  ["/programmes.html", "/programmes"],
  ["/enseignements.html", "/predications"],
  ["/mediatheque.html", "/predications"],
  ["/priere.html", "/priere"],
  ["/temoignages.html", "/temoignages"],
  ["/nous-rejoindre.html", "/nous-rejoindre"],
  ["/dons.html", "/dons"],
  ["/mentions-legales.html", "/mentions-legales"],
  ["/confidentialite.html", "/confidentialite"],
];

const config: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "Content-Security-Policy", value: csp },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), payment=()" },
        ],
      },
    ];
  },
  async redirects() {
    return [
      ...anciennes.map(([source, destination]) => ({ source, destination, permanent: true })),
      // Ancienne adresse avec une faute de frappe, déjà partagée.
      { source: "/predications/service-prohetique.html", destination: "/predications/service-prophetique", permanent: true },
      { source: "/predications/:slug.html", destination: "/predications/:slug", permanent: true },
    ];
  },
};

export default config;

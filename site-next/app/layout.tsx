import type { Metadata, Viewport } from "next";
import "@fontsource-variable/archivo/index.css";
import "@fontsource-variable/manrope/index.css";
import "@fontsource/instrument-serif/400.css";
import "@fontsource/instrument-serif/400-italic.css";
import "./globals.css";

const site = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(site),
  title: { default: "Centre des Amoureux de Dieu — Abidjan", template: "%s · Centre des Amoureux de Dieu" },
  description:
    "Église à Cocody Riviera 2, Abidjan, conduite par le Prophète Daniel Jeff Adou. Cultes le dimanche de 14h00 à 18h30, prédications, prière et programmes.",
  icons: { icon: "/favicon.svg", apple: "/img/icone-512.png" },
  openGraph: { type: "website", locale: "fr_CI", siteName: "Centre des Amoureux de Dieu" },
};

export const viewport: Viewport = { themeColor: "#120C08", width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}

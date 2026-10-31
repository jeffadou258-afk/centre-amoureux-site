#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Serveur de prévisualisation local du site du Centre des Amoureux de Dieu.

Il sert les fichiers statiques ET applique les en-têtes de sécurité de
`vercel.json` (CSP comprise). Sans cela, une prévisualisation locale ne dit
rien de ce que la production servira : une CSP trop stricte casse les styles
en ligne ou les polices, et on ne le verrait qu'après le déploiement.

    python3 outils/serveur.py [port]
"""

import http.server
import os
import socketserver
from http.server import ThreadingHTTPServer
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4321

CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "frame-src https://www.youtube-nocookie.com; "
    "connect-src 'self'; "
    "form-action 'self'; "
    "base-uri 'none'; "
    "object-src 'none'"
)

ENTETES = {
    "Content-Security-Policy": CSP,
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
    "Cache-Control": "no-store",
}


class Gestionnaire(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=RACINE, **kwargs)

    def end_headers(self):
        for cle, valeur in ENTETES.items():
            self.send_header(cle, valeur)
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        # 404 personnalisé, comme sur un hébergement statique correctement réglé.
        if code == 404:
            page = os.path.join(RACINE, "404.html")
            if os.path.exists(page):
                corps = open(page, "rb").read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(corps)))
                self.end_headers()
                self.wfile.write(corps)
                return
        super().send_error(code, message, explain)

    def log_message(self, format, *args):
        sys.stdout.write("%s\n" % (format % args))


if __name__ == "__main__":
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    socketserver.ThreadingTCPServer.daemon_threads = True
    with ThreadingHTTPServer(("127.0.0.1", PORT), Gestionnaire) as httpd:
        print("Site du Centre — http://127.0.0.1:%d/" % PORT)
        print("En-têtes de sécurité de vercel.json appliqués.")
        httpd.serve_forever()

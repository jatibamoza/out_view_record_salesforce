import os
from flask import Flask, render_template, request

app = Flask(__name__)

SITE_DOMAIN = os.getenv("SITE_DOMAIN", "https://s11g0--core.sandbox.my.site.com/recordviewerapp").rstrip("/")
CORE_DOMAIN = os.getenv("CORE_DOMAIN", "https://s11g0--core.sandbox.lightning.force.com").rstrip("/")
CONTENT_DOMAIN = os.getenv("CONTENT_DOMAIN", "https://s11g0--core.sandbox.content.force.com").rstrip("/")

@app.after_request
def add_csp_headers(resp):
    # Permitir scripts/iframing/requests hacia tu Experience y dominios Lightning/Content
    policy = "; ".join([
        f"default-src 'self' {SITE_DOMAIN}",
        f"script-src 'self' 'unsafe-inline' 'unsafe-eval' {SITE_DOMAIN} {CORE_DOMAIN} {CONTENT_DOMAIN}",
        f"style-src  'self' 'unsafe-inline' {SITE_DOMAIN}",
        f"img-src    'self' data: {SITE_DOMAIN} {CONTENT_DOMAIN}",
        f"frame-src  {SITE_DOMAIN} {CORE_DOMAIN}",
        f"connect-src 'self' {SITE_DOMAIN} {CORE_DOMAIN} {CONTENT_DOMAIN}",
    ])
    resp.headers["Content-Security-Policy"] = policy
    # X-Frame-Options ya está obsoleto, pero no estorba:
    resp.headers["X-Frame-Options"] = "ALLOW-FROM " + SITE_DOMAIN
    return resp

@app.route("/")
def index():
    record_id = request.args.get("id", "")
    return render_template(
        "index.html",
        site_domain=SITE_DOMAIN,   # usado para cargar lightning.out.js
        base_domain=CORE_DOMAIN,   # usado por tu botonera
        record_id=record_id
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

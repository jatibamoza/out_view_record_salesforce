import os
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)

# ====== Config por ENV (Render → Settings → Environment) ======
# SITE_ENDPOINT = tu Experience Aura site (con path del site)
SITE_ENDPOINT = os.getenv(
	"SITE_DOMAIN",
	"https://s11g0--core.sandbox.my.site.com/recordviewerapp"
).rstrip("/")

# CORE_DOMAIN = tu dominio core (para forzar login en los botones)
CORE_DOMAIN = os.getenv(
	"CORE_DOMAIN",
	"https://s11g0--core.sandbox.lightning.force.com"
).rstrip("/")

CONTENT_DOMAIN = os.getenv(
	"CONTENT_DOMAIN",
	"https://s11g0--core.sandbox.content.force.com"
).rstrip("/")


def origin(u: str) -> str:
	"""Devuelve solo el ORIGEN (esquema + host [+ puerto]) para CSP."""
	p = urlparse(u)
	return f"{p.scheme}://{p.netloc}"


SITE_ORIGIN = origin(SITE_ENDPOINT)  # <- ¡sin /recordviewerapp!

@app.after_request
def add_csp_headers(resp):
	# ⚠️ CSP NO acepta paths, solo orígenes:
	script_src = f"'self' 'unsafe-inline' 'unsafe-eval' {SITE_ORIGIN} {CORE_DOMAIN} {CONTENT_DOMAIN}"
	policy = "; ".join([
		f"default-src 'self' {SITE_ORIGIN}",
		f"script-src {script_src}",
		f"script-src-elem {script_src}",    # necesario en Chrome
		f"style-src  'self' 'unsafe-inline' {SITE_ORIGIN}",
		f"img-src    'self' data: {SITE_ORIGIN} {CONTENT_DOMAIN}",
		f"frame-src  {SITE_ORIGIN} {CORE_DOMAIN}",
		f"connect-src 'self' {SITE_ORIGIN} {CORE_DOMAIN} {CONTENT_DOMAIN}",
	])
	resp.headers["Content-Security-Policy"] = policy
	return resp


@app.route("/")
def index():
	# ====== lee parámetros ======
	record_id = request.args.get("id", "")             # ← ID del registro
	object_api = request.args.get("object", "Account") # Lead | Account | desconocido

	# Renderiza con los valores (ENDPOINT se usa para cargar lightning.out.js)
	return render_template(
		"index.html",
		site_domain=SITE_ENDPOINT,
		base_domain=CORE_DOMAIN,
		record_id=record_id,
		object_api=object_api
	)


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port)

import os
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)

SITE_ENDPOINT = os.getenv("SITE_DOMAIN", "https://s11g0--core.sandbox.my.site.com/recordviewerapp").rstrip("/")
CORE_DOMAIN   = os.getenv("CORE_DOMAIN",   "https://s11g0--core.sandbox.lightning.force.com").rstrip("/")
CONTENT_DOMAIN= os.getenv("CONTENT_DOMAIN","https://s11g0--core.sandbox.content.force.com").rstrip("/")

def origin(u: str) -> str:
	p = urlparse(u)
	return f"{p.scheme}://{p.netloc}"

SITE_ORIGIN    = origin(SITE_ENDPOINT)        # ej: https://s11g0--core.sandbox.my.site.com
CORE_ORIGIN    = origin(CORE_DOMAIN)          # ej: https://s11g0--core.sandbox.lightning.force.com
CONTENT_ORIGIN = origin(CONTENT_DOMAIN)       # ej: https://s11g0--core.sandbox.content.force.com

# 🔸 hosts estáticos de Salesforce (donde sirve auraFW y assets)
STATIC_LIGHTNING = "https://*.static.lightning.force.com"

@app.after_request
def add_csp_headers(resp):
	# Reglas CSP: usa SOLO orígenes (no paths) y agrega *.static.lightning.force.com
	script = f"'self' 'unsafe-inline' 'unsafe-eval' {SITE_ORIGIN} {CORE_ORIGIN} {CONTENT_ORIGIN} {STATIC_LIGHTNING}"
	policy = "; ".join([
		f"default-src 'self' {SITE_ORIGIN}",
		f"script-src {script}",
		f"script-src-elem {script}",       # ← Chrome usa esta para <script src=...>
		f"style-src  'self' 'unsafe-inline' {SITE_ORIGIN}",
		f"img-src    'self' data: {SITE_ORIGIN} {CONTENT_ORIGIN}",
		f"frame-src  {SITE_ORIGIN} {CORE_ORIGIN}",
		f"connect-src 'self' {SITE_ORIGIN} {CORE_ORIGIN} {CONTENT_ORIGIN} {STATIC_LIGHTNING}",
		f"font-src  'self' data: {SITE_ORIGIN} {CONTENT_ORIGIN}",
		f"navigate-to 'self' {SITE_ORIGIN} {CORE_ORIGIN}",
		f"form-action 'self' {CORE_ORIGIN}",
		# f"worker-src 'self' {SITE_ORIGIN} {CORE_ORIGIN}",   # opcional si lo ves en logs
	])
	resp.headers["Content-Security-Policy"] = policy
	return resp

@app.route("/")
def index():
	auth = request.args.get("auth", "")
	LlamadaId = request.args.get("LlamadaId", "")
	Option = request.args.get("Option", "")
	productPpal = request.args.get("productPpal", "")
	Value  = request.args.get("Value", "")

	return render_template(
		"index.html",
		site_domain=SITE_ENDPOINT,   # con /recordviewerapp
		base_domain=CORE_DOMAIN,
		Value=Value,
		LlamadaId=LlamadaId
	)

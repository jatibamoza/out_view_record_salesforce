import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Dominios de tu org (ajústalos por ENV en Render)
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "https://s11g0--core.sandbox.my.site.com")
CORE_DOMAIN = os.getenv("CORE_DOMAIN", "https://s11g0--core.sandbox.lightning.force.com")

@app.route("/")
def index():
    record_id = request.args.get("id", "")                   # ej: 001D000001HD0MWIA1
    object_api = request.args.get("object", "Account")       # 'Lead' | 'Account' | 'desconocido'
    base_domain = CORE_DOMAIN                                # para la botonera que fuerza login en core
    site_domain = SITE_DOMAIN                                # endpoint del Experience para Lightning Out
    return render_template(
        "index.html",
        record_id=record_id,
        object_api=object_api,
        base_domain=base_domain,
        site_domain=site_domain
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

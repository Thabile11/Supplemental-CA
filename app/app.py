import logging
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

APP_NAME = os.getenv("APP_NAME", "Secure Public Application")

@app.get("/")
def home():
    logging.info("Public application request path=%s remote=%s", request.path, request.remote_addr)
    return f"""
    <!doctype html>
    <html>
      <head><title>{APP_NAME}</title></head>
      <body>
        <h1>{APP_NAME}</h1>
        <p>Public application is running behind the Nginx reverse proxy.</p>
        <p>Try <a href="/health">/health</a> or the protected <a href="/admin/">/admin/</a> area.</p>
      </body>
    </html>
    """

@app.get("/health")
def health():
    logging.info("Health check passed remote=%s", request.remote_addr)
    return jsonify(status="ok", service="public_web")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import hmac
import logging
import os
from base64 import b64decode, binascii
from flask import Flask, Response, request

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

USERNAME = os.environ.get("ADMIN_USERNAME", "")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

def credentials_valid():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Basic "):
        return False
    try:
        decoded = b64decode(auth[6:]).decode("utf-8")
        username, password = decoded.split(":", 1)
    except (ValueError, UnicodeDecodeError, binascii.Error):
        return False
    return hmac.compare_digest(username, USERNAME) and hmac.compare_digest(password, PASSWORD)

def challenge():
    return Response(
        "Authentication required\n",
        401,
        {"WWW-Authenticate": 'Basic realm="Protected Admin"'}
    )

@app.before_request
def require_auth():
    if not credentials_valid():
        logging.warning("Denied admin request path=%s remote=%s", request.path, request.remote_addr)
        return challenge()

@app.get("/")
def admin_home():
    logging.info("Allowed admin request path=%s remote=%s", request.path, request.remote_addr)
    return """
    <!doctype html>
    <html>
      <head><title>Protected Admin</title></head>
      <body>
        <h1>Protected Admin Service</h1>
        <p>Authentication succeeded.</p>
        <p>This service has no published host port and is reachable through the reverse proxy.</p>
      </body>
    </html>
    """

@app.get("/health")
def health():
    logging.info("Authenticated admin health check")
    return {"status": "ok", "service": "protected_admin"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

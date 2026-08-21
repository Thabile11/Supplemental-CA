# Secure Public-Facing Application Platform — Short Report

## 1. System Overview

This prototype implements a small public-facing application platform on an Ubuntu Server LTS virtual machine using Docker Compose. The stack contains three containers: an Nginx reverse proxy, a public Flask web application, and a protected Flask admin service.

The only published container port is Nginx port 80, mapped to host port 8080. Users therefore enter through a single controlled ingress point. Nginx routes normal requests to the public web application and `/admin/` requests to the protected admin service.

The public web application is attached to `app_net`. The protected admin service is attached to `internal_net`. Both networks are marked `internal: true`, meaning they are not intended to provide direct external connectivity. The proxy joins the networks it needs for routing. The admin service has no `ports` mapping, so it is not directly exposed on the VM.

The admin service uses HTTP Basic Authentication. An unauthenticated request receives HTTP 401, while a request with the configured credentials receives HTTP 200. This demonstrates that reaching the network or URL is not sufficient to obtain access.

## 2. Architecture Diagram

See `architecture.svg`.

The main flow is:

`Client -> Nginx reverse proxy -> public_web`

or:

`Client -> Nginx reverse proxy -> protected_admin -> authentication check`

Nginx is the only ingress component. The Docker networks reduce unnecessary connectivity between containers and prevent the admin service from being published directly.

## 3. Configuration and Secrets Management

Docker Compose defines the services, networks, volumes, dependencies, and published port. The application images are built locally from the `app/` and `admin/` directories.

Configuration is supplied through environment variables. `.env.example` documents the required values using placeholders. The real `.env` file is excluded using `.gitignore` and must not be submitted. In particular, the administrator password must never be placed directly in `docker-compose.yml`, source code, screenshots, or Git history.

This is appropriate for a small educational prototype but is not enterprise-grade secret management. A real deployment should use a dedicated secrets manager, TLS certificates, stronger authentication, key rotation, and appropriate access policies.

## 4. Testing Evidence

### Test 1 — Public application

**Purpose:** Verify that the intended public service is reachable.

**Method:** `curl -i http://<VM-IP>:8080/`

**Expected:** HTTP 200 with the public application page.

**Actual:** HTTP 200 and the application page was returned.

**Interpretation:** The host reaches Nginx and Nginx successfully routes the request to `public_web`.

### Test 2 — Reverse proxy health route

**Purpose:** Confirm controlled routing rather than direct container exposure.

**Method:** `curl -i http://<VM-IP>:8080/health`

**Expected:** HTTP 200 and JSON health information.

**Actual:** HTTP 200 from the public web service.

**Interpretation:** The request reached the application through the proxy route.

### Test 3 — Unauthenticated protected access

**Purpose:** Verify that authentication prevents automatic access.

**Method:** `curl -i http://<VM-IP>:8080/admin/`

**Expected:** HTTP 401 Unauthorized.

**Actual:** HTTP 401 was returned with an authentication challenge.

**Interpretation:** A user who can reach the public endpoint is not automatically trusted. This supports a basic Zero Trust principle of verifying access before allowing the protected operation.

### Test 4 — Authenticated protected access

**Purpose:** Verify that valid credentials permit authorised access.

**Method:** `curl -i -u "$ADMIN_USERNAME:$ADMIN_PASSWORD" http://<VM-IP>:8080/admin/`

**Expected:** HTTP 200.

**Actual:** HTTP 200 and the protected admin page was returned.

**Interpretation:** The access-control mechanism is functioning and distinguishes unauthorised from authorised requests.

### Test 5 — Exposure and network configuration

**Purpose:** Confirm that unnecessary container ports are not published.

**Method:** `docker compose ps`, `ss -lnt`, and `docker network inspect`.

**Expected:** Only Nginx has a host port mapping; web and admin remain internal.

**Actual:** Only the proxy publishes port 8080. The web and admin containers expose their application ports only to their Docker networks.

**Interpretation:** The attack surface is reduced because the internal service cannot be reached directly through a host-published port.

### Logging evidence

After running the unauthenticated and authenticated admin tests, `docker compose logs admin` shows denied and allowed requests. Nginx access logs also show requests arriving through the reverse proxy. These logs provide operational evidence that the routing and authentication tests actually occurred.

## 5. Short Security Reflection

The main controls are single-point ingress through Nginx, Docker network separation, no published port for the protected service, environment-based configuration, and authentication on the admin endpoint.

The design follows a basic Zero Trust idea: network reachability does not automatically imply trust. The protected endpoint checks credentials before granting access. Network separation also limits unnecessary communication and reduces exposure.

Remaining risks include HTTP rather than HTTPS, simple Basic Authentication, environment-variable secrets, lack of rate limiting, limited monitoring, and the absence of a production secret-management system. The Flask development server is also suitable only for this educational prototype.

A real deployment should use TLS, a production WSGI server, stronger identity and access management, secure secret storage, regular patching, firewall controls, rate limiting, centralised logging, alerting, backups, and vulnerability scanning. Therefore, this prototype demonstrates security principles but should not be described as fully secure or production ready.

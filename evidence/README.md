# Evidence capture guide

Capture screenshots on the Ubuntu VM and save them under this directory before submission.

Recommended evidence:

1. `01-vm-system.png`
   - `lsb_release -a`
   - `uname -a`
   - VirtualBox VM visible if useful.

2. `02-compose-ps.png`
   - `docker compose ps`
   - Shows all three services running and only the proxy publishing a host port.

3. `03-compose-config.png`
   - `docker compose config`
   - Demonstrates resolved Compose configuration without showing `.env` values.

4. `04-public-app.png`
   - Browser or `curl` showing `http://<VM-IP>:8080/`.

5. `05-proxy-routing.png`
   - `/health` and `/admin/` requests through port 8080.

6. `06-network-separation.png`
   - `docker network inspect ...`
   - Show proxy membership and the separation of web/admin services.

7. `07-auth-denied.png`
   - `curl -i http://<VM-IP>:8080/admin/`
   - Expected `401 Unauthorized`.

8. `08-auth-allowed.png`
   - Authenticated request returning `200 OK`.
   - Do not show the password in the screenshot.

9. `09-logs.png`
   - `docker compose logs admin`
   - Show denied and successful authentication events.

10. `10-tests.png`
   - Output of `bash evidence/test-stack.sh`.

Do not capture or submit `.env`, passwords, private keys, tokens, or other sensitive values.

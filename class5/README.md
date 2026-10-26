# NotesApp HTTPS Lab

**Name:** Haitian Gao

**Student ID:** 2023903116

**Partner:** 叶与陈 Yuchen Ye

**Partner student ID:** 2023901708

**Date:** 22 October 2026

## 1. HTTP login

The password was readable in Wireshark:

```text
username=alice&password=alicepw
```

- **Who can read it:** In this local test, someone with permission to capture loopback traffic.
- **Severity:** High if the same HTTP login is used on an untrusted network, because the password can be stolen.
- **Fix:** Add Nginx with HTTPS and stop exposing Flask directly.

![HTTP: readable username and password](evidence/http-screenshot.png)

## 2. HTTPS test

The login still worked at `https://localhost:8443`. Wireshark showed TLS 1.3 application data, and the username and password were no longer readable. HTTP on port 8080 now redirects to HTTPS.

The two captures used the same login sent with curl, without cookies. Chrome login was also checked.

![HTTPS: encrypted traffic](evidence/https-screenshot.png)

## 3. Certificate check

- **GitHub issuer:** Sectigo Public Server Authentication CA DV E36.
- **Local issuer:** localhost, signed by itself.

Chrome warned about the local certificate because its issuer was not trusted. HTTPS encrypts the connection, but a self-signed certificate does not prove the server's identity through a trusted CA.

**Result:** NotesApp works over HTTPS. The captured password is hidden, but the certificate is still self-signed.

## 4. Reproduce the HTTPS configuration

Generate the local certificate and start the base stack plus the HTTPS overlay:

```powershell
.\generate-https-certificate.ps1
docker compose -f docker-compose.yml -f docker-compose.https.yml up -d --build
```

Nginx listens on `127.0.0.1:8080` for HTTP and redirects requests to `https://localhost:8443`. TLS terminates at Nginx, which proxies to `web:5000` over the private Compose network. The overlay removes Flask's published host port, so Flask is not directly reachable from the host.

Verification commands:

```powershell
docker compose -f docker-compose.yml -f docker-compose.https.yml exec -T nginx nginx -t
curl.exe -I http://localhost:8080/healthz
curl.exe -k https://localhost:8443/healthz
docker compose -f docker-compose.yml -f docker-compose.https.yml ps
```

Expected results are a `301` redirect containing `Location: https://localhost:8443/healthz`, an HTTPS response body of `ok`, three running containers, and no published port on the `web` service. The generated certificate and private key remain Git-ignored.

[Lab instructions](https://kristenpire.github.io/epita-security-labs/class5/https-lab/)

The separate [password storage audit](password-audit/README.md) records the C5b MD5 and Argon2 measurements.

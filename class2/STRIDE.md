# Initial STRIDE analysis

| Category | Concrete NotesApp risk | Affected flows | Initial control |
|---|---|---|---|
| Spoofing | Weak passwords and forgeable `alg=none` JWTs allow identity impersonation | 1-4, 9-12 | Argon2, strong secrets, reject unsigned JWTs |
| Tampering | SQL injection, CSRF and unsigned CSV files allow unauthorized changes | 1-3, 17-24 | Parameterized SQL, CSRF tokens, HMAC exports |
| Repudiation | Grade and account changes lack complete before/after audit records | 17-20, 25-28 | Append-only structured audit log |
| Information disclosure | Plain HTTP, plaintext passwords/comments and IDOR expose sensitive data | 1-12, 21-24 | HTTPS, Argon2, AES-GCM and ownership checks |
| Denial of service | Unbounded requests and synchronous ping can exhaust workers | 25-28 | Rate limiting, timeouts and background jobs |
| Elevation of privilege | Command injection plus a root container and Docker socket can compromise the host | 25-28 | Remove shell execution/socket mount and run non-root |

## Highest initial risks

1. Admin ping command injection, because attacker-controlled text reaches a shell.
2. Root web container with the Docker socket mounted, because an application compromise can become host control.
3. Forgeable JWT authentication and note IDOR, because an authenticated or forged identity can read another student's record.

This is a source-based threat model. It does not claim that exploitation was performed.

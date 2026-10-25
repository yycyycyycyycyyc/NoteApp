# C3 - Encrypted grade comments

NotesApp now protects stored grade comments with AES-256-GCM authenticated encryption. A fresh 96-bit nonce is generated for every write, so equal comments produce different ciphertext. Stored values use the versioned `enc:v1:` prefix. The encryption key is generated locally in `.env` and is not committed.

The migration is idempotent: `docker compose exec -T web python migrate_comments.py` encrypts only legacy plaintext rows. On this checkout it migrated all 60 comments, and a database query confirmed `60/60` values use the encrypted prefix. Application reads decrypt only inside the web process; database exports no longer reveal comment text.

Verification: four security unit tests pass, including encryption round-trip, random nonces, tamper rejection, valid HMAC acceptance, and modified-file rejection.

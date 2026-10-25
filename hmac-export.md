# C4 - HMAC-protected grade export

CSV exports now end with `# HMAC: <hex digest>`, computed with HMAC-SHA256 over the exact preceding CSV bytes. The key is kept in the ignored `.env` file. Verification uses `hmac.compare_digest` to avoid timing-sensitive string comparison.

Teachers can upload an exported CSV through the new verification form. The independently generated evidence files demonstrate both outcomes:

- `class4/evidence/grades-export-valid.csv` was accepted.
- `class4/evidence/grades-export-tampered.csv` contains one changed grade and was rejected.

The test suite also checks unsigned-file rejection and tamper detection.

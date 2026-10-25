import secrets
from pathlib import Path

path = Path(".env")
existing = path.read_text(encoding="utf-8") if path.exists() else ""
if "EXPORT_HMAC_KEY=" not in existing:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"EXPORT_HMAC_KEY={secrets.token_hex(32)}\n")
    print("created EXPORT_HMAC_KEY in .env")
else:
    print("EXPORT_HMAC_KEY already exists")

import secrets
from pathlib import Path

path = Path(".env")
existing = path.read_text(encoding="utf-8") if path.exists() else ""

if "JWT_SECRET=" not in existing:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"JWT_SECRET={secrets.token_hex(32)}\n")
    print("created JWT_SECRET in .env")
else:
    print("JWT_SECRET already exists")

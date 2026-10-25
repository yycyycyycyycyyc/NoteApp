import base64
import os
from pathlib import Path

path = Path(".env")
existing = path.read_text(encoding="utf-8") if path.exists() else ""
if "COMMENT_ENCRYPTION_KEY=" not in existing:
    key = base64.urlsafe_b64encode(os.urandom(32)).decode("ascii")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"COMMENT_ENCRYPTION_KEY={key}\n")
    print("created COMMENT_ENCRYPTION_KEY in .env")
else:
    print("COMMENT_ENCRYPTION_KEY already exists")

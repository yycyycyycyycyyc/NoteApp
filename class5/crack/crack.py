import hashlib
import hmac
import time
from pathlib import Path

folder = Path(__file__).parent
accounts = {}
for line in (folder / "leaked_users.txt").read_text(encoding="utf-8").splitlines():
    username, digest = line.split(":")
    accounts[username] = digest

wordlist = [w.strip() for w in (folder / "wordlist.txt").read_text(encoding="utf-8").splitlines() if w.strip()]
start = time.perf_counter()
cracked = {}
for candidate in wordlist:
    digest = hashlib.md5(candidate.encode()).hexdigest()
    for username, stored in accounts.items():
        if username not in cracked and hmac.compare_digest(digest, stored):
            cracked[username] = candidate
elapsed_ms = (time.perf_counter() - start) * 1000

print(f"cracked {len(cracked)} / {len(accounts)} in {elapsed_ms:.3f} ms")
for username, password in cracked.items():
    print(f"  {username}: {password}")

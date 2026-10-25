"""HMAC signing and verification for exported CSV files."""
import hashlib
import hmac
import os

MARKER = b"# HMAC: "


def _key() -> bytes:
    value = os.environ.get("EXPORT_HMAC_KEY", "")
    if len(value) < 32:
        raise RuntimeError("EXPORT_HMAC_KEY must contain at least 32 characters")
    return value.encode("utf-8")


def sign_csv(data: bytes) -> bytes:
    digest = hmac.new(_key(), data, hashlib.sha256).hexdigest().encode("ascii")
    return data + MARKER + digest + b"\n"


def verify_csv(signed: bytes) -> bool:
    try:
        body, tag_line = signed.rsplit(MARKER, 1)
        supplied = tag_line.strip().decode("ascii")
    except (ValueError, UnicodeDecodeError):
        return False
    expected = hmac.new(_key(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, supplied)

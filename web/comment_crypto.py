"""Authenticated encryption for grade comments."""
import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PREFIX = "enc:v1:"


def _key() -> bytes:
    raw = os.environ.get("COMMENT_ENCRYPTION_KEY", "")
    try:
        key = base64.urlsafe_b64decode(raw.encode())
    except Exception as exc:
        raise RuntimeError("COMMENT_ENCRYPTION_KEY must be URL-safe base64") from exc
    if len(key) != 32:
        raise RuntimeError("COMMENT_ENCRYPTION_KEY must decode to 32 bytes")
    return key


def encrypt_comment(plaintext: str) -> str:
    if plaintext.startswith(PREFIX):
        return plaintext
    nonce = os.urandom(12)
    ciphertext = AESGCM(_key()).encrypt(nonce, plaintext.encode("utf-8"), None)
    payload = base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")
    return PREFIX + payload


def decrypt_comment(value: str) -> str:
    if not value.startswith(PREFIX):
        return value
    payload = base64.urlsafe_b64decode(value[len(PREFIX):].encode("ascii"))
    return AESGCM(_key()).decrypt(payload[:12], payload[12:], None).decode("utf-8")

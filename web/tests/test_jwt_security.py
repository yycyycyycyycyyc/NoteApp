import base64
import hashlib
import hmac
import json
import os
import unittest

os.environ.setdefault("JWT_SECRET", "new-random-test-secret-0123456789abcdef0123456789abcdef")
os.environ.setdefault("COMMENT_ENCRYPTION_KEY", base64.urlsafe_b64encode(b"C" * 32).decode())
os.environ.setdefault("EXPORT_HMAC_KEY", "H" * 64)

from app import make_jwt, verify_jwt


def b64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def token(header: dict, payload: dict, secret: str | None = None) -> str:
    encoded_header = b64url(json.dumps(header).encode())
    encoded_payload = b64url(json.dumps(payload).encode())
    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    signature = ""
    if secret is not None:
        signature = b64url(hmac.new(secret.encode(), signing_input, hashlib.sha256).digest())
    return f"{encoded_header}.{encoded_payload}.{signature}"


class JwtSecurityTests(unittest.TestCase):
    payload = {"user_id": 1, "username": "alice", "role": "student"}

    def test_rejects_none_forgery(self):
        forged = token({"alg": "none", "typ": "JWT"}, self.payload)
        self.assertIsNone(verify_jwt(forged))

    def test_rejects_old_s3cr3t_forgery(self):
        forged = token({"alg": "HS256", "typ": "JWT"}, self.payload, "s3cr3t")
        self.assertIsNone(verify_jwt(forged))

    def test_accepts_real_server_token(self):
        real = make_jwt(self.payload)
        self.assertEqual(verify_jwt(real), self.payload)

    def test_algorithm_is_case_sensitive_and_pinned(self):
        forged = token({"alg": "hs256", "typ": "JWT"}, self.payload, os.environ["JWT_SECRET"])
        self.assertIsNone(verify_jwt(forged))


if __name__ == "__main__":
    unittest.main()

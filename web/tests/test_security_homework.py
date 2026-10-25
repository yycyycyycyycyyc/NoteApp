import base64
import os
import unittest

os.environ.setdefault("COMMENT_ENCRYPTION_KEY", base64.urlsafe_b64encode(b"C" * 32).decode())
os.environ.setdefault("EXPORT_HMAC_KEY", "H" * 64)

from comment_crypto import decrypt_comment, encrypt_comment
from export_hmac import sign_csv, verify_csv


class CommentCryptoTests(unittest.TestCase):
    def test_round_trip_and_random_nonce(self):
        first = encrypt_comment("Good progress")
        second = encrypt_comment("Good progress")
        self.assertNotEqual(first, second)
        self.assertEqual(decrypt_comment(first), "Good progress")

    def test_tampering_is_rejected(self):
        value = encrypt_comment("private")
        with self.assertRaises(Exception):
            decrypt_comment(value[:-2] + "AA")


class ExportHmacTests(unittest.TestCase):
    def test_original_passes_and_tampered_fails(self):
        signed = sign_csv(b"student,grade\nalice,16\n")
        self.assertTrue(verify_csv(signed))
        self.assertFalse(verify_csv(signed.replace(b"16", b"10")))

    def test_unsigned_file_fails(self):
        self.assertFalse(verify_csv(b"student,grade\n"))


if __name__ == "__main__":
    unittest.main()

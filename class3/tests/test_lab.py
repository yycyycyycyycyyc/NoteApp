import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from caesar import encrypt, decrypt, crack_by_frequency
from image_modes import run
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Class3Tests(unittest.TestCase):
    def test_caesar_round_trip(self):
        self.assertEqual(decrypt(encrypt("HELLO", 3), 3), "HELLO")

    def test_frequency_demo(self):
        text = "THE SECRET MESSAGE IS HERE. WE NEED TO KEEP THE MESSAGE SAFE."
        key, recovered = crack_by_frequency(encrypt(text, 7))
        self.assertEqual((key, recovered), (7, text))

    def test_ecb_and_gcm_round_trip_and_outputs(self):
        raw, key, nonce, ecb, gcm = run()
        dec = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
        self.assertEqual(dec.update(ecb) + dec.finalize(), raw)
        self.assertEqual(AESGCM(key).decrypt(nonce, gcm, None), raw)
        self.assertTrue((ROOT / "results/images/ecb-pattern.png").exists())
        self.assertTrue((ROOT / "results/images/gcm-pattern.png").exists())


if __name__ == "__main__":
    unittest.main()

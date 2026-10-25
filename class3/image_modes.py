from pathlib import Path
from PIL import Image, ImageDraw
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
RESULTS = ROOT / "results" / "images"


def source_image():
    ASSETS.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (256, 256), "#F8FAFC")
    draw = ImageDraw.Draw(image)
    draw.rectangle((32, 32, 224, 224), fill="#2563EB")
    draw.rectangle((72, 72, 184, 184), fill="#F8FAFC")
    draw.ellipse((96, 96, 160, 160), fill="#DC2626")
    image.save(ASSETS / "source-pattern.png")
    return image


def run():
    RESULTS.mkdir(parents=True, exist_ok=True)
    image = source_image()
    raw = image.tobytes()
    key = bytes(range(32))
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    ecb = enc.update(raw) + enc.finalize()
    nonce = bytes(range(12))
    gcm_with_tag = AESGCM(key).encrypt(nonce, raw, None)
    gcm = gcm_with_tag[:-16]
    Image.frombytes("RGB", image.size, ecb).save(RESULTS / "ecb-pattern.png")
    Image.frombytes("RGB", image.size, gcm).save(RESULTS / "gcm-pattern.png")
    return raw, key, nonce, ecb, gcm_with_tag


if __name__ == "__main__":
    run()
    print("wrote source, ECB and GCM comparison images")

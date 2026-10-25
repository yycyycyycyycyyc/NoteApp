from collections import Counter


def encrypt(text, key):
    out = []
    for char in text:
        if char.isalpha() and char.isascii():
            base = ord("A") if char.isupper() else ord("a")
            out.append(chr((ord(char) - base + key) % 26 + base))
        else:
            out.append(char)
    return "".join(out)


def decrypt(text, key):
    return encrypt(text, -key)


def crack_by_frequency(ciphertext):
    counts = Counter(c.upper() for c in ciphertext if c.isascii() and c.isalpha())
    most_common = counts.most_common(1)[0][0]
    key = (ord(most_common) - ord("E")) % 26
    return key, decrypt(ciphertext, key)


if __name__ == "__main__":
    original = "THE SECRET MESSAGE IS HERE. WE NEED TO KEEP THE MESSAGE SAFE."
    ciphertext = encrypt(original, 7)
    guessed_key, recovered = crack_by_frequency(ciphertext)
    print(f"Original: {original}")
    print(f"Encrypted: {ciphertext}")
    print(f"Guessed key: {guessed_key}")
    print(f"Decrypted: {recovered}")

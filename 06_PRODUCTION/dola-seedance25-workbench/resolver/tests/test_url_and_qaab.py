from __future__ import annotations

import base64
import hashlib

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from app.resolver.qaab import SALT_HEX, decode_qaab
from app.resolver.url_decoder import decode_media_urls


KEY_SEED = base64.b64encode(bytes(range(32))).decode()
TARGET = "https://cdn.example.test/unit.mp4?lr=video_gen_no_watermark"


def make_qaab(url: str) -> str:
    seed = base64.b64decode(KEY_SEED)
    derived = hashlib.sha512(hashlib.sha512(seed).digest() + bytes.fromhex(SALT_HEX)).digest()
    padder = padding.PKCS7(128).padder()
    plaintext = padder.update(url.encode()) + padder.finalize()
    encryptor = Cipher(algorithms.AES(derived[:16]), modes.CBC(derived[16:32])).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return base64.b64encode(bytes.fromhex("a8000100") + b"0" * 32 + ciphertext).decode()


def test_plain_and_base64_variants_decode() -> None:
    encoded = base64.urlsafe_b64encode(TARGET.encode()).decode().rstrip("=")
    assert decode_media_urls(TARGET) == [TARGET]
    assert decode_media_urls(encoded) == [TARGET]


def test_qaab_decode() -> None:
    token = make_qaab(TARGET)
    assert token.startswith("qAAB")
    assert decode_qaab(token, KEY_SEED) == TARGET
    assert decode_media_urls(token, key_seed=KEY_SEED) == [TARGET]

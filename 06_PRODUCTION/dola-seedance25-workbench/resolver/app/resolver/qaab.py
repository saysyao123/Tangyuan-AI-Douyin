from __future__ import annotations

import base64
import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


SALT_HEX = (
    "4dd4c2e6b83162090e52b3c7a6733ba4"
    "1cb2462b829ab58a196b39db57177524"
    "f49baf7f08e8d68d26a72e37c1a95a2f"
    "1f05a51892aef2949732b62a38aadd58"
)
QAAB_HEADER = bytes.fromhex("a8000100")


class QAABDecodeError(ValueError):
    pass


def loose_b64decode(value: str | bytes) -> bytes:
    text = value.decode("ascii") if isinstance(value, bytes) else str(value)
    text = text.strip().replace("-", "+").replace("_", "/")
    text = text.replace("$", "+").replace("@", "/").replace("#", "=")
    text += "=" * ((4 - len(text) % 4) % 4)
    try:
        return base64.b64decode(text, validate=False)
    except (ValueError, TypeError) as exc:
        raise QAABDecodeError("invalid base64 payload") from exc


def _pkcs7_unpad(value: bytes) -> bytes:
    if not value:
        raise QAABDecodeError("empty decrypted payload")
    pad = value[-1]
    if pad < 1 or pad > 16 or value[-pad:] != bytes([pad]) * pad:
        raise QAABDecodeError("invalid PKCS7 padding")
    return value[:-pad]


def _decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return _pkcs7_unpad(decryptor.update(ciphertext) + decryptor.finalize())


def decode_qaab(token: str, key_seed: str) -> str:
    """Decode a qAAB URL and return only a validated HTTP(S) URL."""
    if not token.startswith("qAAB"):
        raise QAABDecodeError("token does not start with qAAB")
    if not key_seed:
        raise QAABDecodeError("key_seed is required for qAAB")

    encrypted = loose_b64decode(token)
    if encrypted.startswith(QAAB_HEADER):
        payloads = [encrypted[4:], encrypted[36:]]
    else:
        payloads = [encrypted]
    payloads = [payload for index, payload in enumerate(payloads) if payload and payload not in payloads[:index]]

    seed = loose_b64decode(key_seed)[:32]
    first_hash = hashlib.sha512(seed).digest()
    salt = bytes.fromhex(SALT_HEX)
    derived = hashlib.sha512(first_hash + salt).digest()
    key_iv_pairs = [(derived[:16], derived[16:32]), (derived[16:32], derived[:16])]

    for payload in payloads:
        for key, iv in key_iv_pairs:
            if len(payload) % 16:
                continue
            try:
                decoded = _decrypt(payload, key, iv).decode("utf-8").strip()
            except (UnicodeDecodeError, ValueError, QAABDecodeError):
                continue
            if decoded.startswith(("http://", "https://")):
                return decoded
    raise QAABDecodeError("qAAB did not decode to an HTTP(S) URL")

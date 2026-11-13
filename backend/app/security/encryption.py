"""AES-256-GCM helpers for private applicant data. Key is server-only."""
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.config import get_settings


def _key() -> bytes:
    raw = get_settings().encryption_key
    try:
        key = base64.b64decode(raw, validate=True)
    except Exception as exc:
        raise RuntimeError("Set ENCRYPTION_KEY to a base64 encoded 32-byte key") from exc
    if len(key) != 32:
        raise RuntimeError("ENCRYPTION_KEY must decode to exactly 32 bytes")
    return key


def encrypt_value(value: str, *, context: str = "applicant") -> str:
    nonce = os.urandom(12)
    ciphertext = AESGCM(_key()).encrypt(nonce, value.encode("utf-8"), context.encode())
    return base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")


def decrypt_value(token: str, *, context: str = "applicant") -> str:
    packed = base64.urlsafe_b64decode(token.encode("ascii"))
    return AESGCM(_key()).decrypt(packed[:12], packed[12:], context.encode()).decode("utf-8")

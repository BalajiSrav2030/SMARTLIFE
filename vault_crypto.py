"""Encryption for the Legacy Vault (Fernet = AES-128-CBC + HMAC-SHA256).

The key comes from SMARTLIFE_VAULT_KEY in .env, or is generated once into `.vault.key`
next to the app. Keep that file private and backed up: without it the vault cannot be read.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from pathlib import Path

from cryptography.fernet import Fernet

_KEY_FILE = Path(__file__).parent / ".vault.key"


def _key() -> bytes:
    env = os.getenv("SMARTLIFE_VAULT_KEY")
    if env:
        return env.encode()
    if not _KEY_FILE.exists():
        _KEY_FILE.write_bytes(Fernet.generate_key())
        try:
            os.chmod(_KEY_FILE, 0o600)
        except OSError:
            pass
    return _KEY_FILE.read_bytes().strip()


def encrypt(data: bytes | str | None) -> bytes | None:
    if data is None or data == "" or data == b"":
        return None
    if isinstance(data, str):
        data = data.encode()
    return Fernet(_key()).encrypt(data)


def decrypt(token: bytes | None) -> bytes | None:
    if not token:
        return None
    return Fernet(_key()).decrypt(token)


# ---- nominee access codes (stored only as salted hashes) ----
def new_code() -> str:
    """Human-friendly one-time code like 7KQ4-M2XD."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    raw = "".join(secrets.choice(alphabet) for _ in range(8))
    return f"{raw[:4]}-{raw[4:]}"


def hash_code(code: str) -> str:
    salt = secrets.token_hex(16)
    d = hashlib.pbkdf2_hmac("sha256", code.strip().upper().encode(), bytes.fromhex(salt), 200_000)
    return f"{salt}${d.hex()}"


def check_code(code: str, stored: str) -> bool:
    salt, digest = stored.split("$")
    d = hashlib.pbkdf2_hmac("sha256", code.strip().upper().encode(), bytes.fromhex(salt), 200_000)
    return hmac.compare_digest(d.hex(), digest)

import os
import struct

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HEADER = struct.Struct(">?16s12s")  #  is slow?, salt, nonce

SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM = 4, 1024 * 1024, 4
FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM = 4, 256 * 1024, 4


def _derive_key(passphrase: str, salt: bytes, is_slow: bool) -> bytes:
    if is_slow:
        return hash_secret_raw(
            passphrase.encode(), salt, slow_time_cost, slow_memory_cost, slow_parallelism, hash_len=32, type=Type.ID
        )
    else:
        return hash_secret_raw(
            passphrase.encode(), salt, fast_time_cost, fast_memory_cost, fast_parallelism, hash_len=32, type=Type.ID
        )


def encrypt(plaintext: bytes, passphrase: str, is_slow: bool) -> bytes:
    salt, nonce = os.urandom(16), os.urandom(12)
    header = HEADER.pack(is_slow, salt, nonce)
    if is_slow:
        key = _derive_key(passphrase, salt, SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM)
    else:
        key = _derive_key(passphrase, salt, FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM)
    # The header is passed as "associated data": not encrypted, but authenticated
    return header + AESGCM(key).encrypt(nonce, plaintext, header)


def decrypt(blob: bytes, passphrase: str) -> bytes:
    if len(blob) < HEADER.size:
        raise ValueError("file too short")
    header, ciphertext = blob[: HEADER.size], blob[HEADER.size :]
    is_slow, salt, nonce = HEADER.unpack(header)
    if is_slow:
        key = _derive_key(passphrase, salt, SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM)
    elif not is_slow:
        key = _derive_key(passphrase, salt, FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM)
    else:
        raise ValueError("Lentidão não definida!")
    return AESGCM(key).decrypt(nonce, ciphertext, header)  # raises InvalidTag on tampering or wrong passphrase


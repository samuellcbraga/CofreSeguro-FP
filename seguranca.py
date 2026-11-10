import os
import struct

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HEADER = struct.Struct(">?16s12s")  # Struct armazena 3 valores: um booleano, uma string de 16 caracteres e outra string de 12 caracteres, sao elas is slow?, salt e nonce

SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM = 4, 1024 * 1024, 4  # Valores para criptografia lenta (mas mais segura), numero de iteracoes, memoria usada, paralelismo, respectivamente
FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM = 4, 256 * 1024, 4  # Valores para criptografia rapida (mas menos segura), numero de iteracoes, memoria usada, paralelismo, respectivamente

# Funcao serve para derivar chave a partir de uma senha, um salt (aleatorio) e um bool que diz se vai ser rapida ou lenta
def _derive_key(passphrase: str, salt: bytes, is_slow: bool = False) -> bytes:  # funcao de derivacao de chave nao deve ser chamada sozinha, representado pelo _
    if is_slow:
        return hash_secret_raw(
            passphrase.encode(), salt, slow_time_cost, slow_memory_cost, slow_parallelism, hash_len=32, type=Type.ID
        )
    else:
        return hash_secret_raw(
            passphrase.encode(), salt, fast_time_cost, fast_memory_cost, fast_parallelism, hash_len=32, type=Type.ID
        )

# Funcao de criptografar dados, recebe o que deve ser criptografado (em bytes, arquivo deve ser acessado com "rb" inves de "r" e string precisa de .encode()), senha e velocidade
def encrypt(plaintext: bytes, passphrase: str, is_slow: bool = False) -> bytes:
    salt, nonce = os.urandom(16), os.urandom(12)
    header = HEADER.pack(is_slow, salt, nonce)
    if is_slow:
        key = _derive_key(passphrase, salt, is_slow)
    else:
        key = _derive_key(passphrase, salt, is_slow)
    return header + AESGCM(key).encrypt(nonce, plaintext, header)

# Funcao de descriptografar, recebe apenas os bytes criptografados (de novo, arquivo deve ser acessado com "rb" ou "wb" e string precisa de .encode()), e senha, dados para descriptografia estao no HEADER
def decrypt(blob: bytes, passphrase: str) -> bytes:
    if len(blob) < HEADER.size:
        raise ValueError("arquivo muito curto")
    header, ciphertext = blob[: HEADER.size], blob[HEADER.size :]
    is_slow, salt, nonce = HEADER.unpack(header)
    if is_slow:
        key = _derive_key(passphrase, salt, is_slow)
    elif not is_slow:
        key = _derive_key(passphrase, salt, is_slow)
    else:
        raise ValueError("Lentidão não definida!")
    return AESGCM(key).decrypt(nonce, ciphertext, header)  # Retorna um erro InvalidTag independente de se foi por senha incorreta ou por arquivo adulterado


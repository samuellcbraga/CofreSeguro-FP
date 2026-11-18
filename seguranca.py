import os
import struct

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HEADER = struct.Struct(">?16s12s")  # Struct armazena 3 valores: um booleano, uma string de 16 caracteres e outra string de 12 caracteres, sao elas is slow?, salt e nonce

SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM = 4, 1024 * 1024, 4  # Valores para criptografia lenta (mas mais segura), numero de iteracoes, memoria usada, paralelismo, respectivamente
FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM = 4, 256 * 1024, 4  # Valores para criptografia rapida (mas menos segura), numero de iteracoes, memoria usada, paralelismo, respectivamente

# Funcao serve para derivar chave a partir de uma senha, um salt (aleatorio) e um bool que diz se vai ser rapida ou lenta
def _derive_key(passphrase: str, salt: bytes, is_slow: bool) -> bytes:  # funcao de derivacao de chave nao deve ser chamada sozinha, representado pelo _
    if is_slow:
        return hash_secret_raw(
            passphrase.encode(), salt, SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM, hash_len=32, type=Type.ID
        )
    else:
        return hash_secret_raw(
            passphrase.encode(), salt, FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM, hash_len=32, type=Type.ID
        )

def encrypt(plaintext: bytes, passphrase: str, is_slow: bool = False) -> bytes:

    """

    Criptografa dado passado de forma segura.

    Para usar os dados passados, a função precisa receber o dado a ser criptografado e a senha a ser usada, além de especificar se a criptografia será lenta (destinada ao arquivo do banco) ou rápida (uso padrão, feita para categorias de senha ou senhas individuais, a depender da necessidade). Usa-se "rb" ou "wb" no comando 'open' para ler um arquivo e retornar o conteúdo em bytes, para uma string deve-se usar a função [string].encode().

    :param plaintext: O dado a ser criptografado em bytes
    :type plaintext: bytes
    :param passphrase: Senha a ser usada para criptografia
    :type passphrase: str
    :param is_slow: Criptografia deve ser lenta? normalmente irá ser rápida
    :type is_slow: bool, optional
    :return: Dados criptografados em bytes com header apropriado para descriptografia
    :rtype: bytes

    :Example:
    >>> encrypt("mensagem secreta".encode(),"senha")
    b'\x01M\x1a\xf9_L\x13um\xf1\r\xa3cU\x08\xddwm`\xe7\xf0\x0cl_\x07\xcf\xa7\xe6\x86J\x03\xd8\x86\x1c\xb3\xba\xc5\xd8\x920aJm\x02\xdbG\xab\x9b7Jv>\x10\x85\x85Du\x01\x8e\\W'

    """

    salt, nonce = os.urandom(16), os.urandom(12)
    header = HEADER.pack(is_slow, salt, nonce)
    if is_slow:
        key = _derive_key(passphrase, salt, is_slow)
    else:
        key = _derive_key(passphrase, salt, is_slow)
    return header + AESGCM(key).encrypt(nonce, plaintext, header)

def decrypt(blob: bytes, passphrase: str) -> bytes:

    """

    Descriptografa dados passados usando a senha.

    A função apenas precisa dos dados criptografados (blob) e da senha. Dados devem estar em bytes, senha deve ser passada em string. Todos os dados de descriptografia se encontram no header dos arquivos criptografados, então ele automaticamente identifica se é criptografia rápida ou lenta.

    :param blob: Dados criptografados em bytes
    :type blob: bytes
    :param passphrase: A senha para descriptografia
    :type passphrase: str
    :return: Dados descriptografados em bytes
    :rtype: bytes
    :raises ValueError: se o arquivo não tiver espaço de header ou se tiver uma lentidão não definida no header

    :Example:
    >>> decrypt(b'\x01M\x1a\xf9_L\x13um\xf1\r\xa3cU\x08\xddwm`\xe7\xf0\x0cl_\x07\xcf\xa7\xe6\x86J\x03\xd8\x86\x1c\xb3\xba\xc5\xd8\x920aJm\x02\xdbG\xab\x9b7Jv>\x10\x85\x85Du\x01\x8e\\W',"senha")
    b'mensagem secreta'

    """

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

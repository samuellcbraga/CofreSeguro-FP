import os
import struct

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HEADER = struct.Struct(">?16s12s2s")  # Struct armazena 4 valores: um booleano, uma string de 16 caracteres e outra string de 12 caracteres, sao elas is slow?, salt, nonce e últimos dígitos da senha

SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM = 4, 1024 * 1024, 4  # Valores para criptografia lenta (mas mais segura), numero de iteracoes, memoria usada, paralelismo, respectivamente
FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM = 4, 256 * 1024, 4  # Valores para criptografia rapida (mas menos segura), numero de iteracoes, memoria usada, paralelismo, respectivamente

# Funcao serve para derivar chave a partir de uma senha, um salt (aleatorio) e um bool que diz se vai ser rapida ou lenta
def _derivar_chave(passphrase: str, salt: bytes, is_slow: bool) -> bytes:  # funcao de derivacao de chave nao deve ser chamada sozinha, representado pelo _
    if is_slow:
        return hash_secret_raw(
            passphrase.encode(), salt, SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM, hash_len=32, type=Type.ID
        )
    else:
        return hash_secret_raw(
            passphrase.encode(), salt, FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM, hash_len=32, type=Type.ID
        )

def criptografar(plaintext: bytes, passphrase: str, is_slow: bool = False) -> bytes:

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

    """

    salt, nonce = os.urandom(16), os.urandom(12)
    header: bytes = HEADER.pack(is_slow, salt, nonce, passphrase[-1:-2:])
    if is_slow:
        key: bytes = _derivar_chave(passphrase, salt, is_slow)
    else:
        key = _derivar_chave(passphrase, salt, is_slow)
    return header + AESGCM(key).encrypt(nonce, plaintext, header)

def descriptografar(blob: bytes, passphrase: str) -> bytes:

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

    """

    if len(blob) < HEADER.size:
        raise ValueError("arquivo muito curto")
    header, ciphertext = blob[: HEADER.size], blob[HEADER.size :]
    is_slow, salt, nonce, _digitos_senha = HEADER.unpack(header)
    if is_slow:
        key: bytes = _derivar_chave(passphrase, salt, is_slow)
    elif not is_slow:
        key = _derivar_chave(passphrase, salt, is_slow)
    else:
        raise ValueError("Lentidão não definida!")
    return AESGCM(key).decrypt(nonce, ciphertext, header)  # Retorna um erro InvalidTag independente de se foi por senha incorreta ou por arquivo adulterado

def mostrar_final(blob: bytes) -> bytes:
    """Mostra os dois dígitos da senha criptografada sem precisar descriptografar
    
    A função apenas printa o final da senha, detectando quando o dado passado é o banco.

    :param blob: Senha a ter final mostrado
    :type blob: bytes
    :return: Final da senha em bytes
    :rtype: bytes
    :raises ValueError: se blob passado for de criptografia lenta (indica que não foi passada uma senha)
    """
    header = blob[: HEADER.size]
    _is_slow, _salt, _nonce, digitos_senha = HEADER.unpack(header)
    if digitos_senha == b';;':
        raise ValueError
    else:
        return digitos_senha
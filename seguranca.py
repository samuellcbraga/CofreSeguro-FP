import os
import struct

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HEADER = struct.Struct(">?16s12s2s")  # Struct armazena 4 valores: um booleano, uma string de 16 caracteres e outra string de 12 caracteres, sao elas is slow?, salt, nonce e um indicador fixo (b';;' lenta, b'--' rapida). Nada do conteudo vai aqui, pois o cabecalho fica em texto claro

SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM = 4, 1024 * 1024, 4  # Valores para criptografia lenta (mas mais segura), numero de iteracoes, memoria usada, paralelismo, respectivamente
FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM = 4, 256 * 1024, 4  # Valores para criptografia rapida (mas menos segura), numero de iteracoes, memoria usada, paralelismo, respectivamente

# Funcao serve para derivar chave a partir de uma senha, um salt (aleatorio) e um bool que diz se vai ser rapida ou lenta
def _derivar_chave(passphrase: str, salt: bytes, is_slow: bool) -> bytes:  # funcao de derivacao de chave nao deve ser chamada sozinha, representado pelo _
    """Deriva o hash a ser usado como chave de criptografia

    Args:
        passphrase (str): Senha a ser usada
        salt (bytes): Salt a ser usado
        is_slow (bool): Diz se a criptografia será lenta

    Returns:
        bytes: Hash
    """
    if is_slow:
        return hash_secret_raw(
            passphrase.encode(), salt, SLOW_TIME_COST, SLOW_MEMORY_COST, SLOW_PARALLELISM, hash_len=32, type=Type.ID
        )
    else:
        return hash_secret_raw(
            passphrase.encode(), salt, FAST_TIME_COST, FAST_MEMORY_COST, FAST_PARALLELISM, hash_len=32, type=Type.ID
        )

def criptografar(plaintext: bytes, passphrase: str, is_slow: bool = False) -> bytes:

    """Função de criptografar

    Recebe dado a ser criptografado, senha e opcionalmente um booleano para definir se é lenta (para arquivos) ou não (comportamento padrão).

     Args:
        plaintext (bytes): Dado a ser criptografado
        passphrase (str): Senha a ser usada
        is_slow (bool, optional): Diz se a criptografia será lenta (padrão False)

    Returns:
        bytes: Blob criptografado com cabeçalho (sem nenhum dado da senha)
    """

    salt, nonce = os.urandom(16), os.urandom(12)
    if is_slow:
        indicador: bytes = b';;'
        slow_header: bytes = HEADER.pack(is_slow, salt, nonce, indicador)
        key: bytes = _derivar_chave(passphrase, salt, is_slow)
        return slow_header + AESGCM(key).encrypt(nonce, plaintext, slow_header)
    else:
        #valor fixo: antes ia um pedaço do texto original aqui, e o cabeçalho NÃO é criptografado
        indicador_rapido: bytes = b'--'
        header: bytes = HEADER.pack(is_slow, salt, nonce, indicador_rapido)
        key = _derivar_chave(passphrase, salt, is_slow)
        return header + AESGCM(key).encrypt(nonce, plaintext, header)

def descriptografar(blob: bytes, passphrase: str) -> bytes:

    """Função de descriptografar

    Recebe dado criptografado e descriptografa apenas com a senha.

      Args:
        plaintext (bytes): Dado a ser descriptografado
        passphrase (str): Senha da decriptografia

    Raises:
        ValueError: arquivo muito curto quando blob < HEADER.size
        ValueError: Lentidão não definida" quando falta algo no cabeçalho

    Returns:
        bytes: Dado descriptografado
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
    """Mostra o final da senha a partir do cabeçalho (sem descriptografar nada)

    Args:
        blob (bytes): A senha criptografada

    Raises:
        ValueError: Quando tenta revelar senha do arquivo, levanta erro

    Returns:
        bytes: Dígitos finais da senha em bytes
    """
    header = blob[: HEADER.size]
    _is_slow, _salt, _nonce, digitos_senha = HEADER.unpack(header)
    if digitos_senha == b';;':
        raise ValueError
    else:
        return digitos_senha
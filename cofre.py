import seguranca

mestra = [""]
def definirSenha(senha):
    mestra[0] = senha

def senhaCorreta(tentativa):
    return tentativa == mestra[0]

def existe(caminho: str) -> bool:
    try:
        arquivo = open(caminho, "r")  
        arquivo.close()
        return True
    except FileNotFoundError: 
        return False

def lerCifrado(caminho):
    if not existe(caminho): #para caso o arquivo ainda n exista, n tem nd guardado
        return []
    arquivo = open(caminho, "r")
    textoHex = arquivo.read().strip() #strip() tira espaços e quebras de linha sobrando
    arquivo.close()

    #se o arquivo já existir mas n tiver nd dentro
    if textoHex == "": 
        return []

    #o .txt guarda o conteudo trancado escrito em hexadecimal
    #converte esse texto p bytes
    blob = bytes.fromhex(textoHex)
    #destranca c a senha mestra e converte de bytes para texto normal
    texto = seguranca.descriptografar(blob, mestra[0]).decode("utf-8")
    #separa o texto grande em linhas fazendo a lista de registros
    return texto.splitlines()

#pega lista de linhas, tranca e salva no .txt
def gravarCifrado(caminho, linhas):
    #junta todas as linhas em um texto só (uma linha por registro)
    texto = "\n".join(linhas)

    #converte o texto para bytes e tranca com a senha mestra
    #False = trancagem rapida, leva cerca de 1 segundo
    blob = seguranca.criptografar(texto.encode("utf-8"), mestra[0], False)

    #o resultado trancado sao bytes, q n dá para salvar num .txt de forma legivel o .hex() transforma em letras e numeros q cabem no .txt
    arquivo = open(caminho, "w")
    arquivo.write(blob.hex())
    arquivo.close()
##ARQUIVOSENHAS pode ser temporário
from datetime import datetime
ARQUIVOSENHAS = "Lista_senhas.txt"
## Cada registro é uma linha com os campos separados por ";":
## serviço;usuário;senha;categoria;observação;data
## Lê o arquivo e retorna uma Lista com os registros
def lerLinhas():
    open(ARQUIVOSENHAS, "a").close()
    with open(ARQUIVOSENHAS, "r") as arquivo:
        return arquivo.read().splitlines()

## Grava um arquivo de acordo com uma Lista de registros
def gravarLinhas(linhas):
    with open(ARQUIVOSENHAS, "w") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")
## Cadastro padrão mesmo :)
def cadastrar(registro):
    data = datetime.now().strftime("%d/%m/%Y %H:%M") ## Deixa no formato brasileiro
    with open(ARQUIVOSENHAS, "a") as arquivoSenhas:
        arquivoSenhas.write(f"{registro};{data}\n")
    print("Registro salvo!!!!")

## Monta o texto do registro para mostrar na tela, escondendo a senha
def formatarRegistro(linha):
    campos = linha.split(";")
    if len(campos) != 6:
        return "(registro no formato antigo: edite ou exclua)"
    servico, usuario, senha, categoria, obs, data = campos
    ## Mostra só os 2 primeiros caracteres e sempre 6 asteriscos, pra não entregar o tamanho da senha
    return f"Serviço: {servico}, Usuário/E-mail: {usuario}, Senha: {senha[:2]}******, Categoria: {categoria}, Observação: {obs}, Data: {data}"

def listar():
    linhas = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-; ")
    else:
        for i in range(len(linhas)):
            print(f"[{i + 1}] {formatarRegistro(linhas[i])}")
            ## Acessa o elemento i mas imprime como i + 1 pra ficar mais fácil de ler 

def atualizar(antigo, novo):
    linhas = lerLinhas()
    if antigo in linhas:
        data = datetime.now().strftime("%d/%m/%Y %H:%M") ## A data também muda quando o registro é alterado
        linhas[linhas.index(antigo)] = f"{novo};{data}"
        gravarLinhas(linhas)
        print("Registro atualizado! Tudo de acordo!")
        ## Substitui o novo na lista de registros e salva o arquivo com a lista de registros

    else:
        print("Registro não encontrado. ;-;")
            
def excluir(registro):
    linhas = lerLinhas()
    if registro in linhas:
        linhas.remove(registro)
        gravarLinhas(linhas)
        print("Registro excluído com sucesso! Tudo de acordo!")
    else:
        print("Registro não encontrado. ;-;")
def ultimoCadastro():
    linhas = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-;")
    else:
        print(f"Último cadastro: {formatarRegistro(linhas[-1])}") ## linhas[-1] retorna o ultimo registro


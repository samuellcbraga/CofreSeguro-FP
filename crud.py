from datetime import datetime
import cofre

ARQUIVOSENHAS = "Lista_senhas.txt"
## Cada registro é uma linha com os campos separados por ";":
## serviço;usuário;senha;categoria;observação;data
## Lê o arquivo e retorna uma Lista com os registros
def lerLinhas() -> list[str]:
    """o cofre que faz a leitura
    """
    return cofre.lerCifrado(ARQUIVOSENHAS)

## Grava um arquivo de acordo com uma Lista de registros
def gravarLinhas(linhas) -> None:
    """manda pro cofre encriptar
    """
    cofre.gravarCifrado(ARQUIVOSENHAS, linhas) #manda pro cofre encriptar

## Cadastro padrão mesmo :)
def cadastrar(registro) -> None:
    """_summary_

    Args:
        registro (_type_): _description_
    """
    data: str = datetime.now().strftime("%d/%m/%Y %H:%M") ## Deixa no formato brasileiro
    linhas = lerLinhas()  #destranca os registros
    linhas.append(f"{registro};{data}") #acrescenta o novo no fim da Lista
    gravarLinhas(linhas)   #tranca tudo e salva
    print("Registro salvo!!!!")

## Monta o texto do registro para mostrar na tela, escondendo a senha
def formatarRegistro(linha) -> str:
    """_summary_

    Args:
        linha (_type_): _description_

    Returns:
        str: _description_
    """
    campos: list[str] = linha.split(";")
    if len(campos) != 6:
        return "(registro no formato antigo: edite ou exclua)"
    servico, usuario, senha, categoria, obs, data = campos
    ## Mostra só os 2 primeiros caracteres e sempre 6 asteriscos, pra não entregar o tamanho da senha
    return f"Serviço: {servico}, Usuário/E-mail: {usuario}, Senha: {senha[:2]}******, Categoria: {categoria}, Observação: {obs}, Data: {data}"

def listar() -> None:
    """_summary_
    """
    linhas: list[str] = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-; ")
    else:
        for i in range(len(linhas)):
            print(f"[{i + 1}] {formatarRegistro(linhas[i])}")
            ## Acessa o elemento i mas imprime como i + 1 pra ficar mais fácil de ler 

def atualizar(antigo, novo) -> None:
    """_summary_

    Args:
        antigo (_type_): _description_
        novo (_type_): _description_
    """
    linhas: list[str] = lerLinhas()
    if antigo in linhas:
        data: str = datetime.now().strftime("%d/%m/%Y %H:%M") ## A data também muda quando o registro é alterado
        linhas[linhas.index(antigo)] = f"{novo};{data}"
        gravarLinhas(linhas)
        print("Registro atualizado! Tudo de acordo!")
        ## Substitui o novo na lista de registros e salva o arquivo com a lista de registros

    else:
        print("Registro não encontrado. ;-;")
            
def excluir(registro) -> None:
    """_summary_

    Args:
        registro (_type_): _description_
    """
    linhas: list[str] = lerLinhas()
    if registro in linhas:
        linhas.remove(registro)
        gravarLinhas(linhas)
        print("Registro excluído com sucesso! Tudo de acordo!")
    else:
        print("Registro não encontrado. ;-;")

def ultimoCadastro() -> None:
    """_summary_
    """
    linhas: list[str] = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-;")
    else:
        print(f"Último cadastro: {formatarRegistro(linhas[-1])}") ## linhas[-1] retorna o ultimo registro


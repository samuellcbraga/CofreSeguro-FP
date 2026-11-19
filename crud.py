##ARQUIVOSENHAS pode ser temporário
from datetime import datetime

ARQUIVOSENHAS = "Lista_senhas.txt"
## Cada registro é uma linha com os campos separados por ";":
## serviço;usuário;senha;categoria;observação;data
## Lê o arquivo e retorna uma Lista com os registros
def lerLinhas() -> list[str]:
    """Acessa o arquivo das senhas para ser usado no código

    Returns:
        list[str]: Lista das senhas registradas
    """
    open(ARQUIVOSENHAS, "a").close()
    with open(ARQUIVOSENHAS, "r") as arquivo:
        return arquivo.read().splitlines()

## Grava um arquivo de acordo com uma Lista de registros
def gravarLinhas(linhas) -> None:
    """Grava um arquivo de acordo com uma Lista de registros

    Args:
        linhas(_type_): Lista de registros
    """
    with open(ARQUIVOSENHAS, "w") as arquivo:
        arquivo.writelines(linha + "\n" for linha in linhas)
## Cadastro padrão mesmo :)
def cadastrar(registro) -> None:
    """Guarda as informações de cadastro do usuário no Lista_senhas.txt

    Args:
        registro (_type_): Informações de cadastro do usuário
    """
    data: str = datetime.now().strftime("%d/%m/%Y %H:%M") ## Deixa no formato brasileiro
    with open(ARQUIVOSENHAS, "a") as arquivoSenhas:
        arquivoSenhas.write(f"{registro};{data}\n")
    print("Registro salvo!!!!")

## Monta o texto do registro para mostrar na tela, escondendo a senha
def formatarRegistro(linha) -> str:
    """Monta o texto do registro para mostrar na tela, escondendo a senha

    Args:
        linha (_type_): Lista das senhas

    Returns:
        str: Cadastro legível, com a senha oculta
    """
    campos: list[str] = linha.split(";")
    if len(campos) != 6:
        return "(registro no formato antigo: edite ou exclua)"
    servico, usuario, senha, categoria, obs, data = campos
    ## Mostra só os 2 primeiros caracteres e sempre 6 asteriscos, pra não entregar o tamanho da senha
    #descriptografa a senha antes de mostrar 
    return f"Serviço: {servico}, Usuário/E-mail: {usuario}, Senha: {senha[:2]}******, Categoria: {categoria}, Observação: {obs}, Data: {data}"

def listar() -> None:
    """Acessa e escreve todas as senhas de maneira ordenada
    """
    linhas: list[str] = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-; ")
    else:
        for i in range(len(linhas)):
            print(f"[{i + 1}] {formatarRegistro(linhas[i])}")
            ## Acessa o elemento i mas imprime como i + 1 pra ficar mais fácil de ler 

def atualizar(antigo, novo) -> None:
    """Acessa um registro existente e o substitui por um novo input

    Args:
        antigo (_type_): Registro existente
        novo (_type_): Novo registro
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
    """Exclui um registro da lista de senhas

    Args:
        registro (_type_): Nome do registro
    """
    linhas: list[str] = lerLinhas()
    if registro in linhas:
        linhas.remove(registro)
        gravarLinhas(linhas)
        print("Registro excluído com sucesso! Tudo de acordo!")
    else:
        print("Registro não encontrado. ;-;")

def ultimoCadastro() -> None:
    """Retorna o último item da lista de senhas
    """
    linhas: list[str] = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-;")
    else:
        print(f"Último cadastro: {formatarRegistro(linhas[-1])}") ## linhas[-1] retorna o ultimo registro


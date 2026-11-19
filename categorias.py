## Categorias das credenciais. Cada linha do arquivo é: nome;exigência mínima de força
## A exigência é "fraca", "média" ou "forte" (ver VerificadorDeSenha.NIVEIS)
ARQUIVOCATEGORIAS = "categorias.txt"
## Usadas na primeira vez que o programa roda. O usuário pode mudar as exigências pelo menu.
CATEGORIASPADRAO: list[str] = ["banco;forte", "rede social;média", "estudo;média", "trabalho;forte", "outros;fraca"]

## Lê o arquivo e retorna uma Lista com as categorias (cria o arquivo com as padrão se não existir)
def lerCategorias() -> list[str]:
    """_summary_

    Returns:
        list[str]: _description_
    """
    open(ARQUIVOCATEGORIAS, "a").close() ## Cria o arquivo vazio se ele não existir (igual ao crud.py)
    with open(ARQUIVOCATEGORIAS, "r", encoding="utf-8") as arquivo:
        linhas: list[str] = arquivo.read().splitlines()
    if len(linhas) == 0:
        gravarCategorias(CATEGORIASPADRAO)
        return list(CATEGORIASPADRAO)
    return linhas

def gravarCategorias(linhas) -> None:
    """_summary_

    Args:
        linhas (_type_): _description_
    """
    with open(ARQUIVOCATEGORIAS, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(linha + "\n" for linha in linhas)

def listar() -> list[str]:
    """_summary_

    Returns:
        list[str]: _description_
    """
    linhas: list[str] = lerCategorias()
    for i in range(len(linhas)):
        nome, exigencia = linhas[i].split(";")
        print(f"[{i + 1}] {nome} (senha mínima: {exigencia})")
    return linhas

## Se a categoria já existe, muda a exigência dela. Se não existe, cadastra.
def cadastrar(nome, exigencia) -> None:
    """_summary_

    Args:
        nome (_type_): _description_
        exigencia (_type_): _description_
    """
    linhas: list[str] = lerCategorias()
    for i in range(len(linhas)):
        if linhas[i].split(";")[0] == nome:
            linhas[i] = f"{nome};{exigencia}"
            gravarCategorias(linhas)
            print("Exigência da categoria atualizada!")
            return
    linhas.append(f"{nome};{exigencia}")
    gravarCategorias(linhas)
    print("Categoria cadastrada!")

## Retorna a exigência mínima de uma categoria ("fraca" se ela não existir mais)
def exigenciaDa(nome: str) -> str:
    """

    Args:
        nome (str): _description_

    Returns:
        str: _description_
    """
    for linha in lerCategorias():
        nomeCategoria, exigencia = linha.split(";")
        if nomeCategoria == nome:
            return exigencia
    return "fraca"

## Só aceita letras e espaços, até 20 caracteres (evita texto estranho indo pro assistente de IA)
def nomeValido(nome: str) -> bool:
    """confere se o nome da categoria é seguro
    """
    if nome == "" or len(nome) > 20:
        return False
    for letra in nome:
        if not (letra.isalpha() or letra == " "): #isalpha() aceita acento, então "saúde" passa
            return False
    return True

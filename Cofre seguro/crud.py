##ARQUIVOSENHAS pode ser temporário
 
ARQUIVOSENHAS = "Lista_senhas.txt"
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
    with open(ARQUIVOSENHAS, "a") as arquivoSenhas:
        arquivoSenhas.write(registro + "\n")
    print("Registro salvo!!!!")

def listar():
    linhas = lerLinhas()
    if len(linhas) == 0:
        print("Não há nenhum registro ;-; ")
    else:
        for i in range(len(linhas)):
            print(f"[{i + 1}] {linhas[i]}")
            ## Acessa o elemento i mas imprime como i + 1 pra ficar mais fácil de ler 

def atualizar(antigo, novo):
    linhas = lerLinhas()
    if antigo in linhas:
        linhas[linhas.index(antigo)] = novo
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
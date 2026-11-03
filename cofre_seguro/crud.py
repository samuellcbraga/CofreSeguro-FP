def cadastrar(nome):
    arquivo = open("nome.txt", "a")
    arquivo.write(nome + "\n")
    arquivo.close()
    
def listar():
    arquivo = open("nome.txt", "r")
    nomes = arquivo.readlines()
    arquivo.close()
    
    if len(nomes) == 0:
        print("Não há nada registrado")
    else:
        print("Lista de nomes: ")
        for i in range(len(nomes)):
            print(nomes[i].strip())
            
def atualizar(nome, novo_nome):
    arquivo = open("nome.txt", "w")
    nomes = arquivo.readlines()
    for i in range(len(nomes)):
        if nomes[i] == nome:
            nomes = novo_nome
            print("Nome atualizado com sucesso!")
        else:
            print("Nome não encontrado.")
            
def excluir(nome):
    arquivo = open("nome.txt", "w")
    nomes = arquivo.readlines()
    for i in range(len(nomes)):
        if nomes[i] == nome:
            nomes.pop(i)
            print("Nome excluído com sucesso!")
        else:
            print("Nome não encontrado.")

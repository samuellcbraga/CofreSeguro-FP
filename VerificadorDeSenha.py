simbolos = "!@#$%&*()-_=+[]{};:,.<>?/|"

def verificar_forca_senha(senha: str) -> int: #pra quem nao souber, (: str) e (-> int) quer dizer: a senha será um texto e a função vai retornar um valor inteiro 
    # retorna uma pontuação que indica a força da senha
    # quanto maior a pontuação, mais forte é a senha
    

    global tipos_presentes #global tipos_presentes fala pro Python: “esta variável não é local”. Sem o global, o Python criaria uma variável nova que morre quando a função termina
    pontuacao = 0
    tipos_presentes = 0
    # verifica se a senha contém ao menos um caractere de cada classe exigida
    if any(c.isupper() for c in senha): #for c in senha percorre a senha letra por letra, e "c" é cada caractere
        pontuacao += 1                  #c.isupper() é True se o caractere é uma letra maiúscula
        tipos_presentes += 1            #any() recebe todos esses True/False e devolve True >se pelo menos um for True<. Ele para na primeira maiúscula que achar
        #Se tem maiúscula, soma 1 na pontuação e marca tipos_presentes (variável q criei pra contar caractere especial, letra maiuscula etc)
    if any(c.islower() for c in senha):  
        pontuacao += 1                  #o que disse antes vale pra todo o resto, mudando só a função abordada
        tipos_presentes += 1
    if any(c.isdigit() for c in senha):
        pontuacao += 1
        tipos_presentes += 1
    if any(c in simbolos for c in senha):
        pontuacao += 1
        tipos_presentes += 1

    if tipos_presentes < 4:
        return pontuacao

    # verifica se a senha é longa o bastante
    if len(senha) >= 8:
        pontuacao += 1
    if len(senha) >= 12:
        pontuacao += 1
    if len(senha) >= 16:
        pontuacao += 1
    if len(senha) >= 20:        #coloquei quatro if's separados para que a pontuação seja acumulada conforme o tamanho for aumentando
        pontuacao += 1      

    return pontuacao


def verificar_senha(senha: str) -> None:
    #verifica a senha em vários aspectos e imprime uma mensagem sobre sua força

    #lê a lista de senhas comuns do arquivo
    with open("senhas_comuns.txt", "r") as arquivo: #"with ... as arquivo" garante que o arquivo é fechado sozinho ao sair do bloco \\ arquivo.read() lê todo o conteúdo como um único texto 
        senhas_comuns = set(arquivo.read().splitlines()) #set() transforma a lista em um conjunto

    # verifica se a senha é comum demais
    if senha in senhas_comuns:
        print("A senha é muito comum. A força da sua senha é 0.")
        return

    # verifica a força da senha
    pontuacao = verificar_forca_senha(senha)
    if pontuacao == 0:
        print("A senha é muito fraca. \n")
        if tipos_presentes < 4:
            print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. \n")
    elif pontuacao == 1:
        print("A senha é fraca. \n")
        if tipos_presentes < 4:
            print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. \n")
    elif pontuacao == 2:
        print("A senha é mediana. \n")
        if tipos_presentes < 4:
            print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. \n")
    elif pontuacao == 3:
        print("A senha não é tão forte. \n")
        if tipos_presentes < 4:
            print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. \n")
    elif pontuacao == 4:
        print("A senha não é tão forte. \n")
        if tipos_presentes < 4:
            print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. \n")
    else:
        print("A senha é extremamente forte. \n")


while True:
    print("Cadastre aqui sua senha com os seguintes critérios: \n"
      "         *Ao menos 8 digitos\n"
      "         *Ao menos uma letra MAIÚSCULA\n"
      "         *Ao menos um número\n"
      "         *Ao menos um caractere especial(!@#$%¨&)\n")
    senha = input("Digite sua senha: ")
    verificar_senha(senha)

simbolos = "!@#$%&*()-_=+[]{};:,.<>?/|"

def ler_senhas_comuns() -> set: #lê a lista de senhas comuns do arquivo
    with open("senhas_comuns.txt", "r") as arquivo: #"with ... as arquivo" garante que o arquivo é fechado sozinho ao sair do bloco \\ arquivo.read() lê todo o conteúdo como um único texto
        return set(arquivo.read().splitlines()) #set() transforma a lista em um conjunto

def verificar_forca_senha(senha: str) -> int: #pra quem nao souber, (: str) e (-> int) quer dizer: a senha será um texto e a função vai retornar um valor inteiro 
    # retorna uma pontuação que indica a força da senha
    # quanto maior a pontuação, mais forte é a senha
    

    global tipos_presentes #global tipos_presentes fala pro Python: “esta variável não é local”. Sem o global, o Python criaria uma variável nova que morre quando a função termina
    pontuacao = 0
    tipos_presentes = 0
    if senha in ler_senhas_comuns(): #senha comum vale 0, não importa quão "forte" ela pareça
        return pontuacao
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

    senhas_comuns = ler_senhas_comuns()

    # verifica se a senha é comum demais
    if senha in senhas_comuns:
        print("A senha é muito comum. A força da sua senha é 0.")
        print("Sua senha não foi cadastrada. Por favor, cadastre outra senha.")
        return

    # verifica a força da senha
    pontuacao = verificar_forca_senha(senha)
    if pontuacao == 0:
        print("A senha é muito fraca. \n")
        if tipos_presentes < 4:
            explicar_o_que_falta(senha)
    elif pontuacao == 1:
        print("A senha é fraca. \n")
        if tipos_presentes < 4:
            explicar_o_que_falta(senha)
    elif pontuacao == 2:
        print("A senha é mediana. \n")
        if tipos_presentes < 4:
            explicar_o_que_falta(senha)
    elif pontuacao == 3:
        print("A senha não é tão forte. \n")
        if tipos_presentes < 4:
            explicar_o_que_falta(senha)
    elif pontuacao == 4:
        print("A senha não é tão forte. \n")
        if tipos_presentes < 4:
            explicar_o_que_falta(senha)
    else:
        print("A senha é extremamente forte. \n")

    #o tamanho só conta pontos quando a senha já tem os 4 tipos de caractere
    if tipos_presentes == 4 and len(senha) < 20:
        print(f"Sua senha tem {len(senha)} caracteres. Senhas maiores ganham mais pontos (a partir de 8, 12, 16 e 20 caracteres). \n")


def explicar_o_que_falta(senha: str) -> None:
    #em vez de repetir todos os critérios, diz exatamente o que está faltando
    print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. Falta:")
    if not any(c.isupper() for c in senha):
        print("   - uma letra maiúscula")
    if not any(c.islower() for c in senha):
        print("   - uma letra minúscula")
    if not any(c.isdigit() for c in senha):
        print("   - um número")
    if not any(c in simbolos for c in senha):
        print("   - um caractere especial")
    print()


#classificação usada para comparar com a exigência mínima de cada categoria
NIVEIS = ["fraca", "média", "forte"]

def classificar(pontuacao: int) -> str:
    #segue as mensagens acima: 0 e 1 = fraca | 2 a 4 = mediana / não tão forte | 5 ou mais = extremamente forte
    if pontuacao >= 5:
        return "forte"
    if pontuacao >= 2:
        return "média"
    return "fraca"

def atende_exigencia(pontuacao: int, exigencia: str) -> bool:
    #pontuação 0 (senha comum ou muito fraca) nunca é aceita, em nenhuma categoria
    if pontuacao == 0:
        return False
    #NIVEIS.index transforma o nome em posição (fraca = 0, média = 1, forte = 2) para poder comparar
    return NIVEIS.index(classificar(pontuacao)) >= NIVEIS.index(exigencia)



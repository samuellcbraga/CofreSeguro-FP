SIMBOLOS: str = "!@#$%&*()-_=+[]{};:,.<>?/|"

def ler_senhas_comuns() -> set[str]: 
    """Função feita para que, posteriormente, a senha registrada percorra linha por linha desse .txt e, caso seja idêntica a uma das senhas listadas, não seja registrada

    Returns:
        set[str]: As senhas comuns encontradas no arquivo em forma de string, sem repetições e sem as quebras de linha
    """
    with open("senhas_comuns.txt", "r") as arquivo: 
        return set(arquivo.read().splitlines())

def verificar_forca_senha(senha: str) -> tuple[int,int]:   
    """Retorna uma pontuação que indica a força da senha. Quão maior a pontuação, mais forte é a senha.
    Percorre cada caractere da senha e devolve True caso atenda aos requisitos obrigatórios da senha (ter letra maiúscula, número etc).
    Conforme a senha é percorrida e os tipos presentes forem confirmados, recebe uma pontuação acumulativa

    Args:
        senha (str): recebe a senha

    Returns:
        tuple[int,int]: depois de analisar a senha, devolve dois inteiros que servem como variáveis acumuladoras: pontuacao e tipos_presentes
    """
    # retorna uma pontuação que indica a força da senha//quanto maior a pontuação, mais forte é a senha
    
    pontuacao: int = 0
    tipos_presentes: int = 0

    if senha.lower() in ler_senhas_comuns(): #lower() pra "Senha123" também contar como comum. Senha comum vale 0, não importa quão "forte" ela pareça
        return (pontuacao, tipos_presentes)


    
    # agora vamos verificar se a senha contém ao menos um caractere de cada classe exigida

    if any(c.isupper() for c in senha): #c.isupper() é True se o caractere é uma letra maiúscula
        pontuacao += 1                  #any() recebe todos esses True/False e devolve True >se pelo menos um for True<. Ele para na primeira maiúscula que achar
        tipos_presentes += 1            
    if any(c.islower() for c in senha):  
        pontuacao += 1                  #o que disse antes vale pra todo o resto, mudando só a função abordada
        tipos_presentes += 1
    if any(c.isdigit() for c in senha):
        pontuacao += 1
        tipos_presentes += 1
    if any(c in SIMBOLOS for c in senha):
        pontuacao += 1
        tipos_presentes += 1

    if tipos_presentes < 4:
        return pontuacao,tipos_presentes

    # verifica se a senha é longa o bastante//sistema de pontuação é acumulativo nessa etapa
    if len(senha) >= 8:
        pontuacao += 1
    if len(senha) >= 12:
        pontuacao += 1
    if len(senha) >= 16:
        pontuacao += 1
    if len(senha) >= 20:        
        pontuacao += 1      

    return pontuacao,tipos_presentes


def verificar_senha(senha: str) -> None:
    """Verifica a força da senha.
    Primeiramente iremos analisar se ela tá listada em "senhas_comuns" (se estiver lá a senha não será listada); Caso contrário ela será analisada:
    1. calcula a pontuação e devolve o nível de força
    2. caso falte algum tipo de caractere, será retornado uma mensagem explicada na função explicar_o_que_falta


    Args:
        senha (str): recebe a senha que será analisada
    """
    #verifica a senha em vários aspectos e imprime uma mensagem sobre sua força

    senhas_comuns: set[str] = ler_senhas_comuns()

    # verifica se a senha é comum demais
    if senha.lower() in senhas_comuns: #lower() igual ao verificar_forca_senha
        print("A senha é muito comum. A força da sua senha é 0.")
        print("Sua senha não foi cadastrada. Por favor, cadastre outra senha.")
        return

    # verifica a força da senha e imprime o que falta para ela ser considerada forte
    pontuacao_senha_atual, tipos_presentes_senha_atual= verificar_forca_senha(senha)
    if pontuacao_senha_atual == 0:
        print("A senha é muito fraca. \n")
        if tipos_presentes_senha_atual < 4:
            explicar_o_que_falta(senha)
    elif pontuacao_senha_atual == 1:
        print("A senha é fraca. \n")
        if tipos_presentes_senha_atual < 4:
            explicar_o_que_falta(senha)
    elif pontuacao_senha_atual == 2:
        print("A senha é mediana. \n")
        if tipos_presentes_senha_atual < 4:
            explicar_o_que_falta(senha)
    elif pontuacao_senha_atual == 3 or pontuacao_senha_atual == 4:
        print("A senha não é tão forte. \n")
        if tipos_presentes_senha_atual < 4:
            explicar_o_que_falta(senha)
    else:
        print("A senha é extremamente forte. \n")

    #o tamanho só conta pontos quando a senha já tem os 4 tipos de caracteres
    if tipos_presentes_senha_atual == 4 and len(senha) < 20:
        print(f"Sua senha tem {len(senha)} caracteres. Senhas maiores ganham mais pontos (a partir de 8, 12, 16 e 20 caracteres). \n")


def explicar_o_que_falta(senha: str) -> None:
    """Explica o que falta, percorrendo a senha caractere por caractere. Lista os tipos de caractere exigidos

    Args:
        senha (str): senha a ser analisada
    """
    #diz exatamente o que está faltando
    print("A senha deve conter ao menos uma letra maiúscula, uma letra minúscula, um caractere especial e ao menos um número. Falta:")
    if not any(c.isupper() for c in senha):
        print("   - uma letra maiúscula")
    if not any(c.islower() for c in senha):
        print("   - uma letra minúscula")
    if not any(c.isdigit() for c in senha):
        print("   - um número")
    if not any(c in SIMBOLOS for c in senha):
        print("   - um caractere especial")
    print()


#classificação usada para comparar com a exigência mínima de cada categoria
#fraca == 0//média == 1//forte == 2
NIVEIS: list[str] = ["fraca", "média", "forte"]

def classificar(pontuacao: tuple[int,int]) -> str:
    """Classifica a pontuação de uma senha em "fraca", "média" ou "forte".

    Args:
        pontuacao (tuple[int,int]): Recebe a tupla (pontuacao, tipos_presentes) e devolve a pontuação

    Returns:
        str: O nível da senha: "fraca" (0 ou 1), "média" (2 a 4) ou "forte" (5 ou mais)

    """
    #segue as mensagens acima: 0 e 1 = fraca | 2 a 4 = mediana / não tão forte | 5 ou mais = extremamente forte
    if pontuacao[0] >= 5:
        return "forte"
    if pontuacao[0] >= 2:
        return "média"
    return "fraca"

def atende_exigencia(pontuacao: tuple[int,int], exigencia: str) -> bool:
    """Aqui verificamos se a senha atinge o nível mínimo requerido pela escolha feita em menu.py

    Args:
        pontuacao (tuple[int,int]): a tupla (pontuacao,tipos_presentes) é devolvida pela função verificar_forca_senha
        exigencia (str): nível mínimo aceito baseado na escolha feita no menu.py, sendo elas: fraca, média ou forte

    Returns:
        bool: True se o nível da senha for igual ou superior ao exigido; False se for inferior ou se a pontuação for 0
    """
    #pontuação 0 (senha comum ou muito fraca) nunca é aceita, em nenhuma categoria
    if pontuacao[0] == 0:
        return False
    #NIVEIS.index transforma o nome em posição (fraca = 0, média = 1, forte = 2) para poder comparar
    return NIVEIS.index(classificar(pontuacao)) >= NIVEIS.index(exigencia)



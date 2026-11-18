SIMBOLOS: str = "!@#$%&*()-_=+[]{};:,.<>?/|"

def ler_senhas_comuns() -> set[str]: 
    """_summary_

    Returns:
        set[str]: _description_
    """
    with open("senhas_comuns.txt", "r") as arquivo: 
        return set(arquivo.read().splitlines())

def verificar_forca_senha(senha: str) -> tuple[int,int]:   
    """_summary_

    Args:
        senha (str): _description_

    Returns:
        tuple[int,int]: _description_
    """
    # retorna uma pontuação que indica a força da senha//quanto maior a pontuação, mais forte é a senha
    
    pontuacao: int = 0
    tipos_presentes: int = 0

    if senha in ler_senhas_comuns(): #senha comum vale 0, não importa quão "forte" ela pareça
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
    """_summary_

    Args:
        senha (str): _description_
    """
    #verifica a senha em vários aspectos e imprime uma mensagem sobre sua força

    senhas_comuns: set[str] = ler_senhas_comuns()

    # verifica se a senha é comum demais
    if senha in senhas_comuns:
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
    """_summary_

    Args:
        senha (str): _description_
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
NIVEIS: list[str] = ["fraca", "média", "forte"]

def classificar(pontuacao: tuple[int,int]) -> str:
    """_summary_

    Args:
        pontuacao (tuple[int,int]): _description_

    Returns:
        str: _description_
    """
    #segue as mensagens acima: 0 e 1 = fraca | 2 a 4 = mediana / não tão forte | 5 ou mais = extremamente forte
    if pontuacao[0] >= 5:
        return "forte"
    if pontuacao[0] >= 2:
        return "média"
    return "fraca"

def atende_exigencia(pontuacao: tuple[int,int], exigencia: str) -> bool:
    """_summary_

    Args:
        pontuacao (tuple[int,int]): _description_
        exigencia (str): _description_

    Returns:
        bool: _description_
    """
    #pontuação 0 (senha comum ou muito fraca) nunca é aceita, em nenhuma categoria
    if pontuacao[0] == 0:
        return False
    #NIVEIS.index transforma o nome em posição (fraca = 0, média = 1, forte = 2) para poder comparar
    return NIVEIS.index(classificar(pontuacao)) >= NIVEIS.index(exigencia)



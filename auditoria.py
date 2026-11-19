from datetime import datetime
import cofre

ARQUIVOLOG = "auditoria.txt"

#cada linha do log: data e hora;operação;serviço
def registrar(operacao, servico) -> None:
    """Registra as operações realizadas pelo usuário no arquivo "auditoria.txt"
    """
    data: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        linhas = cofre.lerCifrado(ARQUIVOLOG) #destranca o log
        linhas.append(f"{data};{operacao};{servico}") #coloca a nova operacao
        cofre.gravarCifrado(ARQUIVOLOG, linhas) #tranca dnv
    except OSError: #o programa não pode quebrar por causa do log
        print("Aviso: não foi possível gravar no log de auditoria.")

def listar() -> None:
    """Descriptografa, lê e escreve no terminal a auditoria
    """
    open(ARQUIVOLOG, "a", encoding="utf-8").close() #cria o arquivo vazio se ainda não existir
    try:
        linhas = cofre.lerCifrado(ARQUIVOLOG)  #destranca o log
    except OSError:
        print("Não foi possível ler o log de auditoria.")
        return
    if len(linhas) == 0:
        print("O log está vazio.")
        return
    print("----------- LOG DE AUDITORIA -----------")
    for linha in linhas:
        celulas: list[str] = linha.split(";")
        if len(celulas) == 3:  
            data, operacao, servico = celulas
            print(f"{data} | {operacao} | {servico}")

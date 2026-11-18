from io import TextIOWrapper
from datetime import datetime

ARQUIVOLOG = "auditoria.txt"

#cada linha do log: data e hora;operação;serviço
def registrar(operacao, servico) -> None:
    data: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        arquivo: TextIOWrapper = open(ARQUIVOLOG, "a", encoding="utf-8")
        arquivo.write(f"{data};{operacao};{servico}\n")
        arquivo.close()
    except OSError: #o programa não pode quebrar por causa do log
        print("Aviso: não foi possível gravar no log de auditoria.")

def listar() -> None:
    open(ARQUIVOLOG, "a", encoding="utf-8").close() #cria o arquivo vazio se ainda não existir
    try:
        with open(ARQUIVOLOG, "r", encoding="utf-8") as arquivo:
            linhas: list[str] = arquivo.read().splitlines()
    except OSError:
        print("Não foi possível ler o log de auditoria.")
        return
    if len(linhas) == 0:
        print("O log está vazio.")
        return
    print("----------- LOG DE AUDITORIA -----------")
    for linha in linhas:
        celulas = linha.split(";")
        if len(celulas) == 3:  
            data, operacao, servico = celulas
            print(f"{data} | {operacao} | {servico}")
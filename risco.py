from datetime import datetime
import crud
import VerificadorDeSenha

#monta um dicionario onde a chave é a senha e o valor é a lista de servicos que usam essa senha
def agruparPorSenha() -> dict[str, list [str]]:
    """monta um dicionario onde a chave é a senha e o valor é a lista de servicos que usam essa senha
    """
    grupos: dict[str, list[str]] = {}
    for linha in crud.lerLinhas():
        celulas: list[str] = linha.split(";")
        if len(celulas) == 6: #ignora registros em outro formato
            servico: str = celulas[0]
            senha: str = celulas[2]  #a senha é a 3a celula do registro
            if senha not in grupos:
                grupos[senha] = [] #primeira vez que a senha aparece, cria a lista
            grupos[senha].append(servico) #acrescenta o servico na lista dessa senha
    return grupos


def avisarRepetidas() -> None:
    """
        antes de salvar uma senha, avisa se ela ja ta sendo usada em outro canto
    """
    grupos: dict[str, list[str]] = agruparPorSenha()
    achou: bool = False
    for senha in grupos:  # noqa: PLC0206
        if len(grupos[senha]) > 1:
            achou = True
            #join junta a lista num texto só, separado por vírgula (n dá pra somar texto + lista)
            print("Mesma senha nos serviços: " + ", ".join(grupos[senha]))
    if not achou:
        print("Nenhuma senha repetida.")

def servicosComMesmaSenha(senha: str) -> list[str]:
    """antes de salvar uma senha, retorna os servicos que ja usam ela
    """
    grupos: dict[str, list[str]] = agruparPorSenha()
    if senha in grupos:
        return grupos.get(senha)
    return[]


def relatorio():
    """_summary_
    """
    comuns = VerificadorDeSenha.ler_senhas_comuns()
    total = 0
    fracas = 0
    qtdComuns = 0
    print("Tempo desde a última alteração: ")
    for linha in crud.lerLinhas():
        celulas = linha.split(";")
        if len(celulas) == 6:
            total += 1
            senha = celulas[2]
            pontuacao = VerificadorDeSenha.verificar_forca_senha(senha)
            if VerificadorDeSenha.classificar(pontuacao) == "fraca":     
                fracas += 1
            if senha.lower() in comuns:  #coloquei lower() para "Senha" tb ser considerada fraca
                qtdComuns += 1
            ## strptime transforma texto do datatime em uma data de verdade
            ## subtrai duas datas, que dá a quantidade de dias dsd q foi salva/alterada
            dias = (datetime.now() - datetime.strptime(celulas[5], "%d/%m/%Y %H:%M")).days
            print(f"   - {celulas[0]}: {dias} dia(s)")

    #conta quantas senhas aparecem em mais de um lugar
    repetidas = 0
    grupos = agruparPorSenha()
    for senha in grupos:
        if len(grupos[senha]) > 1:
            repetidas += 1

    print(f"\nCredenciais: {total}")
    print(f"Senhas fracas: {fracas}")
    print(f"Senhas na lista de comuns: {qtdComuns}")
    print(f"Senhas repetidas: {repetidas}")
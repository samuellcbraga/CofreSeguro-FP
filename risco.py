from datetime import datetime
import crud
import VerificadorDeSenha

#monta um dicionario onde a chave é a senha e o valor é a lista de servicos que usam essa senha
def agruparPorSenha():
    grupos = {}
    for linha in crud.lerLinhas():              
        celula = linha.split(";")
        if len(celula) == 6:        #ignora registros em outro formato
            servico = celula[0]
            senha = celula[2]           #a senha é a 3a celula do registro
            if senha not in grupos:
                grupos[senha] = []       #primeira vez que a senha aparece, entao ele cria a lista
            grupos[senha].append(servico)
    return grupos

#se uma senha tem mais de um servico na lista, ela tá repetida
def avisarRepetidas():
    grupos = agruparPorSenha()
    achou = False
    for senha in grupos:
        if len(grupos[senha]) > 1:
            achou = True
            print("Mesma senha nos serviços: " + ", ".join(grupos[senha]))
    if not achou:
        print("Nenhuma senha repetida.")

#antes de salvar uma senha, avisa se ela ja ta sendo usada em outro canto
#NAO TO SABENDO ATIVAR ESSE MEGA PODER LÁ NO MENU!!!!!!!!!!!!!
def servicosComMesmaSenha(senha):
    grupos = agruparPorSenha()
    if senha in grupos:
        return grupos[senha]
    return []

def relatorio():
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
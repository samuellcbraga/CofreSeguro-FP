from datetime import datetime
import agente
import auditoria
import categorias
import crud
import risco
import VerificadorDeSenha

NOMESISTEMA = "CofreSeguro"

## Monta o texto que vai pro agente, uma linha por credencial
## Senha, usuário, observação e nome do serviço NÃO entram: só vai o que foi calculado aqui no pc
def montarDados() -> str:
    """monta o texto com os dados que podem ser enviados pro agente
    """
    comuns: set[str] = VerificadorDeSenha.ler_senhas_comuns()
    grupos: dict[str, list[str]] = risco.agruparPorSenha()

    #dá um número pra cada senha repetida, assim o agente sabe quais são iguais sem ver a senha
    numeroDoGrupo: dict[str, int] = {}
    for senha in grupos:
        if len(grupos[senha]) > 1:
            numeroDoGrupo[senha] = len(numeroDoGrupo) + 1

    texto: str = "numero;categoria;forca;senha_comum;grupo_repetida;dias_desde_alteracao\n"
    linhas: list[str] = crud.lerLinhas()
    for i in range(len(linhas)):
        celulas: list[str] = linhas[i].split(";")
        if len(celulas) == 6: #ignora registros em outro formato
            senha: str = celulas[2]  #usada só pra calcular, NÃO é enviada
            categoria: str = celulas[3]
            if not categorias.nomeValido(categoria): #categoria antiga com texto estranho n vai
                categoria = "outros"
            forca: str = VerificadorDeSenha.classificar(VerificadorDeSenha.verificar_forca_senha(senha))
            comum: str = "sim" if senha.lower() in comuns else "não"
            grupo: str = str(numeroDoGrupo[senha]) if senha in numeroDoGrupo else "-"
            ## mesma conta do risco.relatorio(): hoje - data salva = dias
            dias: int = (datetime.now() - datetime.strptime(celulas[5], "%d/%m/%Y %H:%M")).days
            ## manda o número do registro (o mesmo do crud.listar) em vez do nome do serviço
            texto += f"{i + 1};{categoria};{forca};{comum};{grupo};{dias}\n"
    return texto

## Conta os números de verdade direto dos dados, sem IA
## Se a resposta da IA for manipulada, essa conferência mostra o contrário logo abaixo
def mostrarConferencia(dados: str) -> None:
    """mostra um resumo calculado localmente pra conferir a resposta da IA
    """
    fracas: int = 0
    comuns: int = 0
    grupos: list[str] = []
    linhas: list[str] = dados.splitlines()[1:] #pula o cabeçalho
    for linha in linhas:
        celulas: list[str] = linha.split(";")
        if celulas[2] == "fraca":
            fracas += 1
        if celulas[3] == "sim":
            comuns += 1
        if celulas[4] != "-" and celulas[4] not in grupos:
            grupos.append(celulas[4])
    print(f"Conferência (calculada no seu pc): {len(linhas)} credenciais, {fracas} fracas, "
          f"{comuns} comuns, {len(grupos)} grupo(s) de senha repetida")

def perguntar() -> None:
    """deixa o usuário fazer perguntas sobre as senhas até apertar ENTER sem digitar nada
    """
    dados: str = montarDados() #descriptografa uma vez só, fora do loop
    if dados.count("\n") == 1: #só tem o cabeçalho, ou seja, nenhum registro
        print("Não há nenhum registro ;-; Cadastre alguma senha antes de perguntar.")
        return

    print("----------- ASSISTENTE DE IA -----------")
    print("Senhas, usuários, observações e nomes dos serviços NÃO são enviados.")
    print("Na resposta, cada credencial aparece pelo número desta lista:")
    crud.listar()
    while True:
        pergunta: str = input("\nPergunta (ENTER p voltar ao menu): ").strip()
        if pergunta == "":
            break
        resposta: str | None = agente.falar_com_agente_texto(dados, pergunta, NOMESISTEMA)
        if resposta is not None:
            mostrarConferencia(dados)
        #tira o ";" pra n quebrar a linha do log (data;operação;serviço)
        pergunta = pergunta.replace(";", ",")
        if resposta is None:
            auditoria.registrar("PERGUNTA IA (FALHOU)", pergunta)
        else:
            auditoria.registrar("PERGUNTA IA", pergunta)

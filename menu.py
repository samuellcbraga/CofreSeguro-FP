import auditoria
import categorias
import crud
import risco
import VerificadorDeSenha
import cofre



## Igual ao input, mas não aceita ";" (é o separador dos campos no arquivo)
def entrada(mensagem: str) -> str:
    """_summary_

    Args:
        mensagem (str): _description_

    Returns:
        str: _description_
    """
    texto: str = input(mensagem)
    while ";" in texto:
        print('O caractere ";" não é permitido. Tente de novo.')
        entrada(mensagem)
    return texto

## Igual ao int(input()), mas não deixa o programa quebrar se o usuário digitar letras
def lerNumero(mensagem: str) -> int:
    """_summary_

    Arg
        mensagem (str): _description_

    Returns:
        int: _description_
    """
    texto: str = input(mensagem).strip()
    while not texto.isdigit(): ## isdigit() é True só se o texto tiver apenas algarismos
        print("Digite apenas números.")
        lerNumero(mensagem)
    return int(texto)

## Mostra as categorias e retorna o nome da escolhida
def escolherCategoria() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    linhas: list[str] = categorias.listar()
    numero: int = lerNumero("Qual a categoria?: ")
    while not 1 <= numero <= len(linhas):
        print("Número inválido.")
        escolherCategoria()
    return linhas[numero - 1].split(";")[0]

def lerExigencia() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    exigencia: str = input("Exigência mínima de força da senha (fraca, média ou forte): ").strip().lower()
    while exigencia not in VerificadorDeSenha.NIVEIS:
        print("Digite fraca, média ou forte.")
        exigencia = input("Exigência mínima de força da senha (fraca, média ou forte): ").strip().lower()
    return exigencia

def entrar():
    if cofre.existe(crud.ARQUIVOSENHAS):
        tentativas=0
        while tentativas < 3:
            cofre.definirSenha(input("Senha mestra: "))
            try:
                crud.lerLinhas()
                return True
            except Exception:
                print("Senha mestra incorreta.")
                tentativas += 1
            return False



    print("Primeira execução: crie sua senha mestra.")
    senha1 = input("Nova senha mestra: ")
    senha2 = input("Repita a senha mestra: ")
    while senha1 == "" or senha1 != senha2:
            print("As senhas não conferem. Tente de novo.")
            senha1 = input("Nova senha mestra: ")
            senha2 = input("Repita a senha mestra: ")
            cofre.definirSenha(senha1)
            crud.gravarLinhas([])
    return True

if not entrar():
    print("Acesso negado.")
    exit()

while True:
    print("----------------- GERENCIADOR DE SENHAS ----------------")
    print("Opções: ")
    print("[1] - Adicionar nova senha\n[2] - Visualizar senhas\n[3] - Editar informações\n[4] - Excluir senhas\n[5] - Assistente de IA\n[6] - Ver último cadastro\n[7] - Revelar uma senha\n[8] - Categorias\n[9] - Encerrar programa\n[10] - Ver locais com mesma senha\n[11] - Ver senhas em risco\n[12] - Registro de auditoria")
    escolha: int = lerNumero("\nO que deseja fazer?: ")
    match escolha:
        case 1:
            servico: str = entrada("Qual serviço que terá sua senha registrada?: ")
            user: str = entrada("Qual o seu nome de usuário ou e-mail?: ")
            categoria: str = escolherCategoria()
            senha: str = entrada("Cadastre aqui sua senha com os seguintes critérios: \n"
                        "         *Ao menos 8 digitos\n"
                        "         *Ao menos uma letra MAIÚSCULA\n"
                        "         *Ao menos um número\n"
                        "         *Ao menos um caractere especial(!@#$%¨&)\n"
                        "Escreva aqui: ")
            #antes de add a senha tem a verificaçao de segurança
            pontuacao: tuple[int,int] = VerificadorDeSenha.verificar_forca_senha(senha)
            VerificadorDeSenha.verificar_senha(senha)
            if not VerificadorDeSenha.atende_exigencia(pontuacao, categorias.exigenciaDa(categoria)):
                print(f"A categoria {categoria} exige senha no mínimo {categorias.exigenciaDa(categoria)}.")
                print("Sua senha não pode ser cadastrada. Por favor, cadastre outra senha.")
            else:
                obs: str = entrada("Alguma observação?: ")
                #criptografa a senha aqui

                #avisa se a senha ta sendo usada em outro canto
                usadas: str | None = risco.servicosComMesmaSenha(senha)
                if usadas:
                    print("Atenção! Essa senha já é usada em: " + ", ".join(usadas))
                crud.cadastrar(f"{servico};{user};{senha};{categoria};{obs}")
                auditoria.registrar("CADASTRO", servico)
        case 2:
            #talvez possa perguntar de qual categoria/usuario gostaria de ver as senhas
            #por enquanto vai ver todas
            crud.listar()
        case 3:
            crud.listar()
            linhas: list[str] = crud.lerLinhas()
            numero: int = lerNumero("Qual o número do registro que deseja editar?: ")
            if 1 <= numero <= len(linhas):
                antigo: str = linhas[numero - 1]
                servicoAntigo: str = antigo.split(";")[0]
                novo_servico: str = entrada("Serviço: ")
                novo_user: str = entrada("Usuário/E-mail: ")
                nova_categoria: str = escolherCategoria()
                nova_senha: str = entrada("Senha: ")
                nova_pontuacao: int = VerificadorDeSenha.verificar_forca_senha(senha)[0]
                VerificadorDeSenha.verificar_senha(senha)
                if not VerificadorDeSenha.atende_exigencia(pontuacao, categorias.exigenciaDa(categoria)):
                    print(f"A categoria {categoria} exige senha no mínimo {categorias.exigenciaDa(categoria)}.")
                    print("Erro: Tentou cadastrar uma senha fraca. Operação cancelada.")
                else:
                    nova_obs: str = entrada("Observação: ")
                    #criptografa a senha aqui
                    
                    #avisa se a senha ta sendo usada em outro canto
                    usadas = risco.servicosComMesmaSenha(senha)
                    if usadas:
                        print("Atenção! Essa senha já é usada em: " + ", ".join(usadas))

                    novo: str = f"{servico};{user};{senha};{categoria};{obs}"

                    crud.atualizar(antigo, novo)
                    auditoria.registrar("EDIÇÃO", servicoAntigo)
            else:
                print("Número inválido.")
        case 4:
            crud.listar()
            linhas_removiveis: list[str] = crud.lerLinhas()
            numero_removido: int = lerNumero("Qual o número do registro que deseja excluir?: ")
            if 1 <= numero <= len(linhas_removiveis):
                crud.excluir(linhas_removiveis[numero_removido - 1])
                auditoria.registrar("EXCLUSÃO", servico)
            else:
                print("Número inválido.")
        case 5:
            print("WIP")
        case 6:
            crud.ultimoCadastro()
        case 7:
            crud.listar()
            linhas = crud.lerLinhas()
            numero = lerNumero("Qual o número do registro que deseja revelar a senha?: ")
            if 1 <= numero <= len(linhas) and len(linhas[numero - 1].split(";")) == 6:
                celulas: list[str] = linhas[numero - 1].split(";")
                tentativa = input("Use a senha mestra para revelar: ")
                if cofre.senhaCorreta(tentativa):
                    print(f"Senha: {celulas[2]}")  ## a senha é o 3º campo do registro
                    auditoria.registrar("REVELOU SENHA", celulas[0])
                else:
                    print("Senha incorreta.")
                    auditoria.registrar("TENTATIVA NEGADA", celulas[0])
            else:
                print("Número inválido.")
        case 8:
            categorias.listar()
            if input("Deseja cadastrar uma categoria ou alterar uma exigência? (s/n): ").strip().lower() == "s":
                nome: str = entrada("Nome da categoria: ").strip().lower()
                categorias.cadastrar(nome, lerExigencia())
        case 9:
            print("Obrigado por usar nosso gerenciador de senhas!")
            break
        case 10:
            risco.avisarRepetidas()
        case 11:
            risco.relatorio()
        case 12:
            auditoria.listar()
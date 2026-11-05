import crud
import categorias
import VerificadorDeSenha

## Igual ao input, mas não aceita ";" (é o separador dos campos no arquivo)
def entrada(mensagem):
    texto = input(mensagem)
    while ";" in texto:
        print('O caractere ";" não é permitido. Tente de novo.')
        texto = input(mensagem)
    return texto

## Igual ao int(input()), mas não deixa o programa quebrar se o usuário digitar letras
def lerNumero(mensagem):
    texto = input(mensagem).strip()
    while not texto.isdigit(): ## isdigit() é True só se o texto tiver apenas algarismos
        print("Digite apenas números.")
        texto = input(mensagem).strip()
    return int(texto)

## Mostra as categorias e retorna o nome da escolhida
def escolherCategoria():
    linhas = categorias.listar()
    numero = lerNumero("Qual a categoria?: ")
    while not 1 <= numero <= len(linhas):
        print("Número inválido.")
        numero = lerNumero("Qual a categoria?: ")
    return linhas[numero - 1].split(";")[0]

def lerExigencia():
    exigencia = input("Exigência mínima de força da senha (fraca, média ou forte): ").strip().lower()
    while exigencia not in VerificadorDeSenha.NIVEIS:
        print("Digite fraca, média ou forte.")
        exigencia = input("Exigência mínima de força da senha (fraca, média ou forte): ").strip().lower()
    return exigencia

while True:
    print("----------------- GERENCIADOR DE SENHAS ----------------")
    print("Opções: ")
    print("[1] - Adicionar nova senha\n[2] - Visualizar senhas\n[3] - Editar informações\n[4] - Excluir senhas\n[5] - Assistente de IA\n[6] - Ver último cadastro\n[7] - Revelar uma senha\n[8] - Categorias\n[9] - Encerrar programa")
    escolha = lerNumero("\nO que deseja fazer?: ")
    match escolha:
        case 1:
            servico = entrada("Qual serviço que terá sua senha registrada?: ")
            user = entrada("Qual o seu nome de usuário ou e-mail?: ")
            categoria = escolherCategoria()
            senha = entrada("Cadastre aqui sua senha com os seguintes critérios: \n"
                        "         *Ao menos 8 digitos\n"
                        "         *Ao menos uma letra MAIÚSCULA\n"
                        "         *Ao menos um número\n"
                        "         *Ao menos um caractere especial(!@#$%¨&)\n"
                        "Escreva aqui: ")
            #antes de add a senha tem a verificaçao de segurança
            pontuacao = VerificadorDeSenha.verificar_forca_senha(senha)
            VerificadorDeSenha.verificar_senha(senha)
            if not VerificadorDeSenha.atende_exigencia(pontuacao, categorias.exigenciaDa(categoria)):
                print(f"A categoria {categoria} exige senha no mínimo {categorias.exigenciaDa(categoria)}.")
                print("Sua senha não pode ser cadastrada. Por favor, cadastre outra senha.")
            else:
                obs = entrada("Alguma observação?: ")
                #criptografa a senha aqui
                crud.cadastrar(f"{servico};{user};{senha};{categoria};{obs}")
        case 2:
            #talvez possa perguntar de qual categoria/usuario gostaria de ver as senhas
            #por enquanto vai ver todas
            crud.listar()
        case 3:
            crud.listar()
            linhas = crud.lerLinhas()
            numero = lerNumero("Qual o número do registro que deseja editar?: ")
            if 1 <= numero <= len(linhas):
                antigo = linhas[numero - 1]
                servico = entrada("Serviço: ")
                user = entrada("Usuário/E-mail: ")
                categoria = escolherCategoria()
                senha = entrada("Senha: ")
                pontuacao = VerificadorDeSenha.verificar_forca_senha(senha)
                VerificadorDeSenha.verificar_senha(senha)
                if not VerificadorDeSenha.atende_exigencia(pontuacao, categorias.exigenciaDa(categoria)):
                    print(f"A categoria {categoria} exige senha no mínimo {categorias.exigenciaDa(categoria)}.")
                    print("Erro: Tentou cadastrar uma senha fraca. Operação cancelada.")
                else:
                    obs = entrada("Observação: ")
                    #criptografa a senha aqui
                    novo = f"{servico};{user};{senha};{categoria};{obs}"
                    crud.atualizar(antigo, novo)
            else:
                print("Número inválido.")
        case 4:
            crud.listar()
            linhas = crud.lerLinhas()
            numero = lerNumero("Qual o número do registro que deseja excluir?: ")
            if 1 <= numero <= len(linhas):
                crud.excluir(linhas[numero - 1])
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
                print(f"Senha: {linhas[numero - 1].split(';')[2]}")  ## a senha é o 3º campo do registro
            else:
                print("Número inválido.")
        case 8:
            categorias.listar()
            if input("Deseja cadastrar uma categoria ou alterar uma exigência? (s/n): ").strip().lower() == "s":
                nome = entrada("Nome da categoria: ").strip().lower()
                categorias.cadastrar(nome, lerExigencia())
        case 9:
            print("Obrigado por usar nosso gerenciador de senhas!")
            break
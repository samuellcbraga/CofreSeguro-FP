import crud

while True:
    print("----------------- GERENCIADOR DE SENHAS ----------------")
    print("Opções: ")
    print("[1] - Adicionar nova senha\n[2] - Visualizar senhas\n[3] - Editar informações\n[4] - Excluir senhas\n[5] - Assistente de IA\n[6] - Encerrar programa")
    escolha = int(input("\nO que deseja fazer?: "))
    match escolha:
        case 1:
            servico = input("Qual serviço que terá sua senha registrada?: ")
            user = input("Qual o seu nome de usuário ou e-mail?: ")
            senha = input("Qual a sua senha?: ")
            obs = input("Alguma observação?: ")
            #antes de add a senha vai ter a verificaçao de segurança
            #isso é so um wip, ainda vai ser separado por categorias, criptografado, etc
            #será que é o caso de usar um dicionário?
            crud.cadastrar(f"Serviço: {servico}, Usuário/E-mail: {user}, Senha: {senha}, Observação: {obs}")
        case 2:
            #talvez possa perguntar de qual categoria/usuario gostaria de ver as senhas
            #por enquanto vai ver todas
            crud.listar()
        case 3:
            crud.listar()
            linhas = crud.lerLinhas()
            numero = int(input("Qual o número do registro que deseja editar?: "))
            if 1 <= numero <= len(linhas):
                antigo = linhas[numero - 1]
                servico = input("Serviço: ")
                user = input("Usuário/E-mail: ")
                senha = input("Senha: ")
                obs = input("Observação: ")
                novo = f"Serviço: {servico}, Usuário/E-mail: {user}, Senha: {senha}, Observação: {obs}"
                crud.atualizar(antigo, novo)
            else:
                print("Número inválido.")
        case 4:
            crud.listar()
            linhas = crud.lerLinhas()
            numero = int(input("Qual o número do registro que deseja excluir?: "))
            if 1 <= numero <= len(linhas):
                crud.excluir(linhas[numero - 1])
            else:
                print("Número inválido.")
        case 5:
            print("WIP")
        case 6:
            print("Obrigado por usar nosso gerenciador de senhas!")
            break

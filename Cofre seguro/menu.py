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
            obs = input("Alguma observação? (S/N): ")
            #antes de add a senha vai ter a verificaçao de segurança
            lista_senhas = open("Lista_senhas.txt", "a")
            lista_senhas.write(f"Serviço: {servico}, Usuário/E-mail: {user}, Senha: {senha}, Observação: {obs}, Hora da alteração: (hora)\n")
            #isso é so um wip, ainda vai ser separado por categorias, criptografado, etc
            #será que é o caso de usar um dicionário?
            lista_senhas.close()
        case 2:
            #talvez possa perguntar de qual categoria/usuario gostaria de ver as senhas
            #por enquanto vai ver todas
            with open("Lista_senhas.txt", "r", encoding="latin-1") as lista_senhas:
                ler_senhas = lista_senhas.read()
                print(ler_senhas)
            lista_senhas.close()
        case 3: 
            print("nao sei como faz isso")
        case 4:
            print("tambem nao sei como faz isso")
        case 5:
            print("WIP")
        case 6:
            print("Obrigado por usar nosso gerenciador de senhas!")
            break


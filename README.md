
# Cofre Seguro: Projeto CryptoCarol
* Projeto de Fundamentos de Programação
* Turma: CC1A - Cesar School
## Introdução:
O Projeto CryptoCarol é um banco de senhas escrito em Python com capacidade de criptografia de ponta utilizando criptografia em descanso AES-GCM e hashing argon2id (algoritmos de ponta usados pela indústria de cybersegurança) com salting e nonces randomizados a fim de dificultar acesso ao banco de senhas.

### Requisitos:
* Pip
- Bibliotecas padrão do Python:
    - cryptography
    - struct
- Biblioteca externa do Python
    - argon2-cffi
## Instalação:
Instale as bibliotecas necessárias:

    pip install cryptography struct argon2-cffi
Clone o repositório:

    git clone https://github.com/samuellcbraga/CofreSeguro-FP.git

Inicie o programa abrindo o diretório CofreSeguro-FP e inicie o arquivo menu.py:

    python3 menu.py

## Utilização Básica:
Ao iniciar o programa você se deparará com um menu:

    ----------------- GERENCIADOR DE SENHAS ----------------
    Opções:
    [1] - Adicionar nova senha
    [2] - Visualizar senhas
    [3] - Editar informações
    [4] - Excluir senhas
    [5] - Assistente de IA
    [6] - Ver último cadastro
    [7] - Revelar uma senha
    [8] - Categorias
    [9] - Encerrar programa
    [10] - Ver locais com mesma senha
    [11] - Ver senhas em risco
    [12] - Registro de auditoria
    
Para operar, basta digitar o número correspondente. O programa permite tanto criação quanto edição e deleção. Visualização requer a senha novamente para descriptografar o arquivo. Caso o arquivo já exista criptografado como um todo, também será necessário inseri-la para descriptografia do banco como um todo. Opções sensíveis ficam impossibilitadas devido criptografia.

# Arquitetura de Segurança
Conforme descrito na introdução, o programa utiliza algoritmos de alta segurança e entropia para maior dificuldade de acesso, aqui descreverei a fundo.
## Escolhas tomadas:

### Criptografia: AES-256-GCM
Desde o início, o programa como um todo foi pensado como um sistema de alta segurança. A base da criptografia é o AES (Advanced Encryption Standard), um algoritmo internacionalmente usado para criptografia de dados de altíssima segurança. Criptografia AES é feita a partir de uma chave em bytes em valores fixos, neste projeto usamos uma chave de 32 bytes para ter o algoritmo mais difícil de quebrar, AES-256 bits. Finalmente, utilizamos a variante GCM (Galois/Counter Mode) para verificação de integridade dos dados cifrados, se houver alteração de um bit sequer, será detectado. 

Resumidamente o AES utiliza de um algoritmo que deriva novas chaves a partir da primeira e realiza rodadas de operações com cada chave gerada, usando um vetor inicial randomizado para dificultar mais ainda a descriptografia. No caso de uma chave de 256-bits, temos 14 rodadas de operações matemáticas com múltiplos passos, alterando significativamente o resultado com qualquer mudança mínima de bits, seja da senha, dados, ou até mesmo o vetor inicial, tornando o banco diferente toda vez que reencriptado, mesmo usando a mesma senha e mesmos dados!

### Hashing: Argon2id
Com o algoritmo seguro definido, resta apenas um ponto fraco: a senha em si. Apesar de o banco em si poder guardar senhas com criptografia de ponta, nada muda se a senha necessária para abri-lo seja apenas uma simples "senha123", além de ela naturalmente não satisfazer o requisito de chave do AES-256-GCM de 32 bytes. A partir daí, utiliza-se o hashing: um algoritmo unidirecional que não permite recuperação da senha mesmo com o dado completo, por exemplo com SHA256, que retorna exatos 32 bytes de informação.

Apesar disso, o SHA256 tem vulnerabilidades conhecidas. Uma delas é a simples comparação de resultados do hash: um potencial invasor não precisa inverter o hash, apenas testar senhas até conseguir um hash idêntico. A fim de resolver isso em casos de senhas fracas, utiliza-se o *salt*, um conjunto aleatório adicionado no início ou fim da senha para trocar totalmente o resultado do hash... mas ainda há um problema: o SHA256 é extremamente rápido para gerar o hash, mas velocidade nesse caso não é um ponto positivo, pois permite múltiplas tentativas em fração de segundo com pouco gasto de recursos.

Então, finalmente, a escolha do sistema de hash usado: Argon2id. O Argon2id é um algoritmo de hashing com *salt* randomizado nativo, e com uso de memória, número de iterações, e paralelismo utilizado fixos, definidos no momento da criptografia. Isso significa que a quantidade de recursos necessários para uma tentativa pode ser definido de forma a aumentar o tempo necessário por tentativa, e essa funcionalidade permite aumentar MUITO a dificuldade de uma invasão por força bruta. 

### Lógica utilizada:
WIP
    

## Participantes:
- Artur de Carvalho Lyra (Arcaly)
- José Guilherme Burégio (santosdecartier)
- Júlia Melo (Marshmeelo)
- Marco (sem github)
- Marina Queiroga Cavendish (marinacavendish)
- Samuel Lins Braga (samuellcbraga)

## Nossa Organização:
Tarefas foram divididas conforme requisitos exigidos pela cadeira, com exceção de Funcionalidades extras. O código foi colocado no GitHub por todos (exceto Marco, que enviou via WhatsApp) a fim de manter o desenvolvimento estável. Apesar de alguns contratempos, os requisitos foram atendidos.

- Artur Lyra: 
  - Adicionou o módulo seguranca.py;
  - Responsável por organizar a criptografia e descriptografia do sistema como um todo;
  - Limpeza geral do código como um todo atendendo boas práticas (atomização de funções, notação de tipos, uso de docstrings, etc.);
  - Documentação do README.md (manual escolhido).
 
- José Guilherme Burégio: 
  - Adicionou o módulo VerificadorDeSenha.py e senhas_comuns.txt;
  - Responsável por organizar e estruturar o verificador de senha usado pelo programa;
  - Limpeza e condensação do verificador de força da senha.
  
 

 


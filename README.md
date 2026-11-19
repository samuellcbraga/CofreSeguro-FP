
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
    - groq (requisito)
## Instalação:
Instale as bibliotecas necessárias:

    python -m pip install cryptography struct argon2-cffi groq
Clone o repositório:

    git clone https://github.com/samuellcbraga/CofreSeguro-FP.git

Inicie o programa abrindo o diretório CofreSeguro-FP e inicie o arquivo menu.py:

    python3 menu.py
    cd CofreSeguro-FP
    python -m pip install cryptography argon2-cffi groq
    python menu.py

Para usar o assistente de IA (opção 5), copie o `.env.example` com o nome `.env` e coloque nele sua chave gratuita de https://console.groq.com. Nunca envie o `.env` ao GitHub. Senhas, usuários, observações e nomes dos serviços não são enviados ao modelo.


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
Considerando o método seguro de criptografia simétrica utilizado, pode-se dispensar a necessidade de salvar em arquivos adicionais as informações necessárias para descriptografia de qualquer bloco, seja apenas texto ou arquivo inteiro, permitindo especificidade na parte de pesos de memória utilizados. Com isto, pode-se aplicar o hashing da senha através do Argon2id que é resistente a ataques side-channel e de força bruta guardando o *salt* utilizado num *header* não criptografado, porém autenticado, do algoritmo AES-GCM. Desta forma se pode garantir que todos os dados do arquivo estão inalterados.

Para tirar proveito máximo do sistema de hashing e senhas do banco AES, a criptografia e descriptografia foram dadas dois conjuntos de variáveis constantes diferentes para os parâmetros do hash. Desta forma, é possível utilizar um processo mais intensivo no gasto de recursos para fortalecer o arquivo de senhas (caso ele seja copiado por alguém malicioso ou comprometido de alguma forma), enquanto não trazendo o impacto de tempo para toda operação dentro do gerenciador de senhas. Fazendo assim, o banco demora mais por tentativa, impedindo ataques de força bruta em quantidade, mas só precisa realizar as operações mais longas duas vezes ao total, uma ao abrir o programa e outra ao fechar. Simultaneamente, as operações repetitivas internas ao gerenciador, usam uma criptografia rápida e suficientemente segura, ainda mais sabendo que não será legível sem acesso direto à memória do programa após destravamento da primeira camada robusta.

Para permitir funcionamento de mostragem de parte da senha (requisito), foi adicionado ao header 2 caracteres correspondentes ao final da senha, apendidos a uma linha de '*' de quantidade padronizada, evitando divulgar não-intencionalmente o comprimento das senhas do banco. O mesmo sistema de criptografia é replicado nos arquivos de auditoria, evitando novamente que acessos indesejados ocorram. Além de tudo isso, caso um método de força bruta apareça no futuro próximo, a dupla camada de criptografia com GCM permite que uma extração forçada não confirme legibilidade do arquivo, pois o erro levantado ao tentar descriptografar é o mesmo em caso de senha incorreta e bloco criptografado adulterado. 

Da forma que foi feito o sistema de banco de senhas, nenhum acesso indesejado pode ocorrer sem ser explicitamente feito dentro do programa, que em caso de um executável binário ainda ofuscaria o funcionamento do código. Ademais, a senha do banco em si não é escrita a disco em momento algum, impedindo extração sem entrada correta que é apenas armazenada como variável (na RAM da máquina, não no armazenamento de disco). Com isto, temos o efeito adicional de impedir leitura por meio da IA integrada (requisito) sem explicitamente programar uma passagem dos dados para ela. Com isso, não existe possibilidade de vazamento para a IA. 
    
### Soluções de segurança aplicadas pela Lógica:
- Ataques de força bruta à senha do dado criptografado por usar hash;
- Ataques de força bruta para descobrir hash usado com chave de criptografia;
- Ataques de side-channel durante hashing devido à natureza do Argon2id;
- Tentativa e erro de manipulação aos dados ou de senhas levantam mesmo erro (dificulta engenharia reversa);
- Extração de senha do disco é impossível pois a mesma só é inserida em variável (memória temporária);
- Acesso a dados supérfluos é impedido por criptografia dupla (arquivo e dados internos).

### Falhas não mitigadas pela lógica (e porque podem ser amenas):
- **Alteração do código do programa para salvar a senha:** é amena pois acesso direto ao código fonte implica comprometimento da máquina como um todo;
- **Keyloggers:** Assim como o ponto acima, implica que a máquina inteira está comprometida, não sendo falha por parte do programa;
- **Exploit de memória para extração das variáveis do programa:** Requer controle granular dos blocos de memória e acesso de escrita na máquina, de forma que dificilmente ocorreria, mas não é mitigável no presente;
- **Leitura da senha:** Extremamente improvável e requer proximidade à máquina e leitura através da digitação do teclado, pois campos de senha são ofuscados;
- **Esquecimento da senha mestra:** Consequência direta do grau de segurança escolhido. Para impedir novos vetores de ataque, a senha é o único meio de entrada considerado viável, perdê-la implica perda do banco de senhas inteiro;
- **Senha fraca:** Apesar do hash utilizado ser lento com finalidade explícita de redução de viabilidade de tentativa e erro, uma senha comum pode implicar poucas tentativas. Isso é reduzido com uma senha forte, conforme recomendado pelo próprio banco de senhas, juntamente com a repetição constante da senha mestra para acessar o banco em si tornando difícil de se esquecer, além de se tornar necessário memorizar apenas uma senha, deixando o banco cuidar do restante ser uma economia de recursos mentais significativo.

### Conclusão do Sistema de Segurança:
Apesar de não ser perfeito, nenhum sistema de segurança existente pode ser considerado perfeito. O esforço maior foi para tornar o mais improvável possível que houvesse uma invasão de terceiros, de forma que o único meio de acessar os arquivos seria comprometendo a máquina como um todo. Caso queira mitigar invasões de dispositivo, coloque suas senhas anotadas num papel dentro de um cofre cimentado no chão, atualizando manualmente toda vez que necessário. Caso prefira uma camada maior de conveniência, o Cofre CryptoCarol pode ser um bom começo para você.


## Participantes:
- Artur de Carvalho Lyra (Arcaly)
- José Guilherme Burégio (santosdecartier)
- Júlia de Melo (Marsheemelo)
- Marco (Marconet18)
- Marina Queiroga Cavendish (marinacavendish)
- Samuel Lins Braga (samuellcbraga)

## Nossa Organização:
Tarefas foram divididas conforme requisitos exigidos pela cadeira, com exceção de Funcionalidades extras. O código foi colocado no GitHub por todos (exceto Marco, que enviou via WhatsApp) a fim de manter o desenvolvimento estável. Apesar de alguns contratempos, os requisitos foram atendidos.

- Artur Lyra: 
  - Adicionou o módulo seguranca.py;
  - Pesquisa e arquitetura da segurança de arquivos do código;
  - Responsável por organizar as funções de criptografia e descriptografia do sistema como um todo;
  - Limpeza geral do código como um todo atendendo boas práticas (atomização de funções, notação de tipos, uso de docstrings, etc.);
  - Documentação do README.md (manual escolhido).
 
- José Guilherme Burégio: 
  - Adicionou o módulo VerificadorDeSenha.py e senhas_comuns.txt;
  - Responsável por organizar e estruturar o verificador de senha usado pelo programa;
  - Limpeza e condensação do verificador de força da senha.

- Júlia de Melo Lopes:
  - Adicionou o módulo menu.py;
  - Esqueletou entrada de todas as funções que faziam parte do menu;
  - Implementação do código de outros módulos no menu;
  - Correção de bugs vindos de outros módulos;
  - Complementação de Docstrings para documentação das funções.

- Marina Cavendish:
  - Implementou a detecção de risco (risco.py): alerta de senhas repetidas entre serviços, aviso ao cadastrar uma senha já usada e relatório de segurança (total de credenciais, fracas, comuns, repetidas e dias desde a última alteração);
  - Implementou o registro de auditoria (auditoria.py): log de cadastro, edição, exclusão e revelação de senha (operação, serviço, data e hora), consultável pelo menu;
  - Integrou a senha mestra e o cofre criptografado (cofre.py) ao fluxo de entrada do programa, com limite de tentativas;
  - Integrou os módulos criados no menu principal e corrigiu erros encontrados durante a integração.

- Samuel Lins Cavalcanti Braga:
  - Criou o crud.py e o integrou ao menu;
  - Adicionou as categorias, a data de cadastro e a senha mascarada na listagem;
  - Integrou o agente de IA da aula ao menu (opção 5);
  - Ajudou na correção de bugs e na organização do repositório.
 
- Marco Antonio Pinto Paes Fortes Neto:

 - Contribuição na lógica,esqueletização e na criação do módulo VerificadorDeSenha.py
- Ajudou na correçào de bugs e na organização do repositório 

 

 


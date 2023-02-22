# Trabalho de banco de dados
# Alunos: Eduardo Chiarello
#         Éric

import sqlite3
import os

if os.path.isfile('pizzaria.db'):
    tabela_ja_criada_anteriormente = True
    print('O banco de dados já existe')
else:
    print('O banco de dados não existe')
    tabela_ja_criada_anteriormente = False

# conectando ao banco de dados
conn = sqlite3.connect('pizzaria.db')

# cria as tabelas se elas não existirem
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS enderecos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        rua TEXT,
        numero INTEGER,
        bairro TEXT,
        cidade TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sabores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        sabor_especial TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tamanhos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        fatias INTEGER,
        preco REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bordas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bebidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        preco REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        sabor_id INTEGER,
        tamanho_id INTEGER,
        bebida_id INTEGER,
        borda_id INTEGER,
        preco_total REAL,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(sabor_id) REFERENCES sabores(id),
        FOREIGN KEY(tamanho_id) REFERENCES tamanhos(id),
        FOREIGN KEY(bebida_id) REFERENCES bebidas(id)
    )
""")

if tabela_ja_criada_anteriormente == False:

    # insere algumas bordas
    cursor.execute("INSERT INTO bordas (nome, preco) VALUES (?, ?)", ('Nenhuma', 0))
    cursor.execute("INSERT INTO bordas (nome, preco) VALUES (?, ?)", ('Chocolate', 10))
    cursor.execute("INSERT INTO bordas (nome, preco) VALUES (?, ?)", ('Queijo', 5))

    # insere alguns tamanhos de pizza
    cursor.execute("INSERT INTO tamanhos (nome, fatias, preco) VALUES (?, ?, ?)", ('Pequeno', 6, 24.99))
    cursor.execute("INSERT INTO tamanhos (nome, fatias, preco) VALUES (?, ?, ?)", ('Médio', 10, 32.50))
    cursor.execute("INSERT INTO tamanhos (nome, fatias, preco) VALUES (?, ?, ?)", ('Grande', 14, 39.99))

    # insere alguns sabores de pizza
    cursor.execute("INSERT INTO sabores (nome, descricao, sabor_especial) VALUES (?, ?, ?)",
                   ('Nenhuma', 'Nada', 'nao'))
    cursor.execute("INSERT INTO sabores (nome, descricao, sabor_especial) VALUES (?, ?, ?)",
                   ('Mussarela', 'Molho de tomate, mussarela e orégano', 'nao'))
    cursor.execute("INSERT INTO sabores (nome, descricao, sabor_especial) VALUES (?, ?, ?)",
                   ('Calabresa', 'Molho de tomate, mussarela, calabresa, cebola e orégano', 'nao'))
    cursor.execute("INSERT INTO sabores (nome, descricao, sabor_especial) VALUES (?, ?, ?)",
                   ('Margherita', 'Molho de tomate, mussarela de búfala, tomate e manjericão', 'nao'))
    cursor.execute("INSERT INTO sabores (nome, descricao, sabor_especial) VALUES (?, ?, ?)",
                   ('Portuguesa', 'Molho de tomate, mussarela, presunto, ovo, cebola, azeitona e orégano', 'sim'))
    cursor.execute("INSERT INTO sabores (nome, descricao, sabor_especial) VALUES (?, ?, ?)",
                   ('Chocolate com morango', 'Pizza doce de chocolate com morango', 'sim'))

    # insere algumas bebidas
    cursor.execute("INSERT INTO bebidas (nome, descricao, preco) VALUES (?, ?, ?)", ('Nenhuma', 'Nada', 0.00))
    cursor.execute("INSERT INTO bebidas (nome, descricao, preco) VALUES (?, ?, ?)", ('Coca-cola', 'Lata 350ml', 4.00))
    cursor.execute("INSERT INTO bebidas (nome, descricao, preco) VALUES (?, ?, ?)", ('Guaraná', 'Lata 350ml', 3.50))
    cursor.execute("INSERT INTO bebidas (nome, descricao, preco) VALUES (?, ?, ?)",
                   ('Suco de laranja', 'Copo 300ml', 5.00))

# solicita ao usuário a ação a ser realizada
acao = input("Digite 1 para cadastrar novo cliente ou 2 para fazer um pedido: ")

valor_pizza_especial = 10.00

if acao == "1":
    # solicita os dados do novo cliente
    nome = input("Digite o nome do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    rua = input("Digite a rua do endereço do cliente: ")
    numero = input("Digite o número do endereço do cliente: ")
    bairro = input("Digite o bairro do endereço do cliente: ")
    cidade = input("Digite a cidade do endereço do cliente: ")

    # insere o novo cliente
    cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)", (nome, telefone))

    # recupera o id do novo cliente
    cliente_id = cursor.lastrowid

    try:
        # insere o endereço do cliente
        cursor.execute("INSERT INTO enderecos (cliente_id, rua, numero, bairro, cidade) VALUES (?, ?, ?, ?, ?)",
                       (cliente_id, rua, numero, bairro, cidade))

        # salva as alterações no banco de dados
        conn.commit()

        print("Cliente cadastrado com sucesso!")

    except:
        print("Erro ao cadastrar novo cliente!")

elif acao == "2":
    # Exibe os sabores disponíveis
    print("Sabores disponíveis:")
    for sabor in cursor.execute("SELECT * FROM sabores"):
        print(f"{sabor[0]} - {sabor[1]} - {sabor[2]} - {sabor[3]}")

    # Pede ao usuário para selecionar um sabor
    id_sabor = int(input("Digite o ID do sabor que deseja pedir: "))

    # Exibe os tamanhos disponíveis
    print("Tamanhos disponíveis:")
    for tamanho_tal in cursor.execute("SELECT * FROM tamanhos"):
        print(f"{tamanho_tal[0]} - {tamanho_tal[1]} - {tamanho_tal[2]} - {tamanho_tal[3]}")

    # Pede ao usuário para selecionar uma bebida
    id_tamanho = input("Digite ID do tamanho: ")

    # Exibe as bordas disponíveis
    print("Bordas disponíveis:")
    for borda_tal in cursor.execute("SELECT * FROM bordas"):
        print(f"{borda_tal[0]} - {borda_tal[1]} - {borda_tal[2]}")

    # Pede ao usuário para selecionar um sabor
    id_borda = int(input("Digite o ID da borda que deseja pedir: "))

    # Exibe as bebidas disponíveis
    print("Bebidas disponíveis:")
    for bebida_tal in cursor.execute("SELECT * FROM bebidas"):
        print(f"{bebida_tal[0]} - {bebida_tal[1]} - {bebida_tal[2]} - {bebida_tal[3]}")

    id_bebida = input("Digite a bebida desejada: ")

    # Verifica se o sabor escolhido está disponível
    sabor_disponivel = False
    for sabor in cursor.execute("SELECT * FROM sabores WHERE id=?", (id_sabor,)):
        sabor_disponivel = True
        descricao = sabor[2]

    if not sabor_disponivel:
        print("Sabor indisponível. Por favor, escolha outro.")

    # Obtém o endereço do cliente
    id_cliente = int(input("Digite o ID do cliente que está fazendo o pedido: "))
    id_endereco = int(input("Digite o ID do endereço: "))

    # Calculando o valor total:
    cursor.execute("SELECT preco FROM tamanhos WHERE id=?", (id_tamanho,))
    valor_final = float(cursor.fetchone()[0])
    cursor.execute("SELECT preco FROM bebidas WHERE id=?", (id_bebida,))
    valor_final = valor_final + float(cursor.fetchone()[0])
    cursor.execute("SELECT preco FROM bordas WHERE id=?", (id_borda,))
    valor_final = valor_final + float(cursor.fetchone()[0])
    cursor.execute("SELECT sabor_especial FROM sabores WHERE id=?", (id_sabor,))
    if cursor.fetchone()[0] == 'sim':
        valor_final = valor_final + valor_pizza_especial

    print("Valor total a pagar: ", valor_final)

    try:
        # Insere o novo pedido na tabela "pedidos"
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, sabor_id, tamanho_id, bebida_id, borda_id, preco_total) VALUES (?, ?, ?, ?, ?, ?)",
            (id_cliente, id_sabor, id_tamanho, id_bebida, id_borda, valor_final))
        conn.commit()
        print("Pedido cadastrado com sucesso!")

    except:
        print("Erro ao cadastrar pedido!")

else:
    print("Opção inválida. Por favor, tente novamente.")

# salva as alterações no banco de dados
conn.commit()

# fecha a conexão com o banco de dados
conn.close()

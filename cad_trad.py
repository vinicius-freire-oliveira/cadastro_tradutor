import pyodbc

def criar_tabela():
    # Conecta-se ao banco de dados
    conexao = pyodbc.connect('Driver={SQL Server};'
                             'Server=DESKTOP-3ELVTO1;'
                             'Database=tradutor_ingles;'
                             'Trusted_Connection=yes;')

    # Cria o cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Verifica se a tabela já existe
    cursor.execute("IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'palavras') "
                   "BEGIN "
                   "CREATE TABLE palavras ("
                   "id INT IDENTITY(1,1) PRIMARY KEY, "
                   "palavra NVARCHAR(255) UNIQUE, "
                   "traducao NVARCHAR(255))"
                   "END")

    # Confirma as alterações
    conexao.commit()

    # Fecha a conexão
    conexao.close()

def cadastrar_palavra(palavra, traducao):
    # Conecta-se ao banco de dados
    conexao = pyodbc.connect('Driver={SQL Server};'
                             'Server=DESKTOP-3ELVTO1;'
                             'Database=tradutor_ingles;'
                             'Trusted_Connection=yes;')

    cursor = conexao.cursor()

    try:
        # Insere a palavra e sua tradução na tabela
        cursor.execute("INSERT INTO palavras (palavra, traducao) VALUES (?, ?)", (palavra, traducao))
        conexao.commit()
        print("Palavra cadastrada com sucesso!")
    except pyodbc.IntegrityError:
        print("A palavra já existe no dicionário.")

    # Fecha a conexão
    conexao.close()

def pesquisar_palavra(palavra):
    # Conecta-se ao banco de dados
    conexao = pyodbc.connect('Driver={SQL Server};'
                             'Server=DESKTOP-3ELVTO1;'
                             'Database=tradutor_ingles;'
                             'Trusted_Connection=yes;')

    cursor = conexao.cursor()

    # Busca a tradução da palavra no banco de dados
    cursor.execute("SELECT traducao FROM palavras WHERE palavra = ?", (palavra,))
    resultado = cursor.fetchone()

    # Fecha a conexão
    conexao.close()

    if resultado:
        return resultado[0]
    else:
        return None

# Cria a tabela se ela não existir
criar_tabela()

# Exemplo de cadastro de palavras
cadastrar_palavra("swear", "jurar")
cadastrar_palavra("dog", "cachorro")
cadastrar_palavra("cat", "gato")

# Exemplo de pesquisa de palavra
palavra_desejada = input("Digite a palavra em inglês que deseja pesquisar: ")
traducao = pesquisar_palavra(palavra_desejada)
if traducao:
    print(f"A tradução de '{palavra_desejada}' é '{traducao}'.")
else:
    print(f"A palavra '{palavra_desejada}' não foi encontrada no dicionário.")


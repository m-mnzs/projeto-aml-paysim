import sqlite3
import pandas as pd 

# 1. Caminho para o arquivo CSV baixado e nome do banco
CSV_file = 'PS_20174392719_1491204439457_log.csv'
DB_FILE = 'paysim_banco.db'

print("Iniciando a conexão com o banco de dados SQLite...")
# sqlite3.connect cria o arquivo de banco de dados se ele ainda não existir 
conn = sqlite3.connect(DB_FILE)

print("Carregando os dados do CSV para o banco em lotes...")

# 2. Ler em pedaços (chunksize) para não estourar a memória RAM
chunk_size = 100000 # processa 100 mil linhas por vez
total_linhas = 0

for i, chunk in enumerate(pd.read_csv(CSV_file, chunksize=chunk_size)):
    # chunk.to_sql pega o dataframe do Pandas e grava como tabela no SQLite
    # if_exists='append' faz com que cada bloco seja adicionado na mesma tabela
    chunk.to_sql('transacoes', conn, if_exists='append', index=False)
    total_linhas += len(chunk)
    print(f"Bloco {i+1} processado. Total de linhas salvas: {total_linhas}")

# 3. Criar índices em SQL para acelerar as buscas investigativas 
print("Criando índices de busca em SQl...")
cursor = conn.cursor()
cursor.execute("CREATE INDEX IF NOT EXISTS idx_nameOrig ON transacoes(nameOrig);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_nameDest ON transacoes(nameDest);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON transacoes(type);")

conn.commit()
conn.close()

print("Banco SQLite criado e populado com sucesso!")
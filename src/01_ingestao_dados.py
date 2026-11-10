"""
Módulo de Ingestão de Dados (PaySim).
Responsável por processar o arquivo CSV bruto em lotes (chunks) e popular o banco SQLite,
criando índices relacionais para otimização de consultas investigativas.
"""

import os
import sqlite3
import pandas as pd

# Define dinamicamente o diretório raiz do projeto (um nível acima de 'src/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Caminhos para os arquivos 
CSV_FILE = os.path.join(BASE_DIR, 'data', 'PS_20174392719_1491204439457_log.csv')
DB_FILE = os.path.join(BASE_DIR, 'data', 'paysim_banco.db')


def executar_ingestao() -> None:
    """Executa o pipeline de ingestão do CSV para o banco SQLite."""
    
    # Validação defensiva: verifica se o arquivo CSV realmente existe na pasta data/
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado em: {CSV_FILE}\n"
            "Certifique-se de colocar o dataset PaySim na pasta 'data/'."
        )

    print("Iniciando a conexão com o banco de dados SQLite.")
    conn = sqlite3.connect(DB_FILE)

    print("Carregando os dados do CSV para o banco em lotes (chunks).")
    
    # Lê em pedaços para gerenciar eficientemente o uso de RAM
    chunk_size = 100000  # 100 mil linhas por vez
    total_linhas = 0

    try:
        for i, chunk in enumerate(pd.read_csv(CSV_FILE, chunksize=chunk_size)):
            chunk.to_sql('transacoes', conn, if_exists='append', index=False)
            total_linhas += len(chunk)
            print(f"Bloco {i+1} processado. Total de linhas salvas: {total_linhas}")
            
    except Exception as erro:
        print(f"[ERRO] Falha durante a leitura/carga do CSV: {erro}")
        conn.close()
        raise

    # 3. Criar índices em SQL para acelerar as buscas investigativas (Essencial para Grafos/SQL)
    print("Criando índices de busca em SQL.")
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_nameOrig ON transacoes(nameOrig);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_nameDest ON transacoes(nameDest);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON transacoes(type);")

    conn.commit()
    conn.close()

    print("Banco SQLite criado e populado com sucesso na pasta data/!")


if __name__ == "__main__":
    executar_ingestao()
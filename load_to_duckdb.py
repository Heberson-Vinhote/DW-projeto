import duckdb
import os

def main():
    print("Conectando ao banco de dados DuckDB (ecommerce.db)...")
    con = duckdb.connect(database='ecommerce.db')

    # Cria o schema bruto (onde caem os dados da fonte)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    print("Carregando Cliente Bruto...")
    con.execute('''
        CREATE OR REPLACE TABLE raw.raw_cliente AS
        SELECT * FROM read_csv_auto('data/raw_cliente.csv');
    ''')

    print("Carregando Produto Bruto...")
    con.execute('''
        CREATE OR REPLACE TABLE raw.raw_produto AS
        SELECT * FROM read_csv_auto('data/raw_produto.csv');
    ''')

    print("Carregando Loja Bruto...")
    con.execute('''
        CREATE OR REPLACE TABLE raw.raw_loja AS
        SELECT * FROM read_csv_auto('data/raw_loja.csv');
    ''')

    print("Carregando Tempo Bruto...")
    con.execute('''
        CREATE OR REPLACE TABLE raw.raw_tempo AS
        SELECT * FROM read_csv_auto('data/raw_tempo.csv');
    ''')

    print("Carregando Vendas Brutas...")
    con.execute('''
        CREATE OR REPLACE TABLE raw.raw_vendas AS
        SELECT * FROM read_csv_auto('data/raw_vendas.csv');
    ''')

    print("\nValidando a carga dos dados (contagem de registros no schema raw):")
    tables = ['raw_cliente', 'raw_produto', 'raw_loja', 'raw_tempo', 'raw_vendas']
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        print(f" - raw.{table}: {count} registros")

    con.close()
    print("Carga concluída com sucesso e conexão fechada.")

if __name__ == "__main__":
    main()

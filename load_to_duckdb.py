import duckdb
import os

def main():
    print("Conectando ao banco de dados DuckDB (ecommerce.db)...")
    con = duckdb.connect(database='ecommerce.db')

    print("Carregando Dimensão Cliente...")
    con.execute('''
        CREATE TABLE IF NOT EXISTS dim_cliente AS
        SELECT * FROM read_csv_auto('data/dim_cliente.csv');
    ''')

    print("Carregando Dimensão Produto...")
    con.execute('''
        CREATE TABLE IF NOT EXISTS dim_produto AS
        SELECT * FROM read_csv_auto('data/dim_produto.csv');
    ''')

    print("Carregando Dimensão Loja...")
    con.execute('''
        CREATE TABLE IF NOT EXISTS dim_loja AS
        SELECT * FROM read_csv_auto('data/dim_loja.csv');
    ''')

    print("Carregando Dimensão Tempo...")
    con.execute('''
        CREATE TABLE IF NOT EXISTS dim_tempo AS
        SELECT * FROM read_csv_auto('data/dim_tempo.csv');
    ''')

    print("Carregando Fato Vendas...")
    con.execute('''
        CREATE TABLE IF NOT EXISTS fato_vendas AS
        SELECT * FROM read_csv_auto('data/fato_vendas.csv');
    ''')

    print("\nValidando a carga dos dados (contagem de registros):")
    tables = ['dim_cliente', 'dim_produto', 'dim_loja', 'dim_tempo', 'fato_vendas']
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f" - {table}: {count} registros")

    con.close()
    print("Carga concluída com sucesso e conexão fechada.")

if __name__ == "__main__":
    main()

import duckdb
import os

def main():
    print("Conectando ao DuckDB para exportação...")

    # Cria pasta caso não exista
    output_dir = 'powerbi_data'
    os.makedirs(output_dir, exist_ok=True)

    # Conecta ao banco de dados em modo leitura
    con = duckdb.connect('ecommerce.db', read_only=True)

    # Lista de tabelas geradas pelo dbt no schema main
    tables = [
        'dim_cliente',
        'dim_produto',
        'dim_loja',
        'dim_tempo',
        'fato_vendas'
    ]

    for table in tables:
        output_file = f"{output_dir}/{table}.csv"
        print(f"Exportando {table} para {output_file}...")

        # O DuckDB possui uma função nativa maravilhosa para exportar para CSV
        query = f"COPY main.{table} TO '{output_file}' (HEADER, DELIMITER ',');"
        try:
            con.execute(query)
        except Exception as e:
            print(f"[ERRO] Não foi possível exportar a tabela {table}: {e}")

    con.close()
    print("Exportação concluída com sucesso! Os arquivos estão na pasta 'powerbi_data/'.")

if __name__ == "__main__":
    main()

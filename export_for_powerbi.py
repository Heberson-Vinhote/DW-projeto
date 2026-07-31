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

    absolute_paths = []

    for table in tables:
        output_file = f"{output_dir}/{table}.parquet"
        print(f"Exportando {table} para {output_file}...")

        try:
            con.execute(f"COPY main.{table} TO '{output_file}' (FORMAT PARQUET);")
            absolute_paths.append(os.path.abspath(output_file))
        except Exception as e:
            print(f"[ERRO] Não foi possível exportar a tabela {table}: {e}")

    con.close()

    print("\n==================================================")
    print("Exportação concluída com sucesso!")
    print("Os arquivos Parquet estão na pasta 'powerbi_data/'.")
    print("==================================================")
    print("No Power BI, cole os caminhos abaixo no campo 'URL':")
    for path in absolute_paths:
        print(f" -> {path}")
    print("==================================================\n")

if __name__ == "__main__":
    main()

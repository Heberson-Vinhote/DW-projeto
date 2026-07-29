import duckdb

def main():
    print("Conectando ao banco de dados DuckDB (ecommerce.db)...")
    con = duckdb.connect(database='ecommerce.db')

    with open('analytics_queries.sql', 'r') as file:
        sql_content = file.read()

    # Dividir as queries pelos comentários
    queries = sql_content.split('--')

    # Ignorar o primeiro elemento (vazio)
    for q in queries[1:]:
        if not q.strip():
            continue

        # Extrair título e a query
        lines = q.strip().split('\n')
        title = lines[0]
        query = '\n'.join(lines[1:]).strip()

        if query:
            print(f"\n{'-'*50}")
            print(f"Executando Análise: {title}")
            print(f"{'-'*50}")
            try:
                result = con.execute(query).fetchdf()
                print(result)
            except Exception as e:
                print(f"Erro ao executar query: {e}")

    con.close()

if __name__ == "__main__":
    main()

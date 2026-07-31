import subprocess
import sys

def run_script(script_name):
    print(f"\n{'='*50}")
    print(f"Executando Tarefa: {script_name}")
    print(f"{'='*50}")

    try:
        result = subprocess.run([sys.executable, script_name], check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"[SUCESSO] {script_name} executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao executar {script_name}.")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

def run_dbt_command(command):
    print(f"\n{'='*50}")
    print(f"Executando dbt: {command}")
    print(f"{'='*50}")

    try:
        # cwd garante que o comando rode dentro da pasta do projeto dbt
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True, cwd='ecommerce_dbt')
        print(result.stdout)
        print(f"[SUCESSO] Comando '{command}' executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao executar dbt: {command}.")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

def main():
    print("Iniciando o Pipeline de Dados (Data Warehouse) com dbt")

    # 1. Extração e Geração (Extract)
    run_script('generate_data.py')

    # 2. Carga Bruta (Load)
    run_script('load_to_duckdb.py')

    # 3. Transformação (Transform com dbt)
    run_dbt_command('dbt run')

    # 4. Testes de Qualidade (dbt test)
    run_dbt_command('dbt test')

    # 5. Análise (Analytics)
    run_script('run_queries.py')

    # 6. Preparação para o Power BI
    run_script('export_for_powerbi.py')

    print("\n" + "="*50)
    print("🚀 Pipeline E-L-T completo executado com sucesso!")
    print("="*50)

if __name__ == "__main__":
    main()

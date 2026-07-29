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

def main():
    print("Iniciando o Pipeline de Dados (Data Warehouse)")

    # 1. Extração e Geração (ETL)
    run_script('generate_data.py')

    # 2. Carga (Load)
    run_script('load_to_duckdb.py')

    # 3. Análise (Analytics)
    run_script('run_queries.py')

    print("\n" + "="*50)
    print("🚀 Pipeline completo executado com sucesso!")
    print("="*50)

if __name__ == "__main__":
    main()

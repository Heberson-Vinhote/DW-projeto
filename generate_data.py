import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

def generate_dim_cliente(num_records):
    data = []
    for i in range(1, num_records + 1):
        data.append({
            'id_cliente': i,
            'nome': fake.name(),
            'email': fake.email(),
            'cidade': fake.city(),
            'estado': fake.state_abbr(),
            'inadimplente': random.choices([True, False], weights=[0.25, 0.75])[0]
        })
    return pd.DataFrame(data)

def generate_dim_produto():
    # Produtos predefinidos
    categorias = {
        'Eletrônicos': ['Smartphone', 'Notebook', 'Tablet', 'Smartwatch', 'Fone de Ouvido'],
        'Eletrodomésticos': ['Geladeira', 'Micro-ondas', 'Máquina de Lavar', 'Fogão', 'Aspirador'],
        'Vestuário': ['Camiseta', 'Calça Jeans', 'Tênis', 'Jaqueta', 'Vestido'],
        'Casa': ['Sofá', 'Mesa', 'Cadeira', 'Cama', 'Guarda-roupa']
    }

    data = []
    id_prod = 1
    for categoria, produtos in categorias.items():
        for prod in produtos:
            preco_base = random.uniform(50.0, 3000.0)
            data.append({
                'id_produto': id_prod,
                'nome_produto': prod,
                'categoria': categoria,
                'preco': round(preco_base, 2)
            })
            id_prod += 1

    return pd.DataFrame(data)

def generate_dim_loja(num_records):
    data = []
    for i in range(1, num_records + 1):
        data.append({
            'id_loja': i,
            'nome_loja': f'Filial {fake.city()}',
            'cidade': fake.city(),
            'estado': fake.state_abbr()
        })
    return pd.DataFrame(data)

def generate_fato_vendas(num_records, dim_cliente, dim_produto, dim_loja):
    data = []
    start_date = datetime(2022, 1, 1)

    for i in range(1, num_records + 1):
        cliente = dim_cliente.sample(1).iloc[0]
        produto = dim_produto.sample(1).iloc[0]
        loja = dim_loja.sample(1).iloc[0]

        # Gerar uma data aleatória nos últimos 2 anos
        random_days = random.randint(0, 730)
        data_venda = start_date + timedelta(days=random_days)

        quantidade = random.randint(1, 5)
        valor_unitario = produto['preco']
        data.append({
            'id_venda': i,
            'id_cliente': cliente['id_cliente'],
            'id_produto': produto['id_produto'],
            'id_loja': loja['id_loja'],
            'data_venda': data_venda.strftime('%Y-%m-%d'),
            'quantidade': quantidade,
            'valor_unitario': valor_unitario
        })

    return pd.DataFrame(data)

def generate_dim_tempo(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    data = []
    current_date = start_date
    while current_date <= end_date:
        data.append({
            'data': current_date.strftime('%Y-%m-%d'),
            'dia': current_date.day,
            'mes': current_date.month,
            'ano': current_date.year,
            'trimestre': (current_date.month - 1) // 3 + 1,
            'dia_da_semana': current_date.weekday() + 1 # 1 = Segunda, 7 = Domingo
        })
        current_date += timedelta(days=1)

    return pd.DataFrame(data)

def main():
    print("Iniciando a geração de dados...")

    os.makedirs('data', exist_ok=True)

    df_cliente = generate_dim_cliente(500)
    df_produto = generate_dim_produto()
    df_loja = generate_dim_loja(10)
    df_tempo = generate_dim_tempo('2022-01-01', '2024-12-31')

    df_vendas = generate_fato_vendas(2000, df_cliente, df_produto, df_loja)

    print("Salvando dados na pasta 'data/'...")
    df_cliente.to_csv('data/raw_cliente.csv', index=False)
    df_produto.to_csv('data/raw_produto.csv', index=False)
    df_loja.to_csv('data/raw_loja.csv', index=False)
    df_tempo.to_csv('data/raw_tempo.csv', index=False)
    df_vendas.to_csv('data/raw_vendas.csv', index=False)

    print("Geração concluída com sucesso!")

if __name__ == "__main__":
    main()

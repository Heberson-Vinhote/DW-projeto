# Projeto de Data Warehouse - E-commerce

Este é um projeto de Data Warehouse construído do zero, idealizado para compor um portfólio de Engenharia de Dados. O objetivo do projeto é demonstrar a modelagem de um banco de dados analítico (Data Warehouse) utilizando a abordagem de **Star Schema (Esquema Estrela)**, geração de dados fictícios para simular um ambiente real, carga de dados em um banco analítico e consultas SQL para análise de negócio.

## 🏗 Arquitetura do Projeto
O pipeline de dados foi desenhado da seguinte maneira:
1. **Geração de Dados (ETL/ELT)**: Scripts em **Python** utilizando `pandas` e `Faker` para gerar dados transacionais (vendas, clientes, produtos e lojas) em formato CSV.
2. **Armazenamento e Processamento**: **DuckDB**, um SGBD analítico (OLAP) embutido que roda localmente, foi escolhido por ser leve e extremamente rápido em consultas analíticas.
3. **Análise de Dados**: Consultas **SQL** para extrair métricas e responder a perguntas de negócio.

## 📊 Modelagem Dimensional (Star Schema)

O projeto simula uma operação de E-commerce. O modelo de dados foi estruturado em um esquema estrela, onde temos uma tabela central de **Fatos** cercada por tabelas de **Dimensão**.

### Tabelas de Dimensão
As dimensões armazenam o contexto dos eventos.

* **`dim_cliente`**:
  - `id_cliente` (PK)
  - `nome`
  - `email`
  - `cidade`
  - `estado`

* **`dim_produto`**:
  - `id_produto` (PK)
  - `nome_produto`
  - `categoria`
  - `preco`

* **`dim_loja`**:
  - `id_loja` (PK)
  - `nome_loja`
  - `cidade`
  - `estado`

* **`dim_tempo`**:
  - `data` (PK)
  - `dia`
  - `mes`
  - `ano`
  - `trimestre`
  - `dia_da_semana`

### Tabela Fato
A tabela fato armazena as transações (os eventos de venda).

* **`fato_vendas`**:
  - `id_venda` (PK)
  - `id_cliente` (FK)
  - `id_produto` (FK)
  - `id_loja` (FK)
  - `data_venda` (FK)
  - `quantidade`
  - `valor_unitario`
  - `valor_total` (quantidade * valor_unitario)

## 🚀 Como Executar o Projeto

Siga as instruções abaixo para recriar o ambiente, gerar os dados e realizar as análises:

### 1. Configuração do Ambiente
Certifique-se de ter o Python instalado. Clone este repositório e instale as dependências:
```bash
pip install -r requirements.txt
```

### 2. Geração dos Dados
Execute o script para gerar os dados fictícios. Os arquivos `.csv` serão salvos no diretório `data/`.
```bash
python generate_data.py
```

### 3. Carga dos Dados (Load to DuckDB)
Execute o script de carga. Ele criará o banco local `ecommerce.db` (DuckDB) e persistirá as dimensões e os fatos.
```bash
python load_to_duckdb.py
```

### 4. Análise de Dados (Queries)
Por fim, execute o script de análise, que rodará as perguntas de negócio desenhadas no arquivo `analytics_queries.sql` e apresentará os resultados no terminal (usando Pandas).
```bash
python run_queries.py
```

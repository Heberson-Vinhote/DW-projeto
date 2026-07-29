# Projeto de Data Warehouse - E-commerce

Este é um projeto de Data Warehouse construído do zero, idealizado para compor um portfólio de Engenharia de Dados. O objetivo do projeto é demonstrar a modelagem de um banco de dados analítico (Data Warehouse) utilizando a abordagem de **Star Schema (Esquema Estrela)**, geração de dados fictícios para simular um ambiente real, carga de dados em um banco analítico e consultas SQL para análise de negócio.

## 🏗 Arquitetura do Projeto
O pipeline de dados foi desenhado da seguinte maneira:
1. **Extração e Carga (Extract & Load)**: Scripts em **Python** utilizando `pandas` e `Faker` geram dados brutos transacionais simulando fontes externas e os carregam em um schema `raw` no **DuckDB**.
2. **Transformação e Qualidade (Transform)**: O **dbt (Data Build Tool)** atua na camada analítica para:
   - Limpar e modelar os dados brutos no formato de um Star Schema.
   - Calcular métricas de negócio (como o Valor Total de cada venda).
   - Executar testes de qualidade automáticos (garantindo que não existam IDs nulos ou duplicados).
3. **Armazenamento (Data Warehouse)**: O repositório utiliza o **DuckDB**, um banco de dados OLAP embutido e de altíssimo desempenho, como a engine principal.
4. **Análise de Dados**: Consultas **SQL** prontas para extrair métricas de alto nível.
5. **Visualização (Apresentação)**: Dashboard interativo desenvolvido 100% em **Python (Streamlit)** e integração preparada para **Microsoft Power BI**.

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
Certifique-se de ter o Python instalado. Clone este repositório.
É **altamente recomendável** criar um ambiente virtual (para evitar conflitos e garantir que o comando `dbt` seja reconhecido corretamente pelo seu terminal):

**No Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**No Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Executar o Pipeline (Orquestração)
Você pode rodar todo o pipeline de ponta a ponta através do script principal. Ele irá gerar os dados, criar o banco de dados e executar as queries:
```bash
python run_pipeline.py
```

### 📈 Visualização: Executar o Dashboard em Streamlit (Python)
Para visualizar as métricas do Data Warehouse em uma página web interativa, execute o seguinte comando:
```bash
streamlit run dashboard.py
```
*(Isso abrirá uma nova aba no seu navegador padrão com os gráficos gerados dinamicamente)*

### 📈 Visualização: Integração com Microsoft Power BI
Para criar Dashboards e visualizações em cima dos dados gerados, você pode integrar este projeto diretamente com o Power BI das seguintes maneiras:

**Opção 1: Via CSV (Mais Simples)**
1. Abra o Power BI Desktop.
2. Vá em **Obter Dados** > **Texto/CSV**.
3. Navegue até a pasta `data/` do repositório e importe cada um dos arquivos (`fato_vendas.csv`, `dim_cliente.csv`, etc.).
4. No Power BI, vá na aba **Exibição de Modelo** e conecte os `ID`s da tabela Fato com os `ID`s das tabelas Dimensão formando o Esquema Estrela.

**Opção 2: Via DuckDB ODBC (Avançado)**
1. Instale o driver [DuckDB ODBC](https://duckdb.org/docs/api/odbc/overview).
2. Configure uma conexão DSN (Data Source Name) no Windows apontando para o arquivo `ecommerce.db` na raiz do projeto.
3. No Power BI, vá em **Obter Dados** > **ODBC** e selecione a conexão criada.

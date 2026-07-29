import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# Configuração inicial da página Streamlit
st.set_page_config(page_title="Dashboard E-commerce", page_icon="🛒", layout="wide")

st.title("🛒 Dashboard de E-commerce (Data Warehouse)")
st.markdown("Bem-vindo ao dashboard! Os dados abaixo foram modelados com **dbt** e consultados diretamente do **DuckDB**.")

@st.cache_data
def load_data():
    """Função para conectar no DuckDB e carregar as tabelas já transformadas."""
    try:
        # Modo leitura (read_only=True) evita lock no banco se outro script estiver rodando
        con = duckdb.connect(database='ecommerce.db', read_only=True)

        # Consulta juntando a Fato com as Dimensões principais
        query = """
            SELECT
                f.id_venda,
                c.nome as cliente,
                p.nome_produto,
                p.categoria,
                l.nome_loja,
                l.cidade as cidade_loja,
                t.data,
                t.mes,
                t.ano,
                f.quantidade,
                f.valor_unitario,
                f.valor_total
            FROM main.fato_vendas f
            JOIN main.dim_cliente c ON f.id_cliente = c.id_cliente
            JOIN main.dim_produto p ON f.id_produto = p.id_produto
            JOIN main.dim_loja l ON f.id_loja = l.id_loja
            JOIN main.dim_tempo t ON f.data_venda = t.data
        """
        df = con.execute(query).fetchdf()

        # Converte a string de data para datetime no pandas
        df['data'] = pd.to_datetime(df['data'])
        con.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar banco de dados. Certifique-se que o banco foi gerado rodando `python run_pipeline.py`. Detalhes: {e}")
        return pd.DataFrame()

# Carregar os dados
df_vendas = load_data()

if not df_vendas.empty:
    # --- MÉTRICAS GERAIS (KPIs) ---
    st.header("Métricas Principais")
    receita_total = df_vendas['valor_total'].sum()
    total_vendas = df_vendas['id_venda'].nunique()
    ticket_medio = receita_total / total_vendas

    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("Qtd. de Pedidos", total_vendas)
    col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.markdown("---")

    # --- GRÁFICOS ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Receita por Categoria")
        receita_categoria = df_vendas.groupby('categoria')['valor_total'].sum().reset_index()
        fig_cat = px.bar(receita_categoria, x='categoria', y='valor_total',
                         color='categoria', text_auto='.2s',
                         labels={'valor_total': 'Receita (R$)', 'categoria': 'Categoria'})
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_chart2:
        st.subheader("Receita Temporal (Mês a Mês)")
        # Agrupa por Mês/Ano (período)
        df_vendas['ano_mes'] = df_vendas['data'].dt.to_period('M').astype(str)
        receita_tempo = df_vendas.groupby('ano_mes')['valor_total'].sum().reset_index()
        fig_tempo = px.line(receita_tempo, x='ano_mes', y='valor_total', markers=True,
                            labels={'valor_total': 'Receita (R$)', 'ano_mes': 'Mês/Ano'})
        st.plotly_chart(fig_tempo, use_container_width=True)

    # --- TABELAS DETALHADAS ---
    st.markdown("---")
    st.subheader("Ranking: Top 5 Clientes e Top 5 Lojas")

    col_table1, col_table2 = st.columns(2)

    with col_table1:
        st.markdown("**Top Clientes (por valor gasto)**")
        top_clientes = df_vendas.groupby('cliente')['valor_total'].sum().sort_values(ascending=False).head(5).reset_index()
        top_clientes['valor_total'] = top_clientes['valor_total'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(top_clientes, width='stretch')

    with col_table2:
        st.markdown("**Top Lojas (por faturamento)**")
        top_lojas = df_vendas.groupby(['nome_loja', 'cidade_loja'])['valor_total'].sum().sort_values(ascending=False).head(5).reset_index()
        top_lojas['valor_total'] = top_lojas['valor_total'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(top_lojas, width='stretch')

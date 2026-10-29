import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de Vendas com IA",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def gerar_dados():
    dados = [
        ["2026-10-01", "Notebook", "Eletrônicos", 2, 3500],
        ["2026-10-02", "Mouse", "Acessórios", 10, 80],
        ["2026-10-03", "Teclado", "Acessórios", 6, 150],
        ["2026-10-04", "Monitor", "Eletrônicos", 3, 1200],
        ["2026-10-05", "Cadeira", "Móveis", 4, 650],
        ["2026-10-06", "Notebook", "Eletrônicos", 1, 3500],
        ["2026-10-07", "Mouse", "Acessórios", 15, 80],
        ["2026-10-08", "Monitor", "Eletrônicos", 2, 1200],
        ["2026-10-09", "Cadeira", "Móveis", 3, 650],
        ["2026-10-10", "Teclado", "Acessórios", 8, 150],
        ["2026-10-11", "Notebook", "Eletrônicos", 2, 3500],
        ["2026-10-12", "Mouse", "Acessórios", 12, 80],
        ["2026-10-13", "Monitor", "Eletrônicos", 4, 1200],
        ["2026-10-14", "Cadeira", "Móveis", 2, 650],
        ["2026-10-15", "Teclado", "Acessórios", 9, 150],
    ]

    df = pd.DataFrame(
        dados,
        columns=[
            "Data", "Produto", "Categoria",
            "Quantidade", "Preco_unitario"
        ]
    )

    df["Data"] = pd.to_datetime(df["Data"])
    df["Faturamento"] = (
        df["Quantidade"] * df["Preco_unitario"]
    )

    return df


df = gerar_dados()

st.title("📊 Dashboard de Vendas com IA")
st.write(
    "Análise de vendas, indicadores e recomendações "
    "automáticas para apoiar decisões."
)

# Filtros
st.sidebar.header("Filtros")

categorias = ["Todas"] + sorted(
    df["Categoria"].unique().tolist()
)

categoria = st.sidebar.selectbox(
    "Selecione a categoria",
    categorias
)

if categoria != "Todas":
    df = df[df["Categoria"] == categoria]

# Indicadores
faturamento = df["Faturamento"].sum()
unidades = df["Quantidade"].sum()
pedidos = len(df)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Faturamento total",
    f"R$ {faturamento:,.2f}"
)

col2.metric(
    "Unidades vendidas",
    f"{unidades:,}"
)

col3.metric(
    "Registros de venda",
    pedidos
)

st.divider()

# Gráfico de faturamento por produto
st.subheader("Faturamento por produto")

vendas_produto = (
    df.groupby("Produto")["Faturamento"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(vendas_produto)

# Gráfico de quantidade vendida
st.subheader("Quantidade vendida por produto")

quantidade_produto = (
    df.groupby("Produto")["Quantidade"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(quantidade_produto)

# Recomendações automáticas
st.subheader("🤖 Análise automática")

if not df.empty:
    produto_lider = vendas_produto.index[0]
    valor_lider = vendas_produto.iloc[0]

    produto_quantidade = quantidade_produto.index[0]

    st.success(
        f"O produto com maior faturamento é "
        f"{produto_lider}, com R$ {valor_lider:,.2f}."
    )

    st.info(
        f"O produto com maior quantidade vendida é "
        f"{produto_quantidade}."
    )

    if len(vendas_produto) > 1:
        menor = vendas_produto.index[-1]
        st.warning(
            f"Vale investigar o desempenho de {menor} "
            "antes de decidir mudanças de estoque ou preço."
        )
else:
    st.warning("Não existem vendas para os filtros selecionados.")

# Tabela de dados
st.subheader("Dados das vendas")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Exportação
csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "Baixar relatório CSV",
    data=csv,
    file_name="relatorio_vendas.csv",
    mime="text/csv"
)

st.caption(
    "Projeto demonstrativo com dados fictícios. "
    "As recomendações atuais são baseadas em regras, "
    "não em um modelo de IA."
)
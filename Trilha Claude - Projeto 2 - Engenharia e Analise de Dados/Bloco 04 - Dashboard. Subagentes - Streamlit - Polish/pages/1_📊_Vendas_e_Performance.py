import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.supabase_client import load_full_dataset

st.set_page_config(page_title="Vendas & Performance | E-Commerce", page_icon="📊", layout="wide")

# Carrega os dados
@st.cache_data(ttl=300)
def get_data():
    return load_full_dataset()

datasets = get_data()
vendas_df = datasets["vendas_enriquecidas"]

st.title("📊 Vendas & Performance Operacional")
st.markdown("Diagnóstico aprofundado de receita temporal, sazonalidade diária e curva ABC de produtos.")

# Filtros na página
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    canais = ["Todos"] + sorted(vendas_df["canal_venda"].dropna().unique().tolist())
    canal_sel = st.selectbox("Filtrar Canal", canais)
with col_f2:
    cats = ["Todas"] + sorted(vendas_df["categoria"].dropna().unique().tolist())
    cat_sel = st.selectbox("Filtrar Categoria", cats)
with col_f3:
    marcas = ["Todas"] + sorted(vendas_df["marca"].dropna().unique().tolist())
    marca_sel = st.selectbox("Filtrar Marca", marcas)

df = vendas_df.copy()
if canal_sel != "Todos":
    df = df[df["canal_venda"] == canal_sel]
if cat_sel != "Todas":
    df = df[df["categoria"] == cat_sel]
if marca_sel != "Todas":
    df = df[df["marca"] == marca_sel]

# Mini Cards de Performance
m1, m2, m3, m4 = st.columns(4)
rec = df["valor_total"].sum()
ped = len(df)
tkt = rec / ped if ped > 0 else 0
itens = df["quantidade"].sum()

m1.metric("Receita no Filtro", f"R$ {rec:,.2f}")
m2.metric("Transações", f"{ped:,}")
m3.metric("Ticket Médio", f"R$ {tkt:,.2f}")
m4.metric("Total Itens Vendidos", f"{itens:,}")

st.markdown("---")

# Linha 1: Gráfico Temporal detalhado e Horários de Pico
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📅 Faturamento ao Longo do Tempo")
    df_tempo = df.groupby(df["data_venda"].dt.date)["valor_total"].sum().reset_index()
    df_tempo.columns = ["Data", "Receita"]
    
    fig_time = px.line(
        df_tempo,
        x="Data",
        y="Receita",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#6366F1"]
    )
    fig_time.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320
    )
    st.plotly_chart(fig_time, use_container_width=True)

with c2:
    st.subheader("⏰ Vendas por Horário do Dia")
    df["hora"] = df["data_venda"].dt.hour
    vendas_hora = df.groupby("hora")["valor_total"].sum().reset_index()
    
    fig_hora = px.bar(
        vendas_hora,
        x="hora",
        y="valor_total",
        labels={"hora": "Hora (0h-23h)", "valor_total": "Receita (R$)"},
        color_discrete_sequence=["#EC4899"]
    )
    fig_hora.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320
    )
    st.plotly_chart(fig_hora, use_container_width=True)

st.markdown("---")

# Linha 2: Curva ABC de Produtos
st.subheader("📦 Curva ABC e Ranking de Produtos")

prod_summary = df.groupby(["id_produto", "nome_produto", "categoria", "marca"]).agg(
    receita_total=("valor_total", "sum"),
    pedidos=("id_venda", "count"),
    itens_vendidos=("quantidade", "sum"),
    preco_medio=("preco_unitario", "mean")
).reset_index().sort_values(by="receita_total", ascending=False)

if not prod_summary.empty:
    total_faturado = prod_summary["receita_total"].sum()
    prod_summary["percentual_receita"] = (prod_summary["receita_total"] / total_faturado) * 100
    prod_summary["percentual_acumulado"] = prod_summary["percentual_receita"].cumsum()
    
    # Classificação ABC (A: até 80%, B: 80% a 95%, C: 95% a 100%)
    def classificar_abc(pct_acum):
        if pct_acum <= 80:
            return "Curva A (80%)"
        elif pct_acum <= 95:
            return "Curva B (15%)"
        else:
            return "Curva C (5%)"
            
    prod_summary["classificacao_abc"] = prod_summary["percentual_acumulado"].apply(classificar_abc)
    
    col_abc1, col_abc2 = st.columns([1, 2])
    with col_abc1:
        fig_abc = px.pie(
            prod_summary,
            names="classificacao_abc",
            values="receita_total",
            hole=0.5,
            color="classificacao_abc",
            color_discrete_map={
                "Curva A (80%)": "#10B981",
                "Curva B (15%)": "#F59E0B",
                "Curva C (5%)": "#EF4444"
            }
        )
        fig_abc.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=300
        )
        st.plotly_chart(fig_abc, use_container_width=True)
    
    with col_abc2:
        top_10 = prod_summary.head(10)
        fig_top = px.bar(
            top_10,
            x="receita_total",
            y="nome_produto",
            orientation="h",
            text_auto=",.0f",
            color="classificacao_abc",
            color_discrete_map={"Curva A (80%)": "#10B981", "Curva B (15%)": "#F59E0B"},
            labels={"receita_total": "Receita (R$)", "nome_produto": "Produto"}
        )
        fig_top.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_top, use_container_width=True)

    st.dataframe(
        prod_summary[[
            "nome_produto", "categoria", "marca", "classificacao_abc", 
            "receita_total", "pedidos", "itens_vendidos", "preco_medio"
        ]].rename(columns={
            "nome_produto": "Produto",
            "categoria": "Categoria",
            "marca": "Marca",
            "classificacao_abc": "Curva ABC",
            "receita_total": "Receita (R$)",
            "pedidos": "Qtd Pedidos",
            "itens_vendidos": "Itens Vendidos",
            "preco_medio": "Preço Médio (R$)"
        }).style.format({
            "Receita (R$)": "R$ {:,.2f}",
            "Preço Médio (R$)": "R$ {:,.2f}"
        }),
        use_container_width=True
    )

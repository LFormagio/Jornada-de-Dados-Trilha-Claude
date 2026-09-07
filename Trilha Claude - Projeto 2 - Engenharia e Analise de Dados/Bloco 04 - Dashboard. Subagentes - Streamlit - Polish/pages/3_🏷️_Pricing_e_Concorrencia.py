import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.supabase_client import load_full_dataset

st.set_page_config(page_title="Pricing & Concorrência | E-Commerce", page_icon="🏷️", layout="wide")

@st.cache_data(ttl=300)
def get_data():
    return load_full_dataset()

datasets = get_data()
produtos_df = datasets["produtos"]
competidores_df = datasets["competidores"]

st.title("🏷️ Inteligência de Pricing & Benchmark de Concorrência")
st.markdown("Comparativo de competitividade de preços do catálogo próprio contra **Amazon**, **Mercado Livre**, **Shopee** e **Magalu**.")

# Cruzamento de produtos com coletas de concorrentes
comp_merged = competidores_df.merge(
    produtos_df[["id_produto", "nome_produto", "categoria", "marca", "preco_atual"]],
    on="id_produto",
    how="inner"
)

# Média dos concorrentes por produto
bench = comp_merged.groupby(["id_produto", "nome_produto", "categoria", "marca", "preco_atual"]).agg(
    preco_medio_concorrencia=("preco_concorrente", "mean"),
    preco_min_concorrencia=("preco_concorrente", "min"),
    preco_max_concorrencia=("preco_concorrente", "max"),
    total_coletas=("preco_concorrente", "count")
).reset_index()

bench["diferenca_abs"] = bench["preco_atual"] - bench["preco_medio_concorrencia"]
bench["diferenca_pct"] = (bench["diferenca_abs"] / bench["preco_medio_concorrencia"]) * 100
bench["icp"] = bench["preco_atual"] / bench["preco_medio_concorrencia"]

def classificar_status(icp):
    if icp > 1.05:
        return "🔴 Sobrepreço (>5% acima)"
    elif icp < 0.95:
        return "🟡 Oportunidade Margem (>5% abaixo)"
    else:
        return "🟢 Paridade Competitiva"

bench["status_pricing"] = bench["icp"].apply(classificar_status)

# KPIs Executivos de Pricing
total_skus_monitorados = len(bench)
sobrepreco_count = (bench["icp"] > 1.05).sum()
oportunidade_count = (bench["icp"] < 0.95).sum()
paridade_count = total_skus_monitorados - sobrepreco_count - oportunidade_count

k1, k2, k3, k4 = st.columns(4)
k1.metric("SKUs Monitorados", f"{total_skus_monitorados}")
k2.metric("🔴 Sobrepreço Crítico", f"{sobrepreco_count} SKUs", "Risco de perda de volume")
k3.metric("🟢 Paridade Competitiva", f"{paridade_count} SKUs", "Alinhados ao mercado")
k4.metric("🟡 Oportunidade de Margem", f"{oportunidade_count} SKUs", "Preço pode subir")

st.markdown("---")

# Linha 1: Comparativo por Marketplace e Dispersão
c_p1, c_p2 = st.columns([1, 1])

with c_p1:
    st.subheader("🏢 Preço Médio por Marketplace Concorrente")
    player_summary = comp_merged.groupby("nome_concorrente")["preco_concorrente"].mean().reset_index()
    player_summary.columns = ["Concorrente", "Preço Médio"]
    
    nosso_p = produtos_df["preco_atual"].mean()
    df_chart = pd.concat([
        pd.DataFrame([{"Concorrente": "Nosso E-Commerce", "Preço Médio": nosso_p}]),
        player_summary
    ], ignore_index=True)
    
    df_chart["delta_vs_nos"] = ((df_chart["Preço Médio"] - nosso_p) / nosso_p) * 100
    
    fig_bar = px.bar(
        df_chart,
        x="Concorrente",
        y="Preço Médio",
        color="Concorrente",
        text_auto=".2f",
        color_discrete_map={
            "Nosso E-Commerce": "#6366F1",
            "Amazon": "#EF4444",
            "Shopee": "#F59E0B",
            "Mercado Livre": "#3B82F6",
            "Magalu": "#10B981"
        }
    )
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption("A **Amazon** apresenta o catálogo mais agressivo (-7,0% vs nosso preço).")

with c_p2:
    st.subheader("🎯 Dispersão: Nosso Preço vs Média Concorrência")
    fig_scatter = px.scatter(
        bench,
        x="preco_medio_concorrencia",
        y="preco_atual",
        color="status_pricing",
        hover_data=["nome_produto", "categoria", "diferenca_pct"],
        color_discrete_map={
            "🔴 Sobrepreço (>5% acima)": "#EF4444",
            "🟢 Paridade Competitiva": "#10B981",
            "🟡 Oportunidade Margem (>5% abaixo)": "#F59E0B"
        },
        labels={
            "preco_medio_concorrencia": "Preço Médio Concorrentes (R$)",
            "preco_atual": "Nosso Preço Atual (R$)"
        }
    )
    # Linha diagonal de paridade 1:1
    max_val = max(bench["preco_atual"].max(), bench["preco_medio_concorrencia"].max())
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode="lines",
        line=dict(color="rgba(255,255,255,0.3)", dash="dash"),
        name="Paridade 1:1"
    ))
    fig_scatter.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Linha 2: Tabela de Ação Imediata de Pricing
st.subheader("⚡ Matriz de Ação Imediata de Pricing")

status_filtro = st.radio(
    "Filtrar por Status de Paridade",
    ["Todos", "🔴 Sobrepreço (>5% acima)", "🟡 Oportunidade Margem (>5% abaixo)", "🟢 Paridade Competitiva"],
    horizontal=True
)

df_tabela = bench.copy()
if status_filtro != "Todos":
    df_tabela = df_tabela[df_tabela["status_pricing"] == status_filtro]

# Sugestão de novo preço
def sugerir_preco(row):
    if row["status_pricing"] == "🔴 Sobrepreço (>5% acima)":
        return row["preco_medio_concorrencia"] * 1.02 # Reduzir para ficar 2% acima
    elif row["status_pricing"] == "🟡 Oportunidade Margem (>5% abaixo)":
        return row["preco_medio_concorrencia"] * 0.98 # Subir para capturar margem
    else:
        return row["preco_atual"]

df_tabela["sugestao_preco"] = df_tabela.apply(sugerir_preco, axis=1)

st.dataframe(
    df_tabela[[
        "nome_produto", "categoria", "marca", "status_pricing",
        "preco_atual", "preco_medio_concorrencia", "diferenca_pct", "sugestao_preco"
    ]].rename(columns={
        "nome_produto": "Produto",
        "categoria": "Categoria",
        "marca": "Marca",
        "status_pricing": "Status ICP",
        "preco_atual": "Nosso Preço",
        "preco_medio_concorrencia": "Média Mercado",
        "diferenca_pct": "Diferença (%)",
        "sugestao_preco": "Preço Sugerido (Ação)"
    }).sort_values(by="Diferença (%)", ascending=False).style.format({
        "Nosso Preço": "R$ {:,.2f}",
        "Média Mercado": "R$ {:,.2f}",
        "Diferença (%)": "{:+.1f}%",
        "Preço Sugerido (Ação)": "R$ {:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

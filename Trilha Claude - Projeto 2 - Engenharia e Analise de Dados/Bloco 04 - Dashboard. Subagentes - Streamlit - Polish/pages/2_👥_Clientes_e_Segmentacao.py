import streamlit as st
import pandas as pd
import plotly.express as px
from data.supabase_client import load_full_dataset

st.set_page_config(page_title="Clientes & Segmentação | E-Commerce", page_icon="👥", layout="wide")

@st.cache_data(ttl=300)
def get_data():
    return load_full_dataset()

datasets = get_data()
vendas_df = datasets["vendas_enriquecidas"]
clientes_df = datasets["clientes"]

st.title("👥 Clientes & Inteligência Geográfica")
st.markdown("Mapeamento da base consumidora, concentração de faturamento por estado e identificação dos clientes de maior LTV.")

# KPIs da Base
total_clientes_cadastrados = len(clientes_df)
clientes_com_compras = vendas_df["id_cliente"].nunique()
receita_total = vendas_df["valor_total"].sum()
ltv_medio = receita_total / clientes_com_compras if clientes_com_compras > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Clientes Cadastrados", f"{total_clientes_cadastrados}")
c2.metric("Clientes Ativos (Compradores)", f"{clientes_com_compras}")
c3.metric("LTV Médio por Cliente", f"R$ {ltv_medio:,.2f}")
c4.metric("Média de Pedidos/Cliente", f"{(len(vendas_df)/clientes_com_compras):.1f} pedidos")

st.markdown("---")

# Linha 1: Distribuição Geográfica (Estados)
col_geo1, col_geo2 = st.columns([2, 1])

# Agrupamento por estado
estado_vendas = vendas_df.groupby("estado").agg(
    receita=("valor_total", "sum"),
    pedidos=("id_venda", "count"),
    clientes_unicos=("id_cliente", "nunique")
).reset_index().sort_values(by="receita", ascending=False)

with col_geo1:
    st.subheader("🗺️ Faturamento Consolidado por Estado (UF)")
    fig_uf = px.bar(
        estado_vendas,
        x="estado",
        y="receita",
        color="receita",
        color_continuous_scale="Blues",
        labels={"estado": "Estado (UF)", "receita": "Faturamento (R$)"},
        text_auto=",.0f"
    )
    fig_uf.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=340,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_uf, use_container_width=True)

with col_geo2:
    st.subheader("📌 Top 5 Estados Líderes")
    top_uf = estado_vendas.head(5).copy()
    top_uf["ticket_medio"] = top_uf["receita"] / top_uf["pedidos"]
    st.dataframe(
        top_uf[["estado", "receita", "pedidos", "ticket_medio"]].rename(columns={
            "estado": "UF",
            "receita": "Receita (R$)",
            "pedidos": "Pedidos",
            "ticket_medio": "Ticket Médio"
        }).style.format({
            "Receita (R$)": "R$ {:,.2f}",
            "Ticket Médio": "R$ {:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# Linha 2: Ranking de Clientes VIP (LTV)
st.subheader("👑 Ranking de Clientes VIP (Maior LTV)")

cliente_ltv = vendas_df.groupby(["id_cliente", "nome_cliente", "estado"]).agg(
    total_gasto=("valor_total", "sum"),
    total_pedidos=("id_venda", "count"),
    ticket_medio=("valor_total", "mean"),
    primeira_compra=("data_venda", "min"),
    ultima_compra=("data_venda", "max")
).reset_index().sort_values(by="total_gasto", ascending=False)

c_vip1, c_vip2 = st.columns([2, 1])

with c_vip1:
    st.dataframe(
        cliente_ltv.head(15).rename(columns={
            "nome_cliente": "Cliente",
            "estado": "UF",
            "total_gasto": "LTV (R$)",
            "total_pedidos": "Pedidos",
            "ticket_medio": "Ticket Médio (R$)",
            "primeira_compra": "1ª Compra",
            "ultima_compra": "Última Compra"
        }).style.format({
            "LTV (R$)": "R$ {:,.2f}",
            "Ticket Médio (R$)": "R$ {:,.2f}",
            "1ª Compra": lambda t: t.strftime("%d/%m/%Y"),
            "Última Compra": lambda t: t.strftime("%d/%m/%Y")
        }),
        use_container_width=True,
        hide_index=True
    )

with c_vip2:
    st.subheader("📊 Concentração Top 10 Clientes")
    top_10_ltv = cliente_ltv.head(10)["total_gasto"].sum()
    pct_top10 = (top_10_ltv / receita_total) * 100
    
    fig_share = px.pie(
        values=[top_10_ltv, receita_total - top_10_ltv],
        names=["Top 10 Clientes VIP", "Demais Clientes"],
        hole=0.6,
        color_discrete_sequence=["#10B981", "#334155"]
    )
    fig_share.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280
    )
    st.plotly_chart(fig_share, use_container_width=True)
    st.caption(f"Os 10 maiores clientes representam **{pct_top10:.1f}%** do faturamento total da empresa.")

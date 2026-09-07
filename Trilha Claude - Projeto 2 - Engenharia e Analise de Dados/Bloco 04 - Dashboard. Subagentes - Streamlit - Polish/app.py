import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.supabase_client import load_full_dataset

# Configuração da página Streamlit
st.set_page_config(
    page_title="E-Commerce Intelligence | Supabase MCP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada (Polish UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Cards de métricas premium */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .metric-caption {
        color: #10B981;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 6px;
    }
    
    /* Badges */
    .badge-mcp {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-agent {
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin-right: 4px;
    }
    
    /* Box de Insights */
    .insight-box {
        background: rgba(99, 102, 241, 0.08);
        border-left: 4px solid #6366F1;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Carregamento com Cache do Streamlit
@st.cache_data(ttl=300, show_spinner="Sincronizando dados com o Supabase...")
def get_cached_data():
    return load_full_dataset()

try:
    datasets = get_cached_data()
    vendas_df = datasets["vendas_enriquecidas"]
    competidores_df = datasets["competidores"]
    produtos_df = datasets["produtos"]
    clientes_df = datasets["clientes"]
except Exception as e:
    st.error(f"Erro ao carregar dados do Supabase: {e}")
    st.info("Verifique se as variáveis SUPABASE_URL e SUPABASE_KEY estão corretas no arquivo .env")
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### ⚡ E-Commerce Analytics")
    st.markdown('<div class="badge-mcp">● Supabase MCP Ativo</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🔍 Filtros Globais")
    
    # Filtro de Canal
    canais_disponiveis = ["Todos"] + sorted(vendas_df["canal_venda"].dropna().unique().tolist())
    canal_selecionado = st.selectbox("Canal de Venda", canais_disponiveis)
    
    # Filtro de Categoria
    categorias_disponiveis = sorted(produtos_df["categoria"].dropna().unique().tolist())
    categorias_selecionadas = st.multiselect("Categorias", categorias_disponiveis, default=categorias_disponiveis[:4])
    
    # Filtro de Período
    min_date = vendas_df["data_venda"].min().date()
    max_date = vendas_df["data_venda"].max().date()
    periodo = st.date_input("Período de Vendas", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    st.markdown("---")
    st.markdown("### 🤖 Equipe de Subagentes")
    st.markdown('<span class="badge-agent">👔 Negócio</span> Líder Estratégico', unsafe_allow_html=True)
    st.markdown('<span class="badge-agent">🎨 Visual</span> Especialista UI/UX', unsafe_allow_html=True)
    st.markdown('<span class="badge-agent">🛡️ Arquiteto</span> Segurança & QA', unsafe_allow_html=True)
    st.caption("Trilha Claude • Bloco 04")

# Aplicação dos Filtros
df_filtrado = vendas_df.copy()

if canal_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["canal_venda"] == canal_selecionado]

if categorias_selecionadas:
    df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categorias_selecionadas)]

if isinstance(periodo, (list, tuple)) and len(periodo) == 2:
    start_date, end_date = periodo
    df_filtrado = df_filtrado[
        (df_filtrado["data_venda"].dt.date >= start_date) & 
        (df_filtrado["data_venda"].dt.date <= end_date)
    ]

# ================= CABEÇALHO =================
col_title, col_meta = st.columns([3, 1])
with col_title:
    st.title("Painel Executivo de E-Commerce")
    st.caption("Monitoramento estratégico de faturamento, canais de distribuição e paridade de preços em tempo real.")

with col_meta:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 10px;">
        <span style="color: #94A3B8; font-size: 0.8rem;">Banco: Supabase PostgreSQL</span><br>
        <span style="color: #64748B; font-size: 0.75rem;">Total de Vendas: {len(vendas_df):,} regs</span>
    </div>
    """, unsafe_allow_html=True)

# Caixa de Storytelling Executivo
st.markdown("""
<div class="insight-box">
    <strong>💡 Destaque Executivo (Agente de Negócio):</strong> A operação alcançou 
    <strong>R$ 974,0k</strong> em receita consolidada. O canal de <strong>E-commerce</strong> é o principal motor, 
    respondendo por <strong>72,4%</strong> do faturamento com ticket médio de <strong>R$ 327,37</strong>. 
    Atenção prioritária ao pricing: a <strong>Amazon</strong> lidera a agressividade de preços (-7,0% abaixo do nosso catálogo).
</div>
""", unsafe_allow_html=True)

# ================= CARDS DE KPIS =================
receita_total = df_filtrado["valor_total"].sum()
total_pedidos = len(df_filtrado)
ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0.0
clientes_unicos = df_filtrado["id_cliente"].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Faturamento Bruto</div>
        <div class="metric-value">R$ {receita_total:,.2f}</div>
        <div class="metric-caption">↑ {total_pedidos:,} transações</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Volume de Pedidos</div>
        <div class="metric-value">{total_pedidos:,}</div>
        <div class="metric-caption">Itens vendidos: {df_filtrado['quantidade'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Ticket Médio</div>
        <div class="metric-value">R$ {ticket_medio:,.2f}</div>
        <div class="metric-caption">Média por pedido</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Clientes Compradores</div>
        <div class="metric-value">{clientes_unicos}</div>
        <div class="metric-caption">Base ativa no período</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= GRÁFICOS PRINCIPAIS =================
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("📈 Evolução Diária de Receita")
    
    if not df_filtrado.empty:
        vendas_diarias = df_filtrado.groupby(df_filtrado["data_venda"].dt.date)["valor_total"].sum().reset_index()
        vendas_diarias.columns = ["data", "receita"]
        vendas_diarias["media_movel_7d"] = vendas_diarias["receita"].rolling(7, min_periods=1).mean()
        
        fig_evolucao = go.Figure()
        fig_evolucao.add_trace(go.Bar(
            x=vendas_diarias["data"],
            y=vendas_diarias["receita"],
            name="Receita Diária",
            marker_color="rgba(99, 102, 241, 0.45)",
            marker_line_color="#6366F1",
            marker_line_width=1
        ))
        fig_evolucao.add_trace(go.Scatter(
            x=vendas_diarias["data"],
            y=vendas_diarias["media_movel_7d"],
            name="Média Móvel (7d)",
            line=dict(color="#10B981", width=3)
        ))
        fig_evolucao.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
            height=320
        )
        st.plotly_chart(fig_evolucao, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

with row1_col2:
    st.subheader("🛍️ Distribuição por Canal")
    if not df_filtrado.empty:
        canal_sum = df_filtrado.groupby("canal_venda")["valor_total"].sum().reset_index()
        fig_canal = px.pie(
            canal_sum,
            values="valor_total",
            names="canal_venda",
            hole=0.55,
            color="canal_venda",
            color_discrete_map={"ecommerce": "#6366F1", "loja_fisica": "#EC4899"}
        )
        fig_canal.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            showlegend=True
        )
        st.plotly_chart(fig_canal, use_container_width=True)

# ================= SEGUNDA LINHA DE GRÁFICOS =================
row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.subheader("🏆 Top 5 Categorias por Faturamento")
    if not df_filtrado.empty:
        top_cat = df_filtrado.groupby("categoria")["valor_total"].sum().sort_values(ascending=True).tail(5).reset_index()
        fig_cat = px.bar(
            top_cat,
            x="valor_total",
            y="categoria",
            orientation="h",
            color="valor_total",
            color_continuous_scale="Viridis",
            labels={"valor_total": "Receita (R$)", "categoria": "Categoria"}
        )
        fig_cat.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_cat, use_container_width=True)

with row2_col2:
    st.subheader("🏷️ Benchmark de Preço vs Concorrentes")
    if not competidores_df.empty:
        comp_agg = competidores_df.groupby("nome_concorrente")["preco_concorrente"].mean().reset_index()
        comp_agg.columns = ["Player", "Preço Médio"]
        
        # Adiciona nosso preço médio geral
        nosso_preco_medio = produtos_df["preco_atual"].mean()
        df_players = pd.concat([
            pd.DataFrame([{"Player": "Nosso E-Commerce", "Preço Médio": nosso_preco_medio}]),
            comp_agg
        ], ignore_index=True)
        
        colors = ["#6366F1" if p == "Nosso E-Commerce" else "#64748B" for p in df_players["Player"]]
        fig_comp = px.bar(
            df_players,
            x="Player",
            y="Preço Médio",
            text_auto=".2f",
            color="Player",
            color_discrete_map={"Nosso E-Commerce": "#6366F1"}
        )
        fig_comp.update_traces(marker_color=colors)
        fig_comp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")
st.caption("Use o menu lateral para navegar entre as páginas detalhadas: **Vendas e Performance**, **Clientes e Segmentação** e **Pricing e Concorrência**.")

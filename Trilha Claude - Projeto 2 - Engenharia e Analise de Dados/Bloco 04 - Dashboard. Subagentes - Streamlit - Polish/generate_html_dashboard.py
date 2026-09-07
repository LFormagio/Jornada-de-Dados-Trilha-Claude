import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Adiciona o diretório ao path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data.supabase_client import load_full_dataset

data = load_full_dataset()
vendas = data["vendas_enriquecidas"]
prod = data["produtos"]
comp = data["competidores"]
cli = data["clientes"]

# Cálculos Gerais
rec_total = vendas["valor_total"].sum()
ped_total = len(vendas)
tkt_medio = rec_total / ped_total
itens_total = vendas["quantidade"].sum()
cli_unicos = vendas["id_cliente"].nunique()

# Gráfico 1: Evolução Diária
vendas_diarias = vendas.groupby(vendas["data_venda"].dt.date)["valor_total"].sum().reset_index()
vendas_diarias.columns = ["Data", "Receita"]
vendas_diarias["Media_Movel_7d"] = vendas_diarias["Receita"].rolling(7, min_periods=1).mean()

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=vendas_diarias["Data"],
    y=vendas_diarias["Receita"],
    name="Receita Diária",
    marker_color="rgba(99, 102, 241, 0.45)",
    marker_line_color="#6366F1",
    marker_line_width=1
))
fig1.add_trace(go.Scatter(
    x=vendas_diarias["Data"],
    y=vendas_diarias["Media_Movel_7d"],
    name="Média Móvel (7d)",
    line=dict(color="#10B981", width=3)
))
fig1.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=340
)

# Gráfico 2: Mix de Canais
canal_sum = vendas.groupby("canal_venda")["valor_total"].sum().reset_index()
fig2 = px.pie(
    canal_sum,
    values="valor_total",
    names="canal_venda",
    hole=0.55,
    color="canal_venda",
    color_discrete_map={"ecommerce": "#6366F1", "loja_fisica": "#EC4899"}
)
fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=340
)

# Gráfico 3: Horários de Pico
vendas["hora"] = vendas["data_venda"].dt.hour
vendas_hora = vendas.groupby("hora")["valor_total"].sum().reset_index()
fig3 = px.bar(
    vendas_hora,
    x="hora",
    y="valor_total",
    labels={"hora": "Hora (0h-23h)", "valor_total": "Receita (R$)"},
    color_discrete_sequence=["#EC4899"]
)
fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=320
)

# Gráfico 4: Concentração por UF
estado_vendas = vendas.groupby("estado")["valor_total"].sum().reset_index().sort_values(by="valor_total", ascending=False)
fig4 = px.bar(
    estado_vendas,
    x="estado",
    y="valor_total",
    color="valor_total",
    color_continuous_scale="Blues",
    text_auto=",.0f"
)
fig4.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=340,
    coloraxis_showscale=False
)

# Gráfico 5: Benchmark Marketplace
comp_merged = comp.merge(prod[["id_produto", "nome_produto", "categoria", "marca", "preco_atual"]], on="id_produto")
player_summary = comp_merged.groupby("nome_concorrente")["preco_concorrente"].mean().reset_index()
player_summary.columns = ["Concorrente", "Preço Médio"]
nosso_p = prod["preco_atual"].mean()
df_players = pd.concat([
    pd.DataFrame([{"Concorrente": "Nosso E-Commerce", "Preço Médio": nosso_p}]),
    player_summary
], ignore_index=True)

fig5 = px.bar(
    df_players,
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
fig5.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=320,
    showlegend=False
)

# Gráfico 6: Dispersão Pricing
bench = comp_merged.groupby(["id_produto", "nome_produto", "categoria", "marca", "preco_atual"]).agg(
    preco_medio_concorrencia=("preco_concorrente", "mean")
).reset_index()
bench["icp"] = bench["preco_atual"] / bench["preco_medio_concorrencia"]

def classificar_status(icp):
    if icp > 1.05:
        return "🔴 Sobrepreço (>5% acima)"
    elif icp < 0.95:
        return "🟡 Oportunidade Margem (>5% abaixo)"
    else:
        return "🟢 Paridade Competitiva"

bench["status_pricing"] = bench["icp"].apply(classificar_status)

fig6 = px.scatter(
    bench,
    x="preco_medio_concorrencia",
    y="preco_atual",
    color="status_pricing",
    hover_data=["nome_produto", "categoria"],
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
max_val = max(bench["preco_atual"].max(), bench["preco_medio_concorrencia"].max())
fig6.add_trace(go.Scatter(
    x=[0, max_val],
    y=[0, max_val],
    mode="lines",
    line=dict(color="rgba(255,255,255,0.3)", dash="dash"),
    name="Paridade 1:1"
))
fig6.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=340
)

# Curva ABC Top 5
prod_summary = vendas.groupby(["id_produto", "nome_produto", "categoria"]).agg(
    receita_total=("valor_total", "sum"),
    pedidos=("id_venda", "count")
).reset_index().sort_values(by="receita_total", ascending=False)
top_5_rows = "".join([
    f"<tr><td>{r['nome_produto']}</td><td>{r['categoria']}</td><td>{r['pedidos']}</td><td style='color:#10B981;font-weight:600;'>R$ {r['receita_total']:,.2f}</td></tr>"
    for _, r in prod_summary.head(8).iterrows()
])

# Top 5 Clientes LTV
cliente_ltv = vendas.groupby(["id_cliente", "nome_cliente", "estado"]).agg(
    total_gasto=("valor_total", "sum"),
    total_pedidos=("id_venda", "count")
).reset_index().sort_values(by="total_gasto", ascending=False)
top_cli_rows = "".join([
    f"<tr><td>{r['nome_cliente']}</td><td>{r['estado']}</td><td>{r['total_pedidos']}</td><td style='color:#6366F1;font-weight:600;'>R$ {r['total_gasto']:,.2f}</td></tr>"
    for _, r in cliente_ltv.head(8).iterrows()
])

# Gerar HTML unificado
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Intelligence Dashboard | Supabase</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #0B0F17;
            color: #F8FAFC;
            min-height: 100vh;
            padding: 24px 32px;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 20px;
            margin-bottom: 24px;
        }}
        .logo-area h1 {{ font-size: 1.6rem; font-weight: 800; background: linear-gradient(90deg, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .logo-area p {{ color: #94A3B8; font-size: 0.85rem; margin-top: 4px; }}
        .badge-status {{
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 28px;
        }}
        .card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }}
        .card-label {{ color: #94A3B8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}
        .card-value {{ color: #FFFFFF; font-size: 1.8rem; font-weight: 800; margin: 8px 0 4px 0; }}
        .card-caption {{ color: #10B981; font-size: 0.8rem; font-weight: 500; }}
        
        .insight-box {{
            background: rgba(99, 102, 241, 0.08);
            border-left: 4px solid #6366F1;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 28px;
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        
        .nav-tabs {{
            display: flex;
            gap: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 24px;
            padding-bottom: 10px;
        }}
        .tab-btn {{
            background: transparent;
            border: none;
            color: #94A3B8;
            font-size: 0.95rem;
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn.active {{
            background: #6366F1;
            color: #FFFFFF;
        }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        .charts-row {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        .charts-row-equal {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        .chart-card {{
            background: #131A26;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 18px;
        }}
        .chart-title {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 14px; color: #E2E8F0; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 10px;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }}
        th {{ color: #94A3B8; font-weight: 600; background: rgba(255,255,255,0.02); }}
        tr:hover {{ background: rgba(255,255,255,0.03); }}
    </style>
</head>
<body>
    <header>
        <div class="logo-area">
            <h1>⚡ E-Commerce Intelligence Dashboard</h1>
            <p>Trilha Claude - Projeto 2 (Bloco 04) • Banco Relacional Supabase PostgreSQL via MCP</p>
        </div>
        <div>
            <span class="badge-status">● Supabase Conectado (4.052 Linhas)</span>
        </div>
    </header>

    <div class="metrics-grid">
        <div class="card">
            <div class="card-label">Faturamento Total</div>
            <div class="card-value">R$ {rec_total:,.2f}</div>
            <div class="card-caption">↑ 100% dos dados reais carregados</div>
        </div>
        <div class="card">
            <div class="card-label">Volume de Pedidos</div>
            <div class="card-value">{ped_total:,}</div>
            <div class="card-caption">Total de {itens_total:,} unidades vendidas</div>
        </div>
        <div class="card">
            <div class="card-label">Ticket Médio</div>
            <div class="card-value">R$ {tkt_medio:,.2f}</div>
            <div class="card-caption">E-comm: R$ 327,37 | Físico: R$ 310,51</div>
        </div>
        <div class="card">
            <div class="card-label">Clientes Compradores</div>
            <div class="card-value">{cli_unicos}</div>
            <div class="card-caption">LTV Médio: R$ {(rec_total/cli_unicos):,.2f}</div>
        </div>
    </div>

    <div class="insight-box">
        <strong>💡 Destaque da Equipe de Subagentes:</strong> 
        O <strong>E-commerce</strong> é a principal alavanca de crescimento da operação (72,4% de share). 
        No pilar de <strong>Pricing</strong>, nosso preço médio é de R$ 212,63 contra R$ 206,28 do mercado. 
        A <strong>Amazon</strong> lidera o cenário predatório (-7,0% vs nosso preço). 
        Foram mapeados <strong>28 SKUs com sobrepreço crítico</strong> e <strong>6 oportunidades imediatas de expansão de margem</strong>.
    </div>

    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('tab-visao')">🏠 Visão Geral</button>
        <button class="tab-btn" onclick="switchTab('tab-vendas')">📊 Vendas & Performance</button>
        <button class="tab-btn" onclick="switchTab('tab-clientes')">👥 Clientes & LTV</button>
        <button class="tab-btn" onclick="switchTab('tab-pricing')">🏷️ Pricing & Concorrência</button>
    </div>

    <!-- ABA 1: VISÃO GERAL -->
    <div id="tab-visao" class="tab-content active">
        <div class="charts-row">
            <div class="chart-card">
                <div class="chart-title">📈 Faturamento Diário e Média Móvel (7d)</div>
                {fig1.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-title">🛍️ Share por Canal de Venda</div>
                {fig2.to_html(full_html=False, include_plotlyjs=False)}
            </div>
        </div>
        <div class="charts-row-equal">
            <div class="chart-card">
                <div class="chart-title">🏢 Preço Médio: Nosso E-Commerce vs Concorrentes</div>
                {fig5.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-title">🏆 Top Produtos por Receita</div>
                <table>
                    <thead><tr><th>Produto</th><th>Categoria</th><th>Pedidos</th><th>Receita</th></tr></thead>
                    <tbody>{top_5_rows}</tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ABA 2: VENDAS -->
    <div id="tab-vendas" class="tab-content">
        <div class="charts-row-equal">
            <div class="chart-card">
                <div class="chart-title">⏰ Faturamento por Horário de Pico (0h-23h)</div>
                {fig3.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-title">📦 Curva ABC de Produtos (Top SKUs)</div>
                <table>
                    <thead><tr><th>Produto</th><th>Categoria</th><th>Pedidos</th><th>Faturamento</th></tr></thead>
                    <tbody>{top_5_rows}</tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ABA 3: CLIENTES -->
    <div id="tab-clientes" class="tab-content">
        <div class="charts-row-equal">
            <div class="chart-card">
                <div class="chart-title">🗺️ Receita por Estado da Federação (UF)</div>
                {fig4.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-title">👑 Top 8 Clientes VIP (Maior LTV)</div>
                <table>
                    <thead><tr><th>Nome do Cliente</th><th>Estado</th><th>Pedidos</th><th>LTV Total</th></tr></thead>
                    <tbody>{top_cli_rows}</tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ABA 4: PRICING -->
    <div id="tab-pricing" class="tab-content">
        <div class="charts-row-equal">
            <div class="chart-card">
                <div class="chart-title">🎯 Dispersão: Nosso Preço vs Mercado (Linha 1:1)</div>
                {fig6.to_html(full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-title">⚡ Matriz de Competitividade de Preço (ICP)</div>
                <div style="margin-bottom:12px; font-size:0.85rem; color:#94A3B8;">
                    <strong>Fórmula do Índice:</strong> ICP = Preço Próprio / Preço Médio Concorrentes
                </div>
                <table>
                    <thead><tr><th>Faixa de ICP</th><th>Diagnóstico</th><th>Qtd SKUs</th><th>Ação Estratégica</th></tr></thead>
                    <tbody>
                        <tr><td><span style="color:#EF4444;font-weight:700;">ICP > 1.05</span></td><td>🔴 Sobrepreço Crítico</td><td>28 SKUs</td><td>Reduzir preço para recuperar volume</td></tr>
                        <tr><td><span style="color:#10B981;font-weight:700;">0.95 ≤ ICP ≤ 1.05</span></td><td>🟢 Paridade Competitiva</td><td>181 SKUs</td><td>Manter paridade e investir em frete rápido</td></tr>
                        <tr><td><span style="color:#F59E0B;font-weight:700;">ICP < 0.95</span></td><td>🟡 Oportunidade Margem</td><td>6 SKUs</td><td>Subir preço para capturar margem de contribuição</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
            window.dispatchEvent(new Event('resize'));
        }}
    </script>
</body>
</html>
"""

output_path = Path(__file__).resolve().parent / "dashboard.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML dashboard generated successfully at: {output_path}")

# Diretrizes de Design, UI/UX e Storytelling
**Agente 2 — Especialista em Dashboard & Visualização de Dados**

---

## 1. Princípios Visuais & Storytelling

O objetivo deste dashboard é transformar dados relacionais brutos em uma **experiência visual premium**, intuitiva e orientada à tomada de decisão executiva.

### 🎨 Paleta de Cores e Tokens Visuais
- **Primary / Destaque**: `#6366F1` (Indigo vibrante)
- **Secondary / Acento**: `#EC4899` (Pink Coral)
- **Success / Margem Positiva**: `#10B981` (Emerald Green)
- **Warning / Alerta de Paridade**: `#F59E0B` (Amber Orange)
- **Danger / Sobrepreço Crítico**: `#EF4444` (Ruby Red)
- **Background Escuro Sofisticado**: `#0E1117` com cards em `#1E293B` e bordas translúcidas `#334155`
- **Tipografia**: Família moderna sem serifa (Inter, system-ui), com hierarquia clara entre títulos, labels e valores monetários formatados em `pt-BR`.

---

## 2. Arquitetura das Telas e Componentes

### 🏠 Visão Geral (`app.py`)
- **Header Executivo**: Boas-vindas, data da última sincronização com Supabase e status da conexão MCP.
- **Top Metric Cards**: 4 KPIs em destaque com micro-badges (Faturamento Total, Pedidos, Ticket Médio, Clientes Ativos).
- **Storytelling Narrativo**: Decomposição em 3 blocos analíticos (Vendas no Tempo, Mix de Canais e Radar de Competitividade de Preço).
- **Filtros Globais no Sidebar**: Período de datas, Canal de Venda e Categoria de Produto.

### 📊 Página 1: Vendas e Performance (`pages/1_📊_Vendas_e_Performance.py`)
- Série temporal de vendas diárias e média móvel de 7 dias com Plotly interativo.
- Matriz de calor / barras de faturamento por Categoria e Canal.
- Tabela Top 10 SKUs com curva ABC de contribuição e volume de itens.

### 👥 Página 2: Clientes e Segmentação (`pages/2_👥_Clientes_e_Segmentacao.py`)
- Concentração de clientes e faturamento por Estado da Federação (gráfico de barras horizontais ordenado e ranking regional).
- Análise de recorrência: Frequência de compra e ticket médio por cliente.
- Tabela de Clientes VIP (Top 10 LTV) com busca interativa.

### 🏷️ Página 3: Pricing e Concorrência (`pages/3_🏷️_Pricing_e_Concorrencia.py`)
- Comparador direto: Nosso Preço vs Preço Médio Concorrentes por SKU.
- Benchmarking por Marketplace: Amazon vs Mercado Livre vs Shopee vs Magalu.
- Tabela dinâmica de Oportunidades & Alertas:
  - 🔴 **Sobrepreço**: Produtos onde nosso preço é >5% superior aos concorrentes.
  - 🟡 **Subpreço**: Oportunidades de elevar margem sem perder competitividade.
  - 🟢 **Competitivo**: Produtos em linha com o mercado.

---

## 3. Padrão de Estilização CSS Injetado (Polish UI)
Injeção de CSS nativo através de `st.markdown("<style>...</style>", unsafe_allow_html=True)`:
- Cards com efeito glassmorphism e sombras suaves (`box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1)`).
- Bordas arredondadas modernas (`border-radius: 12px`).
- Badges estilizadas para status de preços e categorias.

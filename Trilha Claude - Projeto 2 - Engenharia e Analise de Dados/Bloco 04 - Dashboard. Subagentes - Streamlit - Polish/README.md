# ⚡ E-Commerce Intelligence Dashboard — Supabase & Subagentes (Bloco 04)

Projeto completo de inteligência analítica e dashboard para e-commerce construído na **Trilha Claude - Projeto 2 (Bloco 04)**. A aplicação conecta-se diretamente ao banco de dados relacional **PostgreSQL do Supabase via MCP & PostgREST**, consumindo 4 tabelas relacionais em tempo real (`clientes`, `produtos`, `vendas`, `preco_competidores`).

O projeto foi concebido e executado por uma **equipe de 3 subagentes especialistas**:

1. **👔 Agente 1 — Líder & Executivo de Negócio (Pricing & Vendas)**
2. **🎨 Agente 2 — Especialista em Dashboard & Storytelling (UI/UX Polish)**
3. **🛡️ Agente 3 — Arquiteto de Software, Segurança & QA**

---

## 🏛️ Estrutura do Projeto

```
Bloco 04 - Dashboard. Subagentes - Streamlit - Polish/
├── .env                              <- Credenciais do Supabase (URL e API Key) [Protegido no .gitignore]
├── .env.example                      <- Template de configuração de ambiente
├── .gitignore                        <- Isolamento de segredos e caches
├── requirements.txt                  <- Dependências (Streamlit, Plotly, Pandas, Pytest, etc.)
├── README.md                         <- Documentação da solução
├── app.py                            <- Visão Executiva Geral (Overview & High-level KPIs)
├── data/
│   ├── __init__.py
│   └── supabase_client.py            <- Camada de acesso a dados com paginação e cache (@st.cache_data)
├── pages/
│   ├── 1_📊_Vendas_e_Performance.py   <- Análise temporal, sazonalidade, curva ABC de produtos
│   ├── 2_👥_Clientes_e_Segmentacao.py <- Concentração geográfica (UF) e ranking de LTV
│   └── 3_🏷️_Pricing_e_Concorrencia.py <- Matriz de competitividade vs Amazon/ML/Shopee/Magalu
├── agents/
│   ├── agente_1_business_leader.md   <- Especificação de Métricas, KPIs e Fórmulas
│   ├── agente_2_dashboard_expert.md  <- Design System, Storytelling e Wireframe
│   └── agente_3_software_architect.md<- Arquitetura, Auditoria de Segurança e QA
└── tests/
    ├── __init__.py
    ├── test_data_integrity.py        <- Testes de integridade das 4 tabelas e schemas
    ├── test_business_metrics.py      <- Validação matemática dos KPIs calculados
    └── test_security_architecture.py <- Auditoria de segurança e proteção de credenciais
```

---

## 👥 A Equipe de Subagentes e Entregas

### 👔 1. Agente Líder & Executivo de Negócio
- **Diagnóstico**: Faturamento de **R$ 974.077,28** em **3.020 transações** com **R$ 322,54 de Ticket Médio**.
- **Mix de Canais**: E-commerce lidera com **72,4%** da receita (Ticket Médio: R$ 327,37) vs Loja Física com **27,6%** (Ticket Médio: R$ 310,51).
- **Inteligência de Pricing**:
  - Catálogo próprio opera em média **3,1% acima do mercado**.
  - **Amazon** é a mais agressiva (-7,0% abaixo).
  - Identificados **28 produtos com sobrepreço crítico** (>5% acima) e **6 produtos com oportunidade de aumento de margem** (>5% abaixo).
- *Documento*: `agents/agente_1_business_leader.md`.

### 🎨 2. Agente Especialista em Dashboard & Storytelling
- Interface desenvolvida em **Streamlit + Plotly** com visual refinado (*Polish UI*).
- **Design System**: Paleta Indigo/Emerald/Pink com componentes glassmorphism e tipografia moderna.
- **3 Telas Especializadas**:
  - `app.py`: Visão Executiva Geral (Storytelling executivo, KPIs principais e visão macro).
  - `pages/1_📊_Vendas_e_Performance.py`: Tendência temporal, horários de pico e Curva ABC interativa.
  - `pages/2_👥_Clientes_e_Segmentacao.py`: Concentração regional por estado e Top 10 Clientes VIP por LTV.
  - `pages/3_🏷️_Pricing_e_Concorrencia.py`: Dispersão de preços, radar por player e tabela de ação imediata com preço sugerido.
- *Documento*: `agents/agente_2_dashboard_expert.md`.

### 🛡️ 3. Agente Arquiteto de Software, Segurança & QA
- **Camada de Dados Resiliente**: `data/supabase_client.py` com paginação automática que supera o teto de 1.000 linhas do PostgREST, recuperando todas as 3.020 vendas.
- **Segurança**: Credenciais carregadas estritamente via `.env`, sem vazamento no código nem no repositório (`.gitignore`).
- **Suíte de Testes (13 testes aprovados)**:
  - `test_data_integrity.py`: Validação de contagens, chaves primárias e schemas.
  - `test_business_metrics.py`: Validação de precisão de faturamento, canais e índices ICP.
  - `test_security_architecture.py`: Verificação de segredos e integridade de ambiente.
- *Documento*: `agents/agente_3_software_architect.md`.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos e Instalação
Certifique-se de que o Python 3.10+ está instalado:

```bash
# Na pasta do Bloco 04:
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Verifique se o arquivo `.env` está presente com as credenciais do Supabase:

```env
SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_KEY=<sua-anon-key>
```

### 3. Executar o Dashboard
Para iniciar a aplicação web:

```bash
streamlit run app.py
```
Acesse no navegador: `http://localhost:8501`.

### 4. Executar os Testes Automatizados
Para rodar a suíte completa de testes:

```bash
pytest tests/ -v
```
Resultado esperado: **13 passed**.

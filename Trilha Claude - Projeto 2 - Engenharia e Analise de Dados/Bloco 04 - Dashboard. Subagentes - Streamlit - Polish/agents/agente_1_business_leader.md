# Relatório Executivo e Definição Estratégica de Indicadores
**Agente 1 — Líder & Executivo de Negócio (Pricing & Vendas)**

---

## 1. Sumário Executivo do Negócio

A operação do e-commerce apresentou um faturamento consolidado de **R$ 974.077,28** em **3.020 transações** analisadas, movimentando **4.322 itens** entre 50 clientes cadastrados.

A distribuição de canais revela uma forte tração digital, com o **E-commerce respondendo por 72,4% da receita total** e apresentando um ticket médio superior ao canal físico.

No pilar de **Pricing**, nossa empresa opera em média com preços **3,1% superiores à média dos principais marketplaces**. A **Amazon** é a concorrente mais agressiva em preços (-7,0% em relação ao nosso catálogo), enquanto a **Magalu** posiciona-se com patamares superiores (+3,5%). Identificamos **28 SKUs com sobrepreço crítico**, demandando revisão promocional, e **6 SKUs com subpreço**, representando ganho imediato de margem de contribuição.

---

## 2. Indicadores Estratégicos de Vendas e Operação

| Indicador | Valor Atual | Definição / Fórmula | Ação Executiva Recomendada |
| :--- | :---: | :--- | :--- |
| **Receita Bruta Total** | **R$ 974.077,28** | $\sum (\text{quantidade} \times \text{preco\_unitario})$ | Consolidar meta de atingimento do 1º milhão no próximo fechamento. |
| **Volume de Pedidos** | **3.020** | $\text{COUNT(id\_venda)}$ | Monitorar taxa de conversão por canal. |
| **Ticket Médio Geral** | **R$ 322,54** | $\frac{\text{Receita Total}}{\text{Volume de Pedidos}}$ | Estimular cross-sell e combos para elevar para R$ 350,00. |
| **Ticket Médio E-commerce** | **R$ 327,37** | Receita E-commerce / Pedidos E-commerce | Canal digital com melhor rentabilidade unitária. |
| **Ticket Médio Loja Física** | **R$ 310,51** | Receita Loja Física / Pedidos Loja Física | Oportunidade de treinamento para upsell na ponta física. |
| **Itens por Pedido (IP)** | **1,43 itens** | Total Itens Vendidos (4.322) / Pedidos | Criar campanhas de frete grátis para compras com 2+ itens. |
| **Concentração Top 5 SKUs** | **40,0% da Receita** | Fone Esportivo, Camisa Social, Necessaire, Persiana, Calça Jeans | Risco de dependência de curva A. Exige reposição ágil de estoque. |

---

## 3. Matriz Estratégica de Pricing e Competitividade

Cruzando nossos preços com **728 coletas** nos concorrentes (**Amazon**, **Mercado Livre**, **Shopee** e **Magalu**):

### Comparativo por Player Concorrente:
- **Amazon**: R$ 197,73 médio (7,0% abaixo do nosso preço) $\rightarrow$ *Concorrente mais predatório*.
- **Shopee**: R$ 202,40 médio (4,8% abaixo do nosso preço) $\rightarrow$ *Forte apelo promocional*.
- **Mercado Livre**: R$ 204,94 médio (3,6% abaixo do nosso preço) $\rightarrow$ *Concorrência direta equilibrada*.
- **Magalu**: R$ 220,09 médio (3,5% acima do nosso preço) $\rightarrow$ *Oportunidade de captura de clientes Magalu*.

### Classificação dos SKUs por Índice de Competitividade de Preço (ICP):
$$\text{ICP} = \frac{\text{Preço Próprio}}{\text{Média Preço Concorrentes}}$$

1. **🔴 Sobrepreço Crítico ($\text{ICP} > 1.05$ — 28 produtos):**
   - Nossos preços estão mais de 5% acima do mercado.
   - *Risco*: Perda de buybox e migração de consumidores para Amazon/Shopee.
   - *Ação*: Ajuste fino dinâmico ou agregação de valor perceptível (brindes, garantia estendida).
2. **🟢 Paridade Competitiva ($0.95 \le \text{ICP} \le 1.05$ — 181 produtos):**
   - Preços perfeitamente alinhados com o mercado.
   - *Ação*: Foco em diferenciais de entrega rápida e excelência de atendimento.
3. **🟡 Oportunidade de Margem ($\text{ICP} < 0.95$ — 6 produtos):**
   - Estamos vendendo mais de 5% abaixo da concorrência sem necessidade.
   - *Ação*: Reajuste imediato de preços para capturar margem sem comprometer o volume de vendas.

---

## 4. Requisitos para as Telas do Dashboard (Storytelling)

- **Visão Geral (Overview)**: Painel de controle para a Diretoria, com 4 cards de KPIs essenciais, comparativo de canais e resumo de pricing.
- **Página 1 (Vendas)**: Gráficos de tendência temporal, decomposição por categoria e identificação clara da Curva ABC de produtos.
- **Página 2 (Clientes)**: Mapa/concentração por estado da federação, frequência de compra e ranking de clientes estratégicos (LTV).
- **Página 3 (Pricing)**: Tabela de alertas de ação imediata (com filtros por concorrente e categoria) e gráfico de dispersão com benchmark de mercado.

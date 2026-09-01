# Plano de Implementação: Transição para React & Frontend Patterns

Entendido! Você solicitou a utilização dos **Frontend Patterns** (baseados na skill carregada). A skill descreve padrões modernos e profissionais específicos do ecossistema React (Hooks customizados, Composition, Context API, Framer Motion, etc.).

Atualmente, nossa arquitetura estava gerando um HTML estático injetado via Python. Para aplicarmos essas melhores práticas de frontend de forma *realmente sofisticada e profissional*, precisamos separar o Backend (Analytics) do Frontend (Apresentação) e adotar o **React**.

## Open Questions

> [!WARNING]
> Decisão de Arquitetura de Frontend
> 1. **Mudança para React (Vite):** Você concorda em criarmos uma aplicação React moderna (usando Vite + TypeScript) na pasta `frontend/` em vez de gerar HTML estático?
> 2. A aplicação React consumirá o arquivo `data_payload.json` gerado pelo nosso motor de análise em Python. Isso permite implementar *Framer Motion* e *Compound Components* conforme os patterns exigidos. Podemos seguir essa via?

## Proposta de Mudanças

Se aprovado, o projeto passará a ter a seguinte divisão clara:

### 1. Backend (Data Analytics Pipeline)
- Continuamos usando os scripts em `analysis/` e `tests/` criados anteriormente.
- O arquivo `scripts/build_app.py` será alterado para exportar **apenas** o JSON (`output/data_payload.json`) e não gerar mais HTML via strings.

### 2. Frontend (React App - Nova Arquitetura)
- Criação de uma pasta `frontend/` gerada via `npx create-vite@latest dashboard --template react-ts`.
- **Implementação dos Patterns:**
  - **Composition & Compound Components:** O Design System será reescrito como componentes React reais (`<Card>`, `<CardHeader>`, etc.).
  - **Hooks Customizados:** Usaremos hooks como `useQuery` para carregar o arquivo JSON de dados de forma assíncrona.
  - **Estado (Context API):** Para gerenciar qual aba ou categoria de gráfico está sendo visualizada.
  - **Animações:** Utilização do `framer-motion` para entrada suave dos KPIs e tabelas.
  - **CSS:** Uso de CSS Modules ou TailwindCSS para injetar o *Open Design* de forma isolada e segura.

## Verification Plan

### Testes Manuais
- Executar o pipeline de dados com `python scripts/build_app.py` e validar se o arquivo JSON final tem a estrutura correta.
- Executar a aplicação React localmente com `npm run dev` e validar as animações, organização dos componentes, estados do React e tipagem do TypeScript, comprovando a aplicação rigorosa do `frontend-patterns`.

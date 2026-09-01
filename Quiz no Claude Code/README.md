# Quiz Codex — Verdadeiro ou Falso

Quiz educacional em pt-BR sobre usos, colaboração, validação, segurança e integrações do Codex. O MVP roda inteiramente no navegador e salva apenas a rodada ativa em `sessionStorage`.

## Requisitos

- Node.js 22.13 ou superior
- npm

## Desenvolvimento

```bash
npm install
npm run dev
```

Comandos de qualidade:

```bash
npm run lint
npm test
npm run build
```

## Organização

- `app/`: entrada, metadados e estilos globais.
- `src/components/`: fluxo visual e estados da experiência.
- `src/data/`: banco de perguntas.
- `src/lib/`: sorteio, pontuação, validação e persistência.
- `src/types/`: contratos TypeScript do quiz.
- `tests/`: testes unitários e de componentes.

## Adicionar ou revisar perguntas

Edite `src/data/questions.ts` e preserve o tipo `QuizQuestion`. Use um ID único, estável e legível, como `advanced-security-011`. Toda pergunta precisa de `difficulty`, `topic`, afirmação sem ambiguidade, resposta, explicação, `reviewedAt` no formato `YYYY-MM-DD` e estado `active`.

Inclua `sourceUrl` oficial quando a afirmação depender de capacidades, disponibilidade ou comportamento atual do Codex. Mantenha pelo menos dez perguntas ativas por nível e equilíbrio próximo de 50% entre verdadeiro e falso. Execute `npm test` após qualquer alteração editorial.

## Limites do MVP

Não há backend, contas, ranking, analytics externo ou integração com a API da OpenAI. Este é um recurso educacional independente e não substitui a documentação oficial.


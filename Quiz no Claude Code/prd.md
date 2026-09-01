# PRD — Quiz Codex: Verdadeiro ou Falso

**Status:** pronto para implementação do MVP  
**Versão:** 1.0  
**Idioma do produto:** português do Brasil (pt-BR)  
**Última revisão do PRD:** 10 de agosto de 2026

## 1. Visão do produto

Criar uma experiência web curta e envolvente que ensine o que é Codex, onde ele gera valor, como trabalhar bem com ele e quais cuidados técnicos e humanos continuam necessários.

O produto será um quiz de afirmações “Verdadeiro ou Falso”, com três níveis de dificuldade, feedback educativo imediato e resultado final. Ele deve servir tanto para uma pessoa de negócios que está tendo o primeiro contato com Codex quanto para profissionais técnicos que desejam testar conhecimentos sobre contexto, validação, permissões, sandbox, skills, plugins e integrações.

O MVP não é uma prova de certificação nem uma landing page promocional. É uma ferramenta de aprendizagem rápida, adequada para onboarding, workshops, demonstrações e estudo individual.

## 2. Problema e oportunidade

Codex reúne conceitos de produto, engenharia, agentes, segurança e colaboração. Isso cria três problemas recorrentes:

1. Pessoas não técnicas podem não enxergar aplicações além de “gerar código”.
2. Usuários intermediários podem não fornecer contexto ou critérios de aceite suficientes.
3. Usuários avançados podem subestimar revisão, testes, permissões e diferenças entre ambientes.

Um quiz curto reduz a barreira de entrada e permite corrigir modelos mentais no momento da resposta. O valor pedagógico está menos em marcar certo ou errado e mais em explicar por que a afirmação é verdadeira ou falsa.

## 3. Evidência e base conceitual

A documentação oficial da OpenAI descreve Codex como um agente de desenvolvimento capaz de ajudar a entender codebases, construir e testar funcionalidades, corrigir bugs e revisar mudanças. Ela também apresenta diferentes superfícies e conceitos relacionados, como aplicativo desktop, web, CLI, extensão de IDE, cloud, permissões, skills e plugins.

Referências editoriais iniciais:

- [OpenAI Developers — visão geral e casos de uso](https://developers.openai.com/)
- [OpenAI Developers — casos de uso do Codex](https://developers.openai.com/codex/use-cases)

Como o produto Codex evolui, toda afirmação sobre disponibilidade, planos, modelos, interfaces ou capacidades específicas deve possuir fonte oficial e data de revisão. O quiz não deve apresentar como universal algo que dependa de conta, plano, plataforma, versão ou configuração.

## 4. Objetivos de negócio

- Aumentar a alfabetização sobre Codex entre públicos técnicos e não técnicos.
- Reduzir falsas expectativas sobre autonomia, precisão e necessidade de revisão.
- Criar um ativo reutilizável para onboarding, workshops e demonstrações internas.
- Tornar simples e seguro atualizar o conteúdo conforme Codex evolui.
- Validar interesse antes de investir em login, backend, analytics externo ou certificação.

## 5. Objetivos do usuário

- Entender rapidamente o que Codex pode fazer e onde ele agrega valor.
- Identificar boas práticas para especificar e acompanhar uma tarefa.
- Reconhecer limites, riscos e responsabilidades humanas.
- Receber uma explicação útil depois de cada tentativa.
- Saber quais temas precisa revisar ao terminar.

## 6. Não objetivos do MVP

- Certificar oficialmente conhecimento sobre Codex.
- Substituir a documentação oficial da OpenAI.
- Cobrir todas as funcionalidades, planos ou modelos existentes.
- Oferecer login, ranking global, multiplayer ou painel administrativo.
- Gerar perguntas por IA ou integrar a API da OpenAI.
- Coletar dados pessoais ou resultados em um servidor.
- Criar uma página institucional extensa antes do quiz.

## 7. Público-alvo e trilhas

### Iniciante — negócios

Lideranças, produto, vendas, operações e pessoas curiosas. Precisam compreender valor, casos de uso, limites e colaboração, sem depender de conhecimento de programação.

### Intermediário — colaboração com tecnologia

PMs, designers, analistas, QA, líderes técnicos e desenvolvedores iniciantes. Precisam entender contexto, decomposição de tarefas, critérios de aceite, iteração e validação.

### Avançado — uso técnico responsável

Desenvolvedores, arquitetos, DevOps e segurança. Precisam raciocinar sobre ambientes, permissões, sandbox, ferramentas, skills, plugins, MCP, testes e risco operacional.

## 8. Resultado do brainstorming

### Hipóteses priorizadas

- Verdadeiro/falso é adequado para sessões rápidas, desde que as frases não sejam ambíguas.
- Feedback imediato ensina melhor do que mostrar apenas o gabarito no final.
- Separar por nível reduz intimidação e melhora a relevância.
- Dez perguntas oferecem uma sessão de aproximadamente 3 a 7 minutos.
- Um placar por tema é mais educativo do que apenas um percentual geral.
- Fontes e datas de revisão reduzem o risco de conteúdo desatualizado.

### Decisões de MVP

- Uma rodada contém 10 perguntas do nível escolhido, ou todas se houver menos de 10.
- A ordem das perguntas é embaralhada a cada rodada.
- O usuário responde uma pergunta por vez e não pode mudar a resposta depois de confirmada.
- O feedback é exibido antes de avançar.
- Não haverá temporizador; o foco é aprendizagem, não pressão.
- Não haverá modo misto no MVP.
- Não haverá backend ou analytics externo.
- O progresso da rodada será salvo em `sessionStorage` para tolerar recarregamento acidental.
- O resultado final mostrará desempenho geral, por tema e revisão das respostas.
- Links para fontes oficiais aparecerão no feedback quando disponíveis e serão abertos em nova aba.

### Princípios de experiência

- Começar rápido: no máximo uma escolha e um clique antes da primeira pergunta.
- Ensinar sem punir: erro deve produzir explicação, não constrangimento.
- Ser preciso: evitar pegadinhas, absolutos frágeis e frases dependentes de versão.
- Ser acessível: toda interação deve funcionar com teclado e leitor de tela.
- Ser transparente: deixar claro que o conteúdo é educacional e possui data de revisão.

## 9. Escopo funcional

### RF-01 — Tela inicial

A tela inicial deve conter:

- nome e proposta do quiz em até duas frases;
- três cartões de nível com descrição do público e dos temas;
- seleção de nível;
- botão “Começar quiz”;
- indicação de quantidade de perguntas e duração estimada;
- data da última revisão do conteúdo.

O botão deve permanecer desabilitado até a escolha de um nível.

### RF-02 — Preparação da rodada

Ao iniciar, o sistema deve:

1. filtrar perguntas ativas pelo nível selecionado;
2. embaralhar sem mutar a coleção original;
3. selecionar até 10 perguntas;
4. inicializar respostas, pontuação e progresso;
5. persistir o estado da rodada em `sessionStorage`.

### RF-03 — Resposta

- Exibir uma afirmação por vez.
- Oferecer exatamente dois botões: “Verdadeiro” e “Falso”.
- Permitir seleção pelas teclas `V` e `F`, sem impedir o uso normal de tecnologias assistivas.
- Após uma escolha, bloquear nova resposta para a pergunta atual.
- Não depender somente de cor para comunicar o estado.

### RF-04 — Feedback imediato

Após a resposta, exibir:

- “Você acertou” ou “Você errou”;
- resposta correta em texto;
- explicação de 1 a 3 frases;
- tema da pergunta;
- link “Consultar fonte oficial”, quando houver;
- botão “Próxima pergunta” ou “Ver resultado” na última questão.

### RF-05 — Progresso

Durante a rodada, exibir:

- “Pergunta X de Y”;
- barra de progresso;
- total de acertos até o momento;
- nível atual;
- ação “Sair do quiz”.

Ao sair, pedir confirmação porque o progresso será descartado.

### RF-06 — Recuperação de sessão

Se a página for recarregada durante uma rodada válida, restaurar pergunta atual, ordem, respostas e pontuação. Ao concluir, abandonar ou iniciar uma nova rodada, remover o estado anterior.

Se o estado persistido for inválido ou incompatível com a versão do conteúdo, descartá-lo silenciosamente e voltar à tela inicial.

### RF-07 — Resultado final

Exibir:

- acertos e total;
- percentual arredondado;
- faixa de desempenho;
- resumo de acertos por tema;
- lista de todas as afirmações, resposta do usuário, resposta correta e explicação;
- botão “Jogar novamente”; 
- botão “Escolher outro nível”.

Faixas de desempenho:

| Percentual | Mensagem |
|---|---|
| 0–49% | “Bom começo — revise as explicações e tente novamente.” |
| 50–79% | “Você já tem uma boa base sobre Codex.” |
| 80–99% | “Ótimo domínio — faltou pouco para fechar a rodada.” |
| 100% | “Excelente — você dominou esta rodada.” |

### RF-08 — Estado vazio e falhas

- Se um nível não tiver perguntas válidas, impedir o início e mostrar mensagem amigável.
- Um link de fonte inválido não pode quebrar o quiz.
- Dados inválidos devem ser detectados em desenvolvimento por validação e testes.

## 10. Conteúdo e política editorial

### Cobertura mínima do MVP

O banco deve conter no mínimo 30 perguntas: 10 por nível. Em cada nível, buscar equilíbrio próximo de 50% entre respostas verdadeiras e falsas e evitar mais de três respostas iguais em sequência depois do embaralhamento, quando possível.

Temas mínimos:

- `valor-e-casos-de-uso`
- `contexto-e-especificacao`
- `workflow-e-colaboracao`
- `testes-e-revisao`
- `seguranca-e-permissoes`
- `ferramentas-e-integracoes`

### Regras de escrita

- Cada afirmação deve testar um conceito principal.
- Evitar dupla negação, ironia e formulações deliberadamente enganosas.
- Evitar “sempre”, “nunca”, “garantido” e “qualquer”, exceto quando o absoluto for o conceito testado.
- Definir termos técnicos na explicação quando aparecerem pela primeira vez no nível.
- Não confundir Codex, ChatGPT, API da OpenAI e modelos Codex.
- Não afirmar disponibilidade comercial sem fonte oficial atual.
- Explicações devem ensinar a regra geral e, quando necessário, citar a condição ou exceção.
- Toda pergunta deve possuir `reviewedAt`; fatos de produto devem possuir `sourceUrl` oficial.

### Perguntas-semente

As perguntas abaixo orientam o tom; a implementação deve completar e revisar o conjunto mínimo.

#### Iniciante

1. “Codex pode ajudar a entender uma base de código existente.” — **Verdadeiro**.
2. “Codex serve apenas para criar projetos do zero.” — **Falso**.
3. “Uma entrega gerada por Codex dispensa revisão humana.” — **Falso**.
4. “Objetivo, contexto e critérios de sucesso ajudam Codex a executar melhor uma tarefa.” — **Verdadeiro**.
5. “Pessoas de negócios podem usar Codex para transformar uma ideia em requisitos mais claros.” — **Verdadeiro**.

#### Intermediário

1. “Ler padrões e instruções do repositório antes de editar reduz desalinhamento.” — **Verdadeiro**.
2. “Se o código compilou, testes e revisão são desnecessários.” — **Falso**.
3. “Dividir uma tarefa grande em entregas verificáveis pode facilitar controle e feedback.” — **Verdadeiro**.
4. “Logs de erro e resultados de testes são contexto útil para uma nova iteração.” — **Verdadeiro**.
5. “Pedir ‘melhore isso’ é tão verificável quanto fornecer critérios de aceite.” — **Falso**.

#### Avançado

1. “Sandbox e permissões ajudam a limitar acessos e comandos disponíveis ao agente.” — **Verdadeiro**.
2. “Conceder acesso amplo a ferramentas externas elimina a necessidade de avaliar riscos.” — **Falso**.
3. “Ambientes local e cloud podem diferir em arquivos, dependências e acesso à rede.” — **Verdadeiro**.
4. “Skills podem encapsular instruções e fluxos repetíveis.” — **Verdadeiro**.
5. “Mais contexto elimina a necessidade de uma especificação clara.” — **Falso**.

## 11. Modelo de dados

```ts
export type Difficulty = "beginner" | "intermediate" | "advanced";

export type Topic =
  | "valor-e-casos-de-uso"
  | "contexto-e-especificacao"
  | "workflow-e-colaboracao"
  | "testes-e-revisao"
  | "seguranca-e-permissoes"
  | "ferramentas-e-integracoes";

export interface QuizQuestion {
  id: string;
  difficulty: Difficulty;
  topic: Topic;
  statement: string;
  answer: boolean;
  explanation: string;
  sourceUrl?: string;
  reviewedAt: string; // ISO 8601: YYYY-MM-DD
  active: boolean;
}

export interface QuizAnswer {
  questionId: string;
  selectedAnswer: boolean;
  isCorrect: boolean;
  answeredAt: string;
}

export interface QuizSession {
  schemaVersion: 1;
  difficulty: Difficulty;
  questionIds: string[];
  currentIndex: number;
  answers: QuizAnswer[];
  startedAt: string;
}
```

IDs devem ser únicos, estáveis e legíveis, por exemplo `beginner-use-case-001`.

## 12. Fluxos e estados

Fluxo principal:

```text
Início → escolher nível → responder → ver feedback
                              ↑             ↓
                              └── próxima ──┘
                                            ↓
                                      resultado
                                      ↙       ↘
                              jogar de novo   trocar nível
```

Máquina de estados recomendada:

- `start`: nenhum quiz ativo;
- `question`: aguardando resposta;
- `feedback`: resposta registrada;
- `results`: rodada concluída.

As transições devem ser explícitas e testáveis. Não usar o texto do botão ou estados visuais como fonte de verdade da lógica.

## 13. Direção visual

- Aparência moderna, limpa e editorial, com foco no cartão da pergunta.
- Evitar estética infantil, excesso de gamificação ou landing page promocional.
- Fundo neutro, tipografia de alta legibilidade e uma cor de destaque.
- Estados correto e incorreto devem combinar cor, ícone e texto.
- Botões “Verdadeiro” e “Falso” grandes, equivalentes e confortáveis no mobile.
- Largura de leitura do conteúdo principal entre aproximadamente 640 e 760 px.
- Animações discretas e desativáveis por `prefers-reduced-motion`.
- Não utilizar o logotipo da OpenAI de forma que sugira produto oficial.

## 14. Acessibilidade

Meta: WCAG 2.2 nível AA para o fluxo principal.

- HTML semântico e hierarquia correta de títulos.
- Navegação completa por teclado e foco sempre visível.
- Contraste mínimo adequado para texto e controles.
- Região `aria-live` educada para feedback e mudança de questão.
- Barra de progresso com nome, valor atual e total acessíveis.
- Foco movido de forma previsível para o feedback após responder e para a afirmação ao avançar.
- Ícones decorativos ocultos de leitores de tela.
- Áreas clicáveis com pelo menos 44 × 44 px.
- Layout utilizável a partir de 320 px de largura e com zoom de 200%.

## 15. Arquitetura técnica

### Stack definida

- React 19 + TypeScript.
- Vite.
- CSS Modules ou CSS puro com variáveis de design; não adicionar biblioteca de UI no MVP.
- Vitest + React Testing Library.
- ESLint e TypeScript em modo estrito.
- Sem backend e sem chamadas à API da OpenAI.

Se o repositório já possuir versões ou convenções diferentes quando a implementação começar, preservar o que existe e documentar qualquer desvio justificável.

### Estrutura sugerida

```text
src/
  app/
    App.tsx
  components/
    StartScreen.tsx
    QuizScreen.tsx
    FeedbackPanel.tsx
    ResultsScreen.tsx
    ProgressBar.tsx
  data/
    questions.ts
  hooks/
    useQuiz.ts
  lib/
    quiz.ts
    sessionStorage.ts
    validateQuestions.ts
  types/
    quiz.ts
  styles/
    global.css
  main.tsx
```

### Regras de implementação

- Manter dados de perguntas separados de componentes e regras de negócio.
- Usar uma função de embaralhamento testável, preferencialmente Fisher–Yates sobre uma cópia.
- Permitir injeção de aleatoriedade nos testes para resultados determinísticos.
- Derivar pontuação das respostas registradas, evitando estados duplicados.
- Validar IDs, datas, URLs, campos obrigatórios e duplicidades durante testes ou inicialização em desenvolvimento.
- Isolar leitura e escrita de `sessionStorage` e tratar JSON corrompido.
- Links externos devem usar `rel="noreferrer noopener"`.
- Não incluir segredos, chaves ou dependências de rede.

## 16. Requisitos não funcionais

- Build de produção sem erros ou warnings relevantes.
- Primeira carga utilizável em conexão móvel comum; bundle inicial desejável abaixo de 250 KB gzip.
- Lighthouse desejável: pelo menos 90 em Performance, Accessibility, Best Practices e SEO em desktop.
- Compatibilidade com as duas versões estáveis mais recentes de Chrome, Edge, Firefox e Safari.
- Sem erros no console no fluxo principal.
- Interface responsiva entre 320 px e 1440 px ou mais.
- Conteúdo e interface totalmente em pt-BR.

## 17. Plano de testes

### Testes unitários obrigatórios

- filtro por dificuldade e `active`;
- embaralhamento sem mutação;
- limite de 10 perguntas;
- cálculo de acertos, percentual, faixa e resultado por tema;
- rejeição de IDs duplicados e perguntas inválidas;
- serialização, restauração e descarte de sessão inválida.

### Testes de componentes obrigatórios

- botão inicial desabilitado sem nível selecionado;
- resposta aceita apenas uma vez;
- feedback correto para acerto e erro;
- avanço até o resultado;
- reinício e troca de nível;
- estados e nomes acessíveis dos controles principais.

### Validação manual

- fluxo completo nos três níveis;
- teclado sem mouse;
- viewport móvel de 320 px;
- reload no meio da sessão;
- `prefers-reduced-motion`;
- links de fonte em nova aba;
- ausência de dependência exclusiva de cor.

## 18. Critérios de aceite do MVP

- [ ] Usuário escolhe entre Iniciante, Intermediário e Avançado.
- [ ] Cada nível possui pelo menos 10 perguntas válidas e ativas.
- [ ] Cada rodada apresenta até 10 perguntas embaralhadas.
- [ ] Cada pergunta aceita apenas Verdadeiro ou Falso e somente uma resposta.
- [ ] Feedback imediato informa resultado, resposta correta e explicação.
- [ ] Progresso e pontuação parcial são visíveis e acessíveis.
- [ ] Reload restaura uma rodada em andamento.
- [ ] Resultado mostra percentual, faixa, desempenho por tema e revisão completa.
- [ ] Usuário pode repetir o nível ou escolher outro.
- [ ] O fluxo principal funciona por teclado e em 320 px de largura.
- [ ] Perguntas e lógica ficam desacopladas.
- [ ] Testes obrigatórios passam.
- [ ] `npm run build` conclui sem erros.
- [ ] README explica instalação, execução, testes, build e como adicionar perguntas.

## 19. Métricas e validação do produto

Como o MVP não terá analytics externo, a primeira validação será feita em sessões observadas ou formulário separado.

Indicadores desejados:

- pelo menos 70% das pessoas iniciam uma rodada após abrir o produto;
- pelo menos 75% concluem a rodada iniciada;
- tempo mediano entre 3 e 7 minutos;
- pelo menos 80% respondem que entenderam melhor um uso ou limite de Codex;
- nenhuma pergunta recebe relato recorrente de ambiguidade por mais de 10% dos participantes;
- uma nova pergunta pode ser adicionada sem alterar componentes ou lógica.

Instrumentação futura, se aprovada, deve registrar apenas eventos agregados como início, conclusão, nível e faixa de resultado, sem armazenar respostas individualizadas ou identificadores pessoais por padrão.

## 20. Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Conteúdo ficar desatualizado | Ensinar informação incorreta | `sourceUrl`, `reviewedAt` e revisão editorial periódica |
| Frases ambíguas ou com pegadinha | Frustração e baixa confiança | Uma ideia por questão, revisão humana e teste com usuários |
| Quiz superficial para técnicos | Baixa relevância no avançado | Cobrir segurança, ambientes, permissões, skills, plugins e validação |
| Jargão afastar iniciantes | Abandono | Definições simples e trilhas separadas |
| Aleatoriedade gerar sequência ruim | Sensação de repetição | Balancear banco e reduzir sequências iguais quando possível |
| Marca sugerir produto oficial | Risco reputacional | Identidade própria e aviso educacional independente |
| Persistência corrompida | Fluxo bloqueado | Versionar schema, validar e limpar estado inválido |

## 21. Roadmap posterior ao MVP

Prioridade sugerida:

1. Modo misto e filtros por tema.
2. Histórico local e recomendações de revisão.
3. Compartilhamento de resultado sem expor respostas pessoais.
4. Modo apresentação para workshops.
5. Importação validada de perguntas via JSON.
6. Analytics com consentimento e política de privacidade.
7. Internacionalização.
8. Backend, contas e painel editorial somente após validação de demanda.

## 22. Questões para a próxima rodada de descoberta

Estas questões não bloqueiam o MVP, mas devem orientar entrevistas e evolução:

- O principal canal será onboarding interno, evento, treinamento pago ou acesso público?
- Existe identidade visual ou marca que a interface deve seguir?
- Quem será responsável por revisar o conteúdo e com qual frequência?
- O resultado precisa ser compartilhável ou certificado?
- Há necessidade de linguagem inclusiva ou terminologia interna específica?
- Métricas reais justificam login, backend ou painel editorial?

## 23. Definition of Done

O MVP estará concluído quando todos os critérios de aceite estiverem atendidos, os testes passarem, a aplicação tiver sido revisada em desktop e mobile, o conteúdo tiver sido conferido contra fontes oficiais e o README permitir que outra pessoa execute e mantenha o projeto sem orientação adicional.

## 24. Instrução de implementação para Codex

```text
Implemente o MVP definido neste prd.md.

Antes de editar, inspecione o repositório e preserve convenções existentes. Se ainda não houver aplicação, inicialize React + TypeScript + Vite. Construa primeiro o fluxo funcional completo (início, pergunta, feedback e resultado), depois aplique o acabamento visual e acessibilidade.

Mantenha perguntas em dados tipados e independentes dos componentes. Inclua no mínimo 10 perguntas revisadas por nível, com equilíbrio entre verdadeiro e falso, fontes oficiais quando a afirmação depender do produto e datas de revisão. Não invente funcionalidades do Codex; valide fatos mutáveis na documentação oficial da OpenAI.

Implemente persistência resiliente em sessionStorage, testes obrigatórios, layout responsivo e navegação por teclado. Não adicione backend, autenticação, analytics externo, biblioteca de UI ou integração com a API da OpenAI.

Ao final, execute lint, testes e build; corrija falhas; faça uma revisão visual do fluxo principal em desktop e mobile; atualize o README com comandos e instruções para adicionar perguntas; e relate decisões ou desvios do PRD.
```

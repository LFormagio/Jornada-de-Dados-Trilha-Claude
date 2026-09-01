import type {
  Difficulty,
  QuizAnswer,
  QuizQuestion,
  Topic,
} from "@/src/types/quiz";

export const MAX_QUESTIONS = 10;

export function shuffleQuestions(
  questions: QuizQuestion[],
  random: () => number = Math.random,
): QuizQuestion[] {
  const copy = [...questions];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const target = Math.floor(random() * (index + 1));
    [copy[index], copy[target]] = [copy[target], copy[index]];
  }

  for (let index = 3; index < copy.length; index += 1) {
    const answer = copy[index].answer;
    const createsRun = copy.slice(index - 3, index).every((item) => item.answer === answer);
    if (!createsRun) continue;
    const replacement = copy.findIndex(
      (item, candidate) => candidate > index && item.answer !== answer,
    );
    if (replacement > -1) {
      [copy[index], copy[replacement]] = [copy[replacement], copy[index]];
    }
  }
  return copy;
}

export function createRound(
  questions: QuizQuestion[],
  difficulty: Difficulty,
  random: () => number = Math.random,
): QuizQuestion[] {
  return shuffleQuestions(
    questions.filter((question) => question.active && question.difficulty === difficulty),
    random,
  ).slice(0, MAX_QUESTIONS);
}

export function scoreAnswers(answers: QuizAnswer[]) {
  const correct = answers.filter((answer) => answer.isCorrect).length;
  const total = answers.length;
  const percentage = total === 0 ? 0 : Math.round((correct / total) * 100);
  return { correct, total, percentage };
}

export function performanceMessage(percentage: number): string {
  if (percentage === 100) return "Excelente — você dominou esta rodada.";
  if (percentage >= 80) return "Ótimo domínio — faltou pouco para fechar a rodada.";
  if (percentage >= 50) return "Você já tem uma boa base sobre Codex.";
  return "Bom começo — revise as explicações e tente novamente.";
}

export function scoreByTopic(questions: QuizQuestion[], answers: QuizAnswer[]) {
  const answerMap = new Map(answers.map((answer) => [answer.questionId, answer]));
  return questions.reduce<Partial<Record<Topic, { correct: number; total: number }>>>(
    (summary, question) => {
      const answer = answerMap.get(question.id);
      if (!answer) return summary;
      const current = summary[question.topic] ?? { correct: 0, total: 0 };
      summary[question.topic] = {
        correct: current.correct + (answer.isCorrect ? 1 : 0),
        total: current.total + 1,
      };
      return summary;
    },
    {},
  );
}

export function validateQuestions(questions: QuizQuestion[]): string[] {
  const errors: string[] = [];
  const ids = new Set<string>();
  const difficulties: Difficulty[] = ["beginner", "intermediate", "advanced"];
  const topics: Topic[] = [
    "valor-e-casos-de-uso",
    "contexto-e-especificacao",
    "workflow-e-colaboracao",
    "testes-e-revisao",
    "seguranca-e-permissoes",
    "ferramentas-e-integracoes",
  ];

  questions.forEach((question, index) => {
    const label = question.id || `posição ${index + 1}`;
    if (!question.id || ids.has(question.id)) errors.push(`ID ausente ou duplicado: ${label}`);
    ids.add(question.id);
    if (!difficulties.includes(question.difficulty)) errors.push(`Dificuldade inválida: ${label}`);
    if (!topics.includes(question.topic)) errors.push(`Tema inválido: ${label}`);
    if (!question.statement.trim() || !question.explanation.trim()) errors.push(`Texto incompleto: ${label}`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(question.reviewedAt)) errors.push(`Data inválida: ${label}`);
    if (question.sourceUrl) {
      try {
        const url = new URL(question.sourceUrl);
        if (url.protocol !== "https:") errors.push(`URL insegura: ${label}`);
      } catch {
        errors.push(`URL inválida: ${label}`);
      }
    }
  });
  return errors;
}


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
  reviewedAt: string;
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

export type QuizStage = "start" | "question" | "feedback" | "results";


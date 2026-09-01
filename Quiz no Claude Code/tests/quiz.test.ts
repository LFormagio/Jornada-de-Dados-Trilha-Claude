import { describe, expect, it } from "vitest";
import { questions } from "@/src/data/questions";
import {
  createRound,
  performanceMessage,
  scoreAnswers,
  scoreByTopic,
  shuffleQuestions,
  validateQuestions,
} from "@/src/lib/quiz";

describe("conteúdo e preparação da rodada", () => {
  it("mantém 10 perguntas válidas por nível", () => {
    expect(validateQuestions(questions)).toEqual([]);
    for (const difficulty of ["beginner", "intermediate", "advanced"] as const) {
      expect(questions.filter((question) => question.difficulty === difficulty && question.active)).toHaveLength(10);
      expect(createRound(questions, difficulty, () => 0.4)).toHaveLength(10);
    }
  });

  it("embaralha sem mutar a coleção original", () => {
    const original = [...questions];
    const shuffled = shuffleQuestions(questions, () => 0);
    expect(questions).toEqual(original);
    expect(shuffled).not.toBe(questions);
    expect(shuffled.map((item) => item.id).sort()).toEqual(original.map((item) => item.id).sort());
  });

  it("filtra por dificuldade e perguntas ativas", () => {
    const inactive = { ...questions[0], active: false };
    const round = createRound([inactive, ...questions.slice(1)], "beginner", () => 0.5);
    expect(round).toHaveLength(9);
    expect(round.every((question) => question.difficulty === "beginner" && question.active)).toBe(true);
  });
});

describe("pontuação", () => {
  const answers = [
    { questionId: questions[0].id, selectedAnswer: true, isCorrect: true, answeredAt: "2026-08-10T12:00:00Z" },
    { questionId: questions[1].id, selectedAnswer: true, isCorrect: false, answeredAt: "2026-08-10T12:01:00Z" },
  ];

  it("calcula total, percentual e faixa", () => {
    expect(scoreAnswers(answers)).toEqual({ correct: 1, total: 2, percentage: 50 });
    expect(performanceMessage(49)).toContain("Bom começo");
    expect(performanceMessage(50)).toContain("boa base");
    expect(performanceMessage(80)).toContain("Ótimo domínio");
    expect(performanceMessage(100)).toContain("Excelente");
  });

  it("resume o resultado por tema", () => {
    expect(scoreByTopic(questions.slice(0, 2), answers)["valor-e-casos-de-uso"]).toEqual({ correct: 1, total: 2 });
  });
});


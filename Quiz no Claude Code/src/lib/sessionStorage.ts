import type { Difficulty, QuizAnswer, QuizSession } from "@/src/types/quiz";

export const SESSION_KEY = "quiz-codex-session";

const difficulties: Difficulty[] = ["beginner", "intermediate", "advanced"];

export function parseSession(raw: string | null, validIds: Set<string>): QuizSession | null {
  if (!raw) return null;
  try {
    const value = JSON.parse(raw) as Partial<QuizSession>;
    if (
      value.schemaVersion !== 1 ||
      !value.difficulty ||
      !difficulties.includes(value.difficulty) ||
      !Array.isArray(value.questionIds) ||
      value.questionIds.length === 0 ||
      value.questionIds.length > 10 ||
      new Set(value.questionIds).size !== value.questionIds.length ||
      value.questionIds.some((id) => typeof id !== "string" || !validIds.has(id)) ||
      !Number.isInteger(value.currentIndex) ||
      value.currentIndex! < 0 ||
      value.currentIndex! >= value.questionIds.length ||
      !Array.isArray(value.answers) ||
      value.answers.length > value.questionIds.length ||
      typeof value.startedAt !== "string"
    ) {
      return null;
    }
    const answersValid = value.answers.every((answer: QuizAnswer) =>
      value.questionIds!.includes(answer.questionId) &&
      typeof answer.selectedAnswer === "boolean" &&
      typeof answer.isCorrect === "boolean" &&
      typeof answer.answeredAt === "string",
    );
    return answersValid ? (value as QuizSession) : null;
  } catch {
    return null;
  }
}

export function loadSession(validIds: Set<string>): QuizSession | null {
  if (typeof window === "undefined") return null;
  const session = parseSession(window.sessionStorage.getItem(SESSION_KEY), validIds);
  if (!session) window.sessionStorage.removeItem(SESSION_KEY);
  return session;
}

export function saveSession(session: QuizSession): void {
  if (typeof window !== "undefined") {
    window.sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
}

export function clearSession(): void {
  if (typeof window !== "undefined") window.sessionStorage.removeItem(SESSION_KEY);
}


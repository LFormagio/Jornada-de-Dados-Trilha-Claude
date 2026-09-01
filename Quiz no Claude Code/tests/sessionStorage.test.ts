import { describe, expect, it } from "vitest";
import { parseSession } from "@/src/lib/sessionStorage";

const validIds = new Set(["question-1"]);
const valid = {
  schemaVersion: 1,
  difficulty: "beginner",
  questionIds: ["question-1"],
  currentIndex: 0,
  answers: [],
  startedAt: "2026-08-10T12:00:00Z",
};

describe("sessão persistida", () => {
  it("restaura uma sessão válida", () => {
    expect(parseSession(JSON.stringify(valid), validIds)).toEqual(valid);
  });

  it("descarta JSON corrompido, versão e IDs inválidos", () => {
    expect(parseSession("{", validIds)).toBeNull();
    expect(parseSession(JSON.stringify({ ...valid, schemaVersion: 2 }), validIds)).toBeNull();
    expect(parseSession(JSON.stringify({ ...valid, questionIds: ["missing"] }), validIds)).toBeNull();
  });
});


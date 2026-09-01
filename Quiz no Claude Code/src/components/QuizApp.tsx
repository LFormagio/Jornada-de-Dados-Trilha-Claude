"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { questions } from "@/src/data/questions";
import {
  createRound,
  performanceMessage,
  scoreAnswers,
  scoreByTopic,
  validateQuestions,
} from "@/src/lib/quiz";
import {
  clearSession,
  loadSession,
  saveSession,
} from "@/src/lib/sessionStorage";
import type {
  Difficulty,
  QuizAnswer,
  QuizQuestion,
  QuizSession,
  QuizStage,
  Topic,
} from "@/src/types/quiz";

const levels: Array<{ id: Difficulty; name: string; audience: string }> = [
  { id: "beginner", name: "Iniciante", audience: "Valor, possibilidades e limites essenciais" },
  { id: "intermediate", name: "Intermediário", audience: "Contexto, colaboração e validação" },
  { id: "advanced", name: "Avançado", audience: "Segurança, ambientes e integrações" },
];

const topicLabels: Record<Topic, string> = {
  "valor-e-casos-de-uso": "Valor e casos de uso",
  "contexto-e-especificacao": "Contexto e especificação",
  "workflow-e-colaboracao": "Workflow e colaboração",
  "testes-e-revisao": "Testes e revisão",
  "seguranca-e-permissoes": "Segurança e permissões",
  "ferramentas-e-integracoes": "Ferramentas e integrações",
};

function sessionQuestions(session: QuizSession | null): QuizQuestion[] {
  if (!session) return [];
  const byId = new Map(questions.map((question) => [question.id, question]));
  return session.questionIds.flatMap((id) => {
    const question = byId.get(id);
    return question ? [question] : [];
  });
}

export function QuizApp() {
  const [selectedLevel, setSelectedLevel] = useState<Difficulty | null>(null);
  const [session, setSession] = useState<QuizSession | null>(null);
  const [stage, setStage] = useState<QuizStage>("start");
  const [ready, setReady] = useState(false);
  const statementRef = useRef<HTMLHeadingElement>(null);
  const feedbackRef = useRef<HTMLDivElement>(null);
  const dataErrors = useMemo(() => validateQuestions(questions), []);
  const round = useMemo(() => sessionQuestions(session), [session]);
  const currentQuestion = session ? round[session.currentIndex] : undefined;
  const currentAnswer = currentQuestion
    ? session?.answers.find((answer) => answer.questionId === currentQuestion.id)
    : undefined;

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (!active) return;
      const restored = loadSession(new Set(questions.map((question) => question.id)));
      if (restored) {
        setSession(restored);
        setSelectedLevel(restored.difficulty);
        setStage(restored.answers.some((answer) => answer.questionId === restored.questionIds[restored.currentIndex]) ? "feedback" : "question");
      }
      setReady(true);
    });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (stage === "feedback") feedbackRef.current?.focus();
    if (stage === "question") statementRef.current?.focus();
  }, [stage, session?.currentIndex]);

  useEffect(() => {
    if (stage !== "question" || !currentQuestion) return;
    const handleKey = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement;
      if (["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName)) return;
      if (event.key.toLowerCase() === "v") answer(true);
      if (event.key.toLowerCase() === "f") answer(false);
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  });

  function startQuiz(level: Difficulty = selectedLevel!) {
    const selectedQuestions = createRound(questions, level);
    if (!selectedQuestions.length) return;
    const nextSession: QuizSession = {
      schemaVersion: 1,
      difficulty: level,
      questionIds: selectedQuestions.map((question) => question.id),
      currentIndex: 0,
      answers: [],
      startedAt: new Date().toISOString(),
    };
    setSelectedLevel(level);
    setSession(nextSession);
    setStage("question");
    saveSession(nextSession);
  }

  function answer(selectedAnswer: boolean) {
    if (!session || !currentQuestion || currentAnswer) return;
    const recorded: QuizAnswer = {
      questionId: currentQuestion.id,
      selectedAnswer,
      isCorrect: selectedAnswer === currentQuestion.answer,
      answeredAt: new Date().toISOString(),
    };
    const nextSession = { ...session, answers: [...session.answers, recorded] };
    setSession(nextSession);
    setStage("feedback");
    saveSession(nextSession);
  }

  function advance() {
    if (!session) return;
    if (session.currentIndex === round.length - 1) {
      setStage("results");
      clearSession();
      return;
    }
    const nextSession = { ...session, currentIndex: session.currentIndex + 1 };
    setSession(nextSession);
    setStage("question");
    saveSession(nextSession);
  }

  function leaveQuiz() {
    if (!window.confirm("Sair do quiz? O progresso desta rodada será descartado.")) return;
    clearSession();
    setSession(null);
    setStage("start");
  }

  function chooseAnotherLevel() {
    clearSession();
    setSession(null);
    setSelectedLevel(null);
    setStage("start");
  }

  if (!ready) return <main className="main" aria-busy="true" />;

  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="brand"><span className="brand-mark" aria-hidden="true">VF</span><span>Quiz Codex</span></div>
        <span className="review-date">Conteúdo revisado em 10 ago. 2026</span>
      </header>
      <main className="main">
        {stage === "start" && (
          <section className="start" aria-labelledby="start-title">
            <p className="eyebrow">Verdadeiro ou falso</p>
            <h1 className="hero-title" id="start-title">Quanto você sabe sobre <em>Codex?</em></h1>
            <p className="hero-copy">Dez afirmações, feedback imediato e uma visão clara do que revisar. Escolha seu nível e aprenda em poucos minutos.</p>
            {dataErrors.length > 0 ? (
              <div className="empty-state" role="alert">O conteúdo do quiz está temporariamente indisponível.</div>
            ) : (
              <>
                <div className="level-grid" aria-label="Escolha o nível">
                  {levels.map((level, index) => (
                    <button key={level.id} className="level-card" aria-pressed={selectedLevel === level.id} onClick={() => setSelectedLevel(level.id)}>
                      <span className="level-number">0{index + 1}</span>
                      {selectedLevel === level.id && <span className="level-check" aria-hidden="true">✓</span>}
                      <h2>{level.name}</h2><p>{level.audience}</p>
                    </button>
                  ))}
                </div>
                <div className="start-actions">
                  <button className="primary-button" disabled={!selectedLevel} onClick={() => selectedLevel && startQuiz(selectedLevel)}>Começar quiz</button>
                  <span className="session-note">10 perguntas · cerca de 3–7 minutos</span>
                </div>
              </>
            )}
          </section>
        )}

        {(stage === "question" || stage === "feedback") && session && currentQuestion && (
          <section className="quiz-layout" aria-label="Rodada do quiz">
            <div className="quiz-topline">
              <span>Pergunta {session.currentIndex + 1} de {round.length} · {levels.find((level) => level.id === session.difficulty)?.name}</span>
              <span>{scoreAnswers(session.answers).correct} acertos</span>
              <button className="exit-button" onClick={leaveQuiz}>Sair</button>
            </div>
            <div className="progress-track" role="progressbar" aria-label="Progresso do quiz" aria-valuemin={1} aria-valuemax={round.length} aria-valuenow={session.currentIndex + 1}>
              <div className="progress-fill" style={{ width: `${((session.currentIndex + 1) / round.length) * 100}%` }} />
            </div>
            <article className="question-card">
              <div className="question-meta"><span>Afirmação</span><span>{topicLabels[currentQuestion.topic]}</span></div>
              <h1 className="question-statement" tabIndex={-1} ref={statementRef}>{currentQuestion.statement}</h1>
              <div className="answer-grid">
                {[true, false].map((choice) => {
                  const selected = currentAnswer?.selectedAnswer === choice;
                  const stateClass = selected ? (currentAnswer?.isCorrect ? "selected-correct" : "selected-incorrect") : "";
                  return <button key={String(choice)} className={`answer-button ${stateClass}`} disabled={Boolean(currentAnswer)} onClick={() => answer(choice)}>{choice ? "Verdadeiro" : "Falso"}<span className="key-hint">tecla {choice ? "V" : "F"}</span></button>;
                })}
              </div>
              {currentAnswer && (
                <div className={`feedback ${currentAnswer.isCorrect ? "correct" : "incorrect"}`} role="status" aria-live="polite" tabIndex={-1} ref={feedbackRef}>
                  <p className="feedback-status">{currentAnswer.isCorrect ? "✓ Você acertou" : "× Você errou"}</p>
                  <p><strong>Resposta correta: {currentQuestion.answer ? "Verdadeiro" : "Falso"}.</strong> {currentQuestion.explanation}</p>
                  {currentQuestion.sourceUrl && <a className="feedback-source" href={currentQuestion.sourceUrl} target="_blank" rel="noreferrer noopener">Consultar fonte oficial ↗</a>}
                  <button className="primary-button" onClick={advance}>{session.currentIndex === round.length - 1 ? "Ver resultado" : "Próxima pergunta"}</button>
                </div>
              )}
            </article>
          </section>
        )}

        {stage === "results" && session && (
          <Results session={session} round={round} onReplay={() => startQuiz(session.difficulty)} onChooseLevel={chooseAnotherLevel} />
        )}
      </main>
    </div>
  );
}

function Results({ session, round, onReplay, onChooseLevel }: { session: QuizSession; round: QuizQuestion[]; onReplay: () => void; onChooseLevel: () => void }) {
  const score = scoreAnswers(session.answers);
  const topics = scoreByTopic(round, session.answers);
  const answerMap = new Map(session.answers.map((answer) => [answer.questionId, answer]));
  return (
    <section className="quiz-layout results-card" aria-labelledby="results-title">
      <p className="eyebrow">Rodada concluída</p>
      <div className="score-ring"><div><strong>{score.percentage}%</strong><span>{score.correct} de {score.total}</span></div></div>
      <h1 id="results-title">Seu resultado</h1>
      <p className="performance">{performanceMessage(score.percentage)}</p>
      <div className="topic-results">
        <h2>Desempenho por tema</h2>
        {Object.entries(topics).map(([topic, result]) => <div className="topic-row" key={topic}><span>{topicLabels[topic as Topic]}</span><strong>{result.correct}/{result.total}</strong></div>)}
      </div>
      <div className="results-actions">
        <button className="primary-button" onClick={onReplay}>Jogar novamente</button>
        <button className="secondary-button" onClick={onChooseLevel}>Escolher outro nível</button>
      </div>
      <div className="review">
        <h2>Revise suas respostas</h2>
        {round.map((question) => {
          const answer = answerMap.get(question.id)!;
          return <article className="review-item" key={question.id}><span className={`review-state ${answer.isCorrect ? "correct" : "incorrect"}`}>{answer.isCorrect ? "✓ Acertou" : "× Errou"}</span><h3>{question.statement}</h3><p>Sua resposta: {answer.selectedAnswer ? "Verdadeiro" : "Falso"}. Correta: {question.answer ? "Verdadeiro" : "Falso"}. {question.explanation}</p></article>;
        })}
      </div>
    </section>
  );
}

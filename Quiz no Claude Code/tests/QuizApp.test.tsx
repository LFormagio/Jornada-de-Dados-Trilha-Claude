import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { QuizApp } from "@/src/components/QuizApp";

describe("QuizApp", () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it("exige a seleção de um nível antes de começar", async () => {
    render(<QuizApp />);
    const start = await screen.findByRole("button", { name: "Começar quiz" });
    expect(start).toBeDisabled();
    await userEvent.click(screen.getByRole("button", { name: /Iniciante/ }));
    expect(start).toBeEnabled();
  });

  it("aceita apenas uma resposta e mostra feedback acessível", async () => {
    vi.spyOn(Math, "random").mockReturnValue(0.5);
    render(<QuizApp />);
    await userEvent.click(await screen.findByRole("button", { name: /Iniciante/ }));
    await userEvent.click(screen.getByRole("button", { name: "Começar quiz" }));
    const verdadeiro = await screen.findByRole("button", { name: /Verdadeiro/ });
    await userEvent.click(verdadeiro);
    expect(screen.getByRole("status")).toHaveTextContent(/Você (acertou|errou)/);
    expect(verdadeiro).toBeDisabled();
    expect(screen.getByRole("button", { name: /Falso/ })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Próxima pergunta" })).toBeInTheDocument();
  });
});


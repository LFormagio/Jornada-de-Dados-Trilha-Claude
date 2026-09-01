# 📖 Guia Prático do Git — Monorepo Trilha Claude

Este documento serve como referência rápida para versionar e atualizar este repositório no GitHub (`Jornada-de-Dados-Trilha-Claude`).

---

## ⚡ 1. Fluxo do Dia a Dia (Atualizações / Edições de Código)

Sempre que realizar mudanças em qualquer um dos projetos existentes e quiser enviar para o GitHub:

1. **Abra o terminal na pasta raiz do Monorepo:**
   `D:\Lucas Formagio\Projects\Jornada de Dados - Projetos`

2. **Execute a sequência padrão:**
   ```powershell
   # 1. Cheque o que foi alterado
   git status

   # 2. Adicione todos os arquivos modificados/criados
   git add .

   # 3. Crie o commit com uma mensagem explicativa
   git commit -m "feat: Descreva aqui o que voce fez"

   # 4. Envie para o GitHub
   git push origin main
   ```

---

## 🚀 2. Adicionando um Novo Projeto (Ex: Projeto 03)

Quando iniciar um novo projeto dentro do Monorepo:

1. Crie a pasta do projeto (ex: `Trilha Claude - Projeto 3 - Nome do Projeto`).
2. Se você utilizar ferramentas que inicializam o Git automaticamente (como `create-vite`, `create-next-app` ou `git clone`), **exclua a pasta oculta `.git` de dentro do novo projeto** para não transformá-lo acidentalmente em um *submódulo*:
   ```powershell
   # Execute caso o gerador crie um .git interno:
   Remove-Item -Path "Trilha Claude - Projeto 3 - ...\.git" -Recurse -Force -ErrorAction Ignore
   ```
3. Volte para a pasta raiz `Jornada de Dados - Projetos` e faça o commit normalmente:
   ```powershell
   git status
   git add .
   git commit -m "feat: Adiciona Projeto 03 - Nome do Projeto"
   git push origin main
   ```

---

## 🛡️ 3. Regras de Ouro & Boas Práticas

- **Sempre na Raiz:** Execute os comandos `git add`, `git commit` e `git push` a partir da pasta raiz (`Jornada de Dados - Projetos`).
- **Arquivos Pesados:** O arquivo `.gitignore` na raiz já está configurado para não subir pastas temporárias ou pesadas (`node_modules/`, `.venv/`, `.next/`, `.dist/`, etc.).
- **Nomes Longos no Windows:** Caso ocorra erro de caminho longo no Windows, rode uma única vez:
  ```powershell
  git config core.longpaths true
  ```
- **Branches:** O branch principal é o **`main`**. Não é mais necessário usar `--force` / `-f` no `git push`.

---

## 🔍 4. Comandos Úteis de Diagnóstico

| Objetivo | Comando |
| :--- | :--- |
| Ver arquivos pendentes de commit | `git status` |
| Ver os últimos commits realizados | `git log --oneline -5` |
| Ver qual repositório remoto está conectado | `git remote -v` |
| Desfazer alterações não commitadas em um arquivo | `git checkout -- <caminho-do-arquivo>` |

# Repository Guidelines

## Project Structure & Module Organization

This repository currently contains the product specification in `prd.md`; treat it as the source of truth. The planned application uses React 19, TypeScript, and Vite. Keep UI code in `src/components/`, orchestration in `src/app/`, quiz data in `src/data/`, reusable logic in `src/lib/`, hooks in `src/hooks/`, shared types in `src/types/`, and global styles in `src/styles/`. Place tests beside the code they cover or under `src/__tests__/`, consistently. Static assets belong in `public/`.

## Build, Test, and Development Commands

The app has not been scaffolded yet. After creating the Vite project and installing dependencies, expose these standard npm scripts:

- `npm run dev` starts the local development server.
- `npm run lint` runs ESLint and reports style or correctness issues.
- `npm test` runs the Vitest suite.
- `npm run build` type-checks and creates the production bundle.

Do not commit `node_modules/`, `dist/`, or coverage output.

## Coding Style & Naming Conventions

Use TypeScript strict mode, two-space indentation, and functional React components. Name components and component files in PascalCase (`QuizScreen.tsx`), hooks with a `use` prefix (`useQuiz.ts`), and utilities in camelCase. Keep question data separate from rendering and business logic. Prefer explicit state transitions (`start`, `question`, `feedback`, `results`) and derive scores from recorded answers instead of duplicating state. Use CSS Modules or plain CSS variables; do not add a UI library for the MVP. All user-facing copy must be pt-BR.

## Testing Guidelines

Use Vitest and React Testing Library. Name tests `*.test.ts` or `*.test.tsx`. Cover difficulty filtering, immutable shuffling, scoring, question validation, session restoration, single-answer enforcement, navigation, and accessible control names. Inject randomness where needed so tests remain deterministic. Before submitting changes, run lint, tests, and the production build; manually verify keyboard navigation, a 320 px viewport, reload recovery, and reduced motion.

## Commit & Pull Request Guidelines

No Git history is available, so no repository-specific commit convention can be inferred. Use short, imperative subjects such as `Add resilient quiz session storage`. Keep commits focused. Pull requests should summarize the change, reference the relevant PRD requirement or issue, list verification performed, and include screenshots for visible UI changes. Call out accessibility impacts, content-source updates, and intentional deviations from `prd.md`.

## Security & Content Maintenance

Never add secrets, backend calls, analytics, or OpenAI API integration to the MVP. Validate persisted JSON and external URLs. Product-dependent claims require an official `sourceUrl` and an ISO `reviewedAt` date.

<!-- SYNC IMPACT REPORT
Version change: 0.0.0 → 1.0.0
Added sections:
  - Core Principles (7 principles)
  - Technology & Design Constraints
  - Development Workflow & Quality Gates
  - Governance
Removed sections: none
Follow-up TODOs: none
-->

# Formagio.dev Constitution

## Core Principles

### I. Bilingual-First (PT-BR / EN-US)

Every page, component, and content block MUST be fully available in both
Portuguese (PT-BR) and English (EN-US). Language switching MUST be seamless,
client-side, and preserve the current page state.

- All static UI text MUST use an i18n key system; hardcoded strings are
  forbidden.
- Content (projects, about, experience) MUST be authored in both languages
  as first-class content — not machine-translated afterthoughts.
- The default language MUST be detected from the browser's
  `navigator.language` and fallback to PT-BR.
- URL structure MUST reflect the active locale (e.g., `/en/projects`,
  `/pt/projetos`).

**Rationale**: The target audience spans Brazilian professionals, international
recruiters, and global stakeholders. Both languages are equally important to
Lucas's professional positioning.

### II. Data-Driven Storytelling

The site MUST communicate professional value through quantifiable results,
structured narratives, and visual evidence — not generic self-descriptions.

- Every project card MUST include at least one measurable impact metric
  (e.g., "50% reduction in execution time", "450 documents/month automated").
- The experience timeline MUST surface progression and scope growth, not
  just job titles.
- Skills MUST be contextualized by usage (tools tied to projects and results),
  not presented as isolated tag clouds.
- Certifications MUST be grouped by domain and recency, highlighting active
  learning trajectory.

**Rationale**: Lucas's audience — recruiters, directors, and fellow data
professionals — values demonstrated impact over self-reported skill lists.

### III. Premium Executive Aesthetics

The visual design MUST convey professionalism, technical sophistication, and
executive presence. The site MUST feel like a premium product, not a template.

- Dark mode MUST be the default theme, with an optional light mode toggle.
- Typography MUST use a modern, professional font stack (e.g., Inter, Outfit,
  or equivalent from Google Fonts).
- Color palette MUST be curated and harmonious — no generic primary colors.
  Prefer deep blues, slate grays, and accent colors that evoke data/tech.
- Micro-animations and transitions MUST enhance perceived quality without
  harming performance.
- Layout MUST be responsive across desktop, tablet, and mobile breakpoints.
- No stock photography placeholders; use generated or real assets only.

**Rationale**: First impressions from senior decision-makers and recruiters
are formed in seconds. The design itself is a demonstration of quality
standards.

### IV. Performance & SEO Excellence

The site MUST load fast, score well on Core Web Vitals, and be discoverable
by search engines and social media link previews.

- Largest Contentful Paint (LCP) MUST be under 2.5 seconds.
- Cumulative Layout Shift (CLS) MUST be under 0.1.
- Every page MUST have proper `<title>`, `<meta description>`, Open Graph
  tags, and structured data (JSON-LD for Person/ProfilePage).
- Images MUST use modern formats (WebP/AVIF) with lazy loading and
  responsive `srcset`.
- Critical CSS MUST be inlined; non-critical assets MUST be deferred.

**Rationale**: A data professional's site that loads slowly or lacks SEO
fundamentals undermines credibility.

### V. Accessibility & Inclusivity

The site MUST meet WCAG 2.1 AA compliance as a baseline.

- All interactive elements MUST be keyboard-navigable with visible focus
  indicators.
- Color contrast ratios MUST meet AA minimums (4.5:1 for normal text,
  3:1 for large text).
- All images MUST have meaningful `alt` text; decorative images MUST use
  `alt=""`.
- Semantic HTML MUST be used (`<nav>`, `<main>`, `<article>`, `<section>`,
  `<footer>`).
- ARIA attributes MUST be used only when native semantics are insufficient.

**Rationale**: Accessibility is a non-negotiable quality standard and
reflects professional maturity.

### VI. Content-as-Code

All portfolio content (projects, experience, certifications, about text)
MUST be structured as data files (JSON/YAML/Markdown), not embedded in
component markup.

- Adding a new project or certification MUST NOT require modifying component
  source code.
- Content files MUST be bilingual, containing both PT-BR and EN-US versions
  in the same structure.
- Content schema MUST be validated at build time; missing required fields
  MUST cause build failures.

**Rationale**: Scalability and maintainability. Lucas should be able to update
his portfolio by editing a data file, not by debugging JSX.

### VII. Scalable & Modular Architecture

The codebase MUST be organized into clear, reusable components with a
well-defined design system.

- A design token system (colors, typography, spacing, shadows) MUST be
  established before component development begins.
- Components MUST be self-contained and reusable across pages.
- Global state MUST be minimal; prefer component-local state and props.
- Dependencies MUST be justified; no library additions without clear need.
- File structure MUST follow a feature-based or atomic design organization.

**Rationale**: A clean architecture reflects engineering discipline and
ensures the site can evolve without accumulating technical debt.

## Technology & Design Constraints

- **Core Stack**: HTML, CSS (Vanilla), JavaScript. A framework (Vite or
  Next.js) MUST only be adopted if the user explicitly requests it.
- **Styling**: Vanilla CSS with CSS custom properties for the design token
  system. TailwindCSS is forbidden unless the user explicitly opts in.
- **Fonts**: Google Fonts (Inter or equivalent professional sans-serif).
- **Icons**: SVG-based icon system; no icon font libraries.
- **Hosting**: The site MUST be deployable as a static site (no server-side
  runtime required at minimum).
- **Version Control**: Git with conventional commits.
- **Content Format**: JSON or Markdown with frontmatter for all portfolio
  content.
- **Browser Support**: Latest 2 versions of Chrome, Firefox, Safari, and
  Edge.

## Development Workflow & Quality Gates

- **Design-First**: Visual design tokens and component library MUST be
  established before page assembly.
- **Mobile-First Responsive**: All layouts MUST be designed mobile-first and
  progressively enhanced for larger viewports.
- **Semantic Commits**: All commits MUST follow Conventional Commits format
  (e.g., `feat:`, `fix:`, `docs:`, `style:`).
- **Build Validation**: The project MUST build without errors or warnings
  before any merge or deployment.
- **Content Completeness**: Both language versions of every content entry
  MUST be present and reviewed before deployment.
- **Lighthouse Audit**: Every deployment candidate MUST score ≥90 on
  Performance, Accessibility, Best Practices, and SEO in Lighthouse.

## Governance

This constitution is the authoritative source of project principles and
constraints. All design decisions, code reviews, and architectural choices
MUST be evaluated against these principles.

- Amendments require explicit documentation of the change, rationale, and
  impact assessment.
- Principle violations MUST be justified in writing; unjustified violations
  block deployment.
- Version increments follow semantic versioning: MAJOR for principle
  removals/redefinitions, MINOR for additions/expansions, PATCH for
  clarifications.

**Version**: 1.0.0 | **Ratified**: 2026-08-24 | **Last Amended**: 2026-08-24

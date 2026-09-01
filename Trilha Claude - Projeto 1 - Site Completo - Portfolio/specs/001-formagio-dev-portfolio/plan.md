# Implementation Plan: formagio.tech — Professional Portfolio & Personal Brand

**Branch**: `001-formagio-dev-portfolio` | **Date**: 2026-08-24 | **Spec**: [spec.md](file:///d:/Lucas%20Formagio/Projects/Site%20Completo/specs/001-formagio-dev-portfolio/spec.md)

**Input**: Feature specification from `/specs/001-formagio-dev-portfolio/spec.md`

## Summary

Build **formagio.tech**, a premium bilingual (PT-BR / EN-US) professional portfolio
website for Lucas Formagio — BI Analyst & Analytics Engineer. The site will showcase
career trajectory, projects with quantified impact metrics, 50+ certifications,
and technical skills, targeting recruiters, directors, and fellow data professionals.

**Technical approach**: Static site built with Vite + vanilla HTML/CSS/JS, structured
as a modern SPA with client-side i18n routing, a CSS custom-property design system,
and all portfolio content sourced from JSON data files. Deployable to any static
hosting provider (Vercel, Netlify, GitHub Pages).

## Technical Context

**Language/Version**: JavaScript (ES2022+), HTML5, CSS3

**Primary Dependencies**: Vite 6.x (build tool + dev server), no UI framework
(vanilla JS + Web Components for encapsulation if needed)

**Storage**: N/A — all content from static JSON files at build time

**Testing**: Lighthouse CI for performance/accessibility/SEO audits, manual
cross-browser testing

**Target Platform**: Modern browsers (latest 2 versions of Chrome, Firefox,
Safari, Edge), responsive from 375px to 1440px+

**Project Type**: Static web application (SPA with client-side routing)

**Performance Goals**: Lighthouse Performance ≥ 90, LCP < 2.5s, CLS < 0.1,
TTI < 3s on 4G

**Constraints**: No server-side runtime, no backend, < 500KB initial bundle
(excluding images), progressive enhancement for no-JS fallback

**Scale/Scope**: Single-user portfolio site, ~6 page sections, ~15 projects,
~50 certifications, ~3 experience entries, 2 language variants

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Bilingual-First | ✅ PASS | i18n system with JSON locale files, URL-based locale routing, browser detection |
| II. Data-Driven Storytelling | ✅ PASS | All projects include impact metrics, experience shows progression, skills tied to projects |
| III. Premium Executive Aesthetics | ✅ PASS | Dark mode default, Corporate & Traditional (Navy & Silver) palette, subtle animations |
| IV. Performance & SEO Excellence | ✅ PASS | Vite optimized build, JSON-LD, OG tags, lazy loading, critical CSS inlining |
| V. Accessibility & Inclusivity | ✅ PASS | WCAG 2.1 AA target, semantic HTML, keyboard nav, contrast compliance |
| VI. Content-as-Code | ✅ PASS | All content in JSON data files, no hardcoded text in components |
| VII. Scalable & Modular Architecture | ✅ PASS | Design token system, component-based structure, feature-organized files |

**Pre-Phase 0 Gate: PASSED** — No violations. Proceeding to research.

## Project Structure

### Documentation (this feature)

```text
specs/001-formagio-dev-portfolio/
├── plan.md              # This file
├── research.md          # Phase 0 output — technology decisions
├── data-model.md        # Phase 1 output — content entity schemas
├── quickstart.md        # Phase 1 output — validation guide
├── contracts/           # Phase 1 output — UI component contracts
│   ├── navigation.md
│   ├── hero-section.md
│   ├── experience-timeline.md
│   ├── project-showcase.md
│   ├── skills-ecosystem.md
│   ├── certifications.md
│   └── i18n-system.md
└── tasks.md             # Phase 2 output (via $speckit-tasks)
```

### Source Code (repository root)

```text
src/
├── index.html                  # Main HTML entry point
├── main.js                     # App initialization, router, i18n bootstrap
├── styles/
│   ├── tokens.css              # Design tokens (colors, typography, spacing, shadows)
│   ├── reset.css               # CSS reset / normalize
│   ├── base.css                # Base element styles
│   ├── layout.css              # Grid system, containers, responsive breakpoints
│   ├── utilities.css           # Utility classes (visually-hidden, etc.)
│   └── animations.css          # Keyframes, transitions, scroll-reveal
├── components/
│   ├── navbar/
│   │   ├── navbar.js
│   │   └── navbar.css
│   ├── hero/
│   │   ├── hero.js
│   │   └── hero.css
│   ├── about/
│   │   ├── about.js
│   │   └── about.css
│   ├── experience/
│   │   ├── experience.js
│   │   └── experience.css
│   ├── projects/
│   │   ├── projects.js
│   │   └── projects.css
│   ├── skills/
│   │   ├── skills.js
│   │   └── skills.css
│   ├── certifications/
│   │   ├── certifications.js
│   │   └── certifications.css
│   ├── education/
│   │   ├── education.js
│   │   └── education.css
│   ├── contact/
│   │   ├── contact.js
│   │   └── contact.css
│   ├── footer/
│   │   ├── footer.js
│   │   └── footer.css
│   ├── theme-toggle/
│   │   ├── theme-toggle.js
│   │   └── theme-toggle.css
│   └── lang-toggle/
│       ├── lang-toggle.js
│       └── lang-toggle.css
├── i18n/
│   ├── i18n.js                 # i18n engine (detect, switch, translate)
│   ├── pt-br.json              # Portuguese content + UI strings
│   └── en-us.json              # English content + UI strings
├── data/
│   ├── profile.json            # Name, headline, bio, social links
│   ├── experience.json         # Career timeline entries
│   ├── projects.json           # Project portfolio with metrics
│   ├── skills.json             # Skills by category
│   ├── certifications.json     # All 50+ certifications
│   ├── education.json          # Academic background
│   └── recommendations.json    # Professional testimonials
├── assets/
│   ├── images/                 # Photos, generated images
│   ├── icons/                  # SVG icons
│   └── fonts/                  # Self-hosted font files (fallback)
└── utils/
    ├── scroll-reveal.js        # Intersection Observer scroll animations
    ├── theme.js                # Dark/light theme management
    └── router.js               # Simple hash/history-based SPA router
```

**Structure Decision**: Single-project static SPA. All content is client-side
rendered from JSON data files. No backend, no framework — vanilla JS with Vite
as the build tool. Components are organized by feature (navbar, hero, projects, etc.)
with co-located CSS. The `i18n/` directory holds locale files that contain both
UI strings and content translations.

## Complexity Tracking

No constitution violations — this section is intentionally empty.

## Post-Design Constitution Re-Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Bilingual-First | ✅ PASS | i18n engine with JSON locale files, URL locale prefix, browser detection implemented |
| II. Data-Driven Storytelling | ✅ PASS | data-model.md defines metric fields for every project and experience entry |
| III. Premium Executive Aesthetics | ✅ PASS | Design tokens include Corporate Navy & Silver palette, Inter font, elegant keyframes |
| IV. Performance & SEO Excellence | ✅ PASS | Vite code-splitting, JSON-LD in contracts, lazy image loading |
| V. Accessibility & Inclusivity | ✅ PASS | Semantic HTML in all component contracts, ARIA roles defined |
| VI. Content-as-Code | ✅ PASS | 7 JSON data files, no hardcoded content in components |
| VII. Scalable & Modular Architecture | ✅ PASS | 12 components, design token system, utils separated |

**Post-Phase 1 Gate: PASSED**

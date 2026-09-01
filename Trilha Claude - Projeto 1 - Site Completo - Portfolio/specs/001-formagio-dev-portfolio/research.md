# Research: Formagio.dev — Technology & Design Decisions

**Feature**: `001-formagio-dev-portfolio` | **Date**: 2026-08-24

## R1: Build Tool — Vite vs. Vanilla vs. Next.js

**Decision**: Vite 6.x with vanilla JS (no framework)

**Rationale**:
- Vite provides instant HMR, optimized production builds (Rollup), and native
  ES module support without requiring a framework.
- Next.js would be overkill for a static portfolio — introduces React dependency,
  SSR complexity, and larger bundle size with no benefit (no dynamic data, no API).
- Pure vanilla (no build tool) would sacrifice code-splitting, CSS minification,
  asset hashing, and dev experience.
- Vite's static site generation supports hash-based or history-based SPA routing
  natively.

**Alternatives considered**:
- **Next.js**: Rejected — too heavy for a content-static portfolio. SSR/ISR
  features are unnecessary.
- **Astro**: Considered — excellent for static content sites, but introduces
  framework-specific templating. Vite keeps it closer to web standards.
- **No build tool**: Rejected — loses minification, code-splitting, asset
  optimization, and modern development features.

---

## R2: Internationalization (i18n) Strategy

**Decision**: Custom lightweight i18n engine with JSON locale files and URL
prefix-based routing (`/en/`, `/pt/`).

**Rationale**:
- No dependency on heavy i18n libraries (i18next, FormatJS) — the site has
  ~200 translatable strings plus content blocks, well within custom scope.
- URL-based locale routing (`/en/projects`, `/pt/projetos`) is essential for
  SEO — search engines index locale-specific URLs.
- Browser locale detection via `navigator.language` with PT-BR fallback.
- Language switch is client-side only — no page reload, instant swap.
- Locale files contain both UI strings and content translations (experience,
  projects, about text) in a flat key-value structure with namespacing.

**Alternatives considered**:
- **i18next**: Rejected — 40KB+ library for a use case that needs only string
  lookup and pluralization. Custom engine is ~2KB.
- **Separate HTML files per language**: Rejected — duplicates structure,
  creates maintenance burden, breaks DRY principle.
- **Query parameter locale** (`?lang=en`): Rejected — poor for SEO, not
  bookmarkable in the same way as path-based routing.

---

## R3: Design System & Color Palette

**Decision**: CSS custom properties design token system with a curated dark-first
palette inspired by data visualization aesthetics.

**Rationale**:
- Dark mode as default conveys technical sophistication and matches the data/tech
  professional brand.
- Color palette derived from corporate aesthetics (Navy & Silver) — deep navy backgrounds,
  silver/gray texts, and corporate blue for highlights.
- CSS custom properties enable theme switching without JavaScript class toggling
  on every element.

**Color Palette**:
```css
/* Dark theme (default) */
--color-bg-primary:     hsl(217, 31%, 15%);     /* Dark Navy (#1a2332) */
--color-bg-secondary:   hsl(216, 32%, 18%);     /* Card backgrounds (#1f2b3d) */
--color-text-primary:   hsl(214, 32%, 91%);     /* Silver/Light Gray (#e2e8f0) */
--color-text-secondary: hsl(215, 25%, 65%);     /* Medium Gray (#94a3b8) */
--color-accent-primary: hsl(221, 83%, 53%);     /* IBM Corporate Blue (#2563eb) */
--color-accent-hover:   hsl(217, 91%, 60%);     /* Lighter blue (#3b82f6) */
--color-border:         hsl(216, 26%, 24%);     /* Subtle borders (#2d3a4d) */
--color-success:        hsl(142, 71%, 45%);     /* Green for metrics (#22c55e) */
--color-glass:          hsla(217, 31%, 15%, 0.8); /* Glassmorphism */

/* Light theme (toggle) */
--color-bg-primary:     hsl(210, 20%, 98%);     /* Off-white (#f8f9fa) */
--color-bg-secondary:   hsl(0, 0%, 100%);       /* Pure white */
--color-text-primary:   hsl(217, 31%, 15%);     /* Dark Navy */
--color-text-secondary: hsl(215, 15%, 45%);     /* Medium Gray */

```

**Typography**:
- **Headings**: Inter (700, 600) — clean, professional, widely supported.
- **Body**: Inter (400, 500) — excellent readability at all sizes.
- **Code/Metrics**: JetBrains Mono (400) — data-professional touch for numbers
  and metric displays.
- Scale: 1.25 (Major Third) type scale from 14px base.

**Alternatives considered**:
- **Tailwind CSS**: Rejected per constitution — vanilla CSS required unless
  explicitly requested.
- **Pre-built theme**: Rejected — no existing theme matches the specific
  data-professional aesthetic needed.
- **Material Design tokens**: Rejected — too generic, not distinctive enough
  for a personal brand.

---

## R4: Animation & Interaction Strategy

**Decision**: CSS-driven animations with Intersection Observer for scroll reveals.
No animation libraries.

**Rationale**:
- CSS animations are GPU-accelerated and don't block the main thread.
- Intersection Observer API provides efficient scroll-based triggers without
  scroll event listeners.
- Animations target `opacity` and `transform` only — the two properties that
  can be composited without triggering layout/paint.
- Interactions must be subtle and elegant, avoiding flashy or disruptive movements that detract from the corporate vibe.

**Animation inventory**:
- **Hero entrance**: Staggered fade-up for name → headline → CTA (300ms delays)
- **Scroll reveals**: Elements fade-in + translate-y(20px) when entering viewport
- **Timeline nodes**: Sequential appear on scroll with scale pulse
- **Project cards**: Hover lift + subtle glow on accent border
- **Skill badges**: Hover scale(1.05) with background color transition
- **Navigation**: Backdrop-filter blur for glassmorphism sticky nav
- **Theme toggle**: Smooth color transitions (300ms ease)
- **Language toggle**: Content cross-fade (200ms)
- **Metric counters**: Animated count-up on viewport entry

**Alternatives considered**:
- **GSAP**: Rejected — 25KB+ for animations achievable with CSS + IO API.
- **Framer Motion**: Rejected — React dependency.
- **AOS library**: Rejected — 14KB for what Intersection Observer does natively.

---

## R5: SEO & Structured Data Strategy

**Decision**: JSON-LD structured data (Person + ProfilePage schemas), Open Graph
tags, semantic HTML, sitemap.xml.

**Rationale**:
- JSON-LD is Google's preferred structured data format.
- ProfilePage schema directly maps to the portfolio use case.
- Open Graph tags ensure professional link previews on LinkedIn, Twitter, WhatsApp.

**Implementation**:
- `<script type="application/ld+json">` in `<head>` with Person schema including
  name, jobTitle, worksFor, skills, sameAs (LinkedIn URL).
- Dynamic `<title>` and `<meta description>` per locale.
- `<link rel="alternate" hreflang="pt-br">` / `<link rel="alternate" hreflang="en-us">`
  for cross-locale SEO.
- Canonical URLs with locale prefix.
- `sitemap.xml` generated at build time listing both locale variants.

---

## R6: Image & Asset Strategy

**Decision**: WebP format with lazy loading, responsive `srcset`, and generated
placeholder images via the generate_image tool during development.

**Rationale**:
- WebP provides 25-35% smaller files than JPEG at equivalent quality.
- Lazy loading (`loading="lazy"`) defers off-screen images.
- `srcset` with `sizes` attribute serves appropriate resolution per viewport.
- Professional photos/avatars will be generated during development; Lucas can
  replace with real photos later.

---

## R7: Deployment Strategy

**Decision**: Static deployment via Vercel (primary) or GitHub Pages (fallback).

**Rationale**:
- Vite builds to a `dist/` folder of static assets — compatible with any static
  host.
- Vercel offers: automatic HTTPS, global CDN, preview deployments, custom domain
  support, and zero-config Vite detection.
- GitHub Pages as fallback requires only a GitHub Action to push `dist/` to
  `gh-pages` branch.
- SPA fallback routing configured via `vercel.json` or `_redirects` file.

---

## R8: Content Data Architecture

**Decision**: Flat JSON files with bilingual content embedded in a `{pt, en}`
structure per field.

**Rationale**:
- Simpler than separate locale files for content (avoids key synchronization
  issues between files).
- UI strings remain in separate locale JSON files (`pt-br.json`, `en-us.json`).
- Build-time validation ensures no missing translations.

**Example structure**:
```json
{
  "id": "quote-flow-tracker",
  "title": { "pt": "Monitor de Cotações", "en": "Quote Flow Tracker" },
  "description": { "pt": "Produto de BI que...", "en": "BI product that..." },
  "metrics": [
    { "value": "45000+", "label": { "pt": "linhas/mês", "en": "lines/month" } },
    { "value": "50%", "label": { "pt": "redução no tempo", "en": "time reduction" } }
  ],
  "technologies": ["Power BI", "DAX", "SAP BW"],
  "category": "bi-products",
  "dateRange": { "start": "2023-08", "end": null }
}
```

This approach keeps content maintainable while supporting bilingual rendering
without duplicating entire data structures.

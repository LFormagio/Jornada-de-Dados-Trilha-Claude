# Quickstart Validation Guide: Formagio.dev

**Feature**: `001-formagio-dev-portfolio` | **Date**: 2026-08-24

## Prerequisites

- **Node.js**: v18+ (LTS recommended)
- **npm**: v9+ (bundled with Node.js)
- **Browser**: Chrome, Firefox, Safari, or Edge (latest 2 versions)
- **OS**: Windows, macOS, or Linux

## Setup

```bash
# 1. Navigate to the project root
cd "d:\Lucas Formagio\Projects\Site Completo"

# 2. Initialize Vite project (if not yet created)
npx -y create-vite@latest ./ --template vanilla

# 3. Install dependencies
npm install

# 4. Start development server
npm run dev
```

The dev server will start at `http://localhost:5173/`.

## Validation Scenarios

### VS-001: Homepage Renders Correctly

**Action**: Open `http://localhost:5173/` in a browser.

**Expected**:
- Hero section displays with Lucas's name, headline, metrics, and avatar.
- Navbar is visible at the top with all section links.
- Language toggle shows PT/EN buttons (PT active by default for pt-BR locale).
- Theme toggle shows moon icon (dark mode is default).
- Scroll indicator pulses at the bottom of the hero.

---

### VS-002: Language Switching

**Action**: Click the "EN" button in the navbar.

**Expected**:
- All UI text switches to English (< 200ms).
- URL updates to include `/en/` prefix.
- Hero metrics labels change to English.
- Navigation links change: "Sobre" → "About", "Projetos" → "Projects", etc.
- Clicking "PT" reverts all text to Portuguese.
- Refreshing the page preserves the selected language.

---

### VS-003: Theme Switching

**Action**: Click the theme toggle button.

**Expected**:
- All colors transition smoothly (300ms) from dark to light palette.
- Background changes from deep navy to light gray.
- Text color inverts appropriately.
- Clicking again returns to dark mode.
- Preference persists on page refresh.

---

### VS-004: Section Navigation

**Action**: Click each navigation link (About, Experience, Projects, Skills,
Certifications, Education, Contact).

**Expected**:
- Page smooth-scrolls to the target section.
- Active section is highlighted in the navbar.
- Scrolling manually also updates the active nav indicator.

---

### VS-005: Experience Timeline Interaction

**Action**: Scroll to the Experience section and click "Ver detalhes" on the
BI Analyst entry.

**Expected**:
- Detail panel expands with slide-down animation.
- Shows achievement bullets, key metrics, and technology badges.
- Button text changes to "Fechar" (or "Close" in EN).
- Clicking again collapses the panel.

---

### VS-006: Project Filtering

**Action**: Navigate to the Projects section and click different filter buttons.

**Expected**:
- "Todos" shows all projects.
- "BI Products" shows only BI-related projects (Quote Flow Tracker, Sales Data
  Intelligence, etc.).
- "Automação" shows only automation projects (Workflow Automation Engine, etc.).
- "IA" shows AI Solutions projects.
- Filtered-out cards animate out; filtered-in cards animate in.
- Project count updates per filter.

---

### VS-007: Project Detail Modal

**Action**: Click a project card (e.g., Quote Flow Tracker).

**Expected**:
- Modal opens with overlay and focus trap.
- Shows full description, all metrics, all technologies, and timeline.
- Pressing Escape or clicking overlay closes modal.
- Focus returns to the triggering card after modal closes.

---

### VS-008: Responsive Layout

**Action**: Resize the browser window through breakpoints (375px, 768px,
1024px, 1440px).

**Expected**:
- `< 768px`: Hamburger menu, single-column layouts, stacked content.
- `768px–1023px`: Two-column grids, condensed timeline.
- `≥ 1024px`: Full layouts, multi-column grids, horizontal navigation.
- No horizontal overflow at any breakpoint.
- All text remains readable.

---

### VS-009: Accessibility Audit

**Action**: Run Lighthouse accessibility audit in Chrome DevTools.

**Expected**:
- Score ≥ 90.
- All interactive elements keyboard-navigable.
- Tab order is logical.
- All images have alt text.
- Color contrast passes AA standards.

---

### VS-010: Performance Audit

**Action**: Run Lighthouse performance audit in Chrome DevTools (mobile preset).

**Expected**:
- Performance score ≥ 90.
- LCP < 2.5s.
- CLS < 0.1.
- Total bundle size < 500KB (excluding images).

---

### VS-011: SEO Validation

**Action**: Run Lighthouse SEO audit and check page source.

**Expected**:
- SEO score ≥ 95.
- `<title>` tag present and descriptive.
- `<meta description>` present.
- Open Graph tags present (`og:title`, `og:description`, `og:image`).
- JSON-LD structured data present with Person schema.
- `<link rel="alternate" hreflang>` tags for both locales.

---

### VS-012: Certifications Display

**Action**: Scroll to Certifications section.

**Expected**:
- Initial view shows 12 most recent certifications.
- "Ver mais" button reveals remaining certifications.
- Domain filter tabs filter correctly.
- Total count badge shows 50+.
- Credential verification links open in new tabs.

---

## Production Build Validation

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

**Expected**:
- Build completes without errors or warnings.
- Production preview at `http://localhost:4173/` matches dev behavior.
- All assets are hashed and optimized.
- CSS is minified.
- JavaScript is tree-shaken and minified.

## Deployment Validation

```bash
# Deploy to Vercel (if configured)
npx vercel --prod

# Or deploy to GitHub Pages
# Push dist/ to gh-pages branch
```

**Expected**:
- Site loads on custom domain with HTTPS.
- All routes resolve correctly (SPA fallback working).
- Both locale URLs work (`/en/`, `/pt/`).
- Open Graph previews render correctly on LinkedIn and Twitter.

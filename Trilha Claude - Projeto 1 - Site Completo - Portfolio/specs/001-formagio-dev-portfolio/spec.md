# Feature Specification: formagio.tech — Professional Portfolio & Personal Brand

**Feature Branch**: `001-formagio-dev-portfolio`

**Created**: 2026-08-24

**Status**: Draft

**Input**: User description: "Site pessoal profissional e executivo. Portfolio, consultoria e currículo para área de dados, analytics, BI, Analytics Engineering. Público-alvo: profissionais de tecnologia, recrutadores, gestores e diretores. Bilíngue PT-BR/EN-US."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - First Impression & Navigation (Priority: P1)

A recruiter or hiring manager lands on Formagio.dev for the first time and immediately understands who Lucas is, what he does, and how to navigate the site. The hero section conveys expertise, professionalism, and measurable impact within seconds.

**Why this priority**: First impressions determine whether visitors explore further or bounce. The hero + navigation is the minimum viable product.

**Independent Test**: Can be tested by loading the homepage and verifying the hero section, navigation menu, and language toggle render correctly in both PT-BR and EN-US.

**Acceptance Scenarios**:

1. **Given** a first-time visitor, **When** they load the homepage, **Then** they see a hero section with Lucas's name, headline, a compelling value proposition with key metrics, and a professional photo (using the cutout version with removed background).
2. **Given** a visitor with browser locale `en-US`, **When** they load the site, **Then** all UI text renders in English by default.
3. **Given** a visitor viewing in PT-BR, **When** they click the language toggle, **Then** all content switches to EN-US without page reload, and the URL updates to reflect `/en/`.
4. **Given** a visitor on mobile, **When** they view the homepage, **Then** the layout is fully responsive with a hamburger menu for navigation.

---

### User Story 2 - Professional Experience Timeline (Priority: P1)

A recruiter or director explores Lucas's career trajectory, understanding his progression from intern to BI Analyst with quantifiable achievements at each stage.

**Why this priority**: Experience is the primary evaluation criterion for senior roles and consulting engagements.

**Independent Test**: Can be tested by navigating to the Experience section and verifying all positions render with correct dates, titles, descriptions, and metrics.

**Acceptance Scenarios**:

1. **Given** a visitor on the Experience section, **When** they view the timeline, **Then** they see a unified Avnet card highlighting the BI Analyst role with full metrics, and previous positions (Sales Rep, Sales Intern) presented compactly to show upward progression.
2. **Given** a visitor, **When** they interact with a timeline entry, **Then** they can expand to see detailed achievements and technologies used.
3. **Given** the content is in PT-BR, **When** the user switches to EN-US, **Then** all experience descriptions update to English equivalents.

---

### User Story 3 - Project Showcase with Impact Metrics (Priority: P1)

A technical manager or data professional browses Lucas's project portfolio, seeing real deliverables with measurable business impact, technologies used, and scope.

**Why this priority**: Projects demonstrate practical capability and are the strongest proof of expertise beyond job titles.

**Independent Test**: Can be tested by navigating to the Projects section and verifying project cards render with titles, descriptions, metrics, tech stacks, and proper filtering.

**Acceptance Scenarios**:

1. **Given** a visitor on the Projects page, **When** they view the grid/list, **Then** they see project cards for all major projects (Quote Flow Tracker, AI Solutions, Workflow Automation Engine, Customer Financial Overview Suite, etc.) with impact metrics and tech badges.
2. **Given** a visitor, **When** they click a project card, **Then** a detailed view expands showing full description, scope, technologies, timeline, and quantified results.
3. **Given** a visitor, **When** they filter by technology (e.g., "Power BI", "Microsoft Fabric"), **Then** only relevant projects are displayed.
4. **Given** a visitor, **When** they filter by category (e.g., "BI Products", "Automation", "AI Solutions"), **Then** projects are filtered accordingly.

---

### User Story 4 - Skills & Technology Ecosystem (Priority: P2)

A visitor explores Lucas's technical competencies, seeing skills organized by category and validated by project usage — not just listed as buzzwords.

**Why this priority**: Skills provide a quick scan for keyword matching (recruiters) and depth assessment (technical leads).

**Independent Test**: Can be tested by navigating to the Skills section and verifying skills render grouped by category with project cross-references.

**Acceptance Scenarios**:

1. **Given** a visitor on the Skills section, **When** they view the layout, **Then** skills are organized into categories: BI & Analytics, Data Engineering, Automation, AI & ML, Programming, ERP/SAP, Soft Skills.
2. **Given** a visitor, **When** they hover/click a skill, **Then** they see which projects and roles used that skill.
3. **Given** a visitor, **When** they view the skills section, **Then** primary tools (Power BI, Microsoft Fabric, DAX, SQL, Python, Power Automate) are visually emphasized over secondary ones.

---

### User Story 5 - Certifications & Continuous Learning (Priority: P2)

A visitor sees Lucas's 50+ certifications organized by domain and recency, demonstrating a continuous learning trajectory.

**Why this priority**: Certifications validate commitment to professional growth and breadth of knowledge.

**Independent Test**: Can be tested by navigating to the Certifications section and verifying certifications render grouped and filterable.

**Acceptance Scenarios**:

1. **Given** a visitor on the Certifications section, **When** they view the layout, **Then** they see a grid of issuer logos (Anthropic, Databricks, Microsoft, etc.) with a prominent "50+ Certifications" badge.
2. **Given** a visitor, **When** they want to see more, **Then** they can click to expand the exhaustive list of certifications.
3. **Given** a visitor, **When** they view a certification, **Then** they see the issuer, date, and associated skills.

---

### User Story 6 - Education & Awards (Priority: P2)

A visitor sees Lucas's academic background, his capstone project achievement, and relevant academic activities.

**Why this priority**: Education adds context, especially the 2nd-place INOVA FEI award which validates applied research capability.

**Independent Test**: Can be tested by verifying the Education section renders with university, degree, capstone project details, and awards.

**Acceptance Scenarios**:

1. **Given** a visitor on the Education section, **When** they view the content, **Then** they see FEI - Production Engineering degree with dates, capstone project title, and 2nd place INOVA FEI recognition.
2. **Given** a visitor, **When** they view the capstone project, **Then** they see impact metrics (74.48% step reduction, 335.5 hours saved, R$ 90k+ annual savings).

---

### User Story 7 - Contact & Call to Action (Priority: P2)

A recruiter, manager, or potential client can easily reach Lucas through a professional contact section.

**Why this priority**: The site's ultimate conversion goal is professional contact.

**Independent Test**: Can be tested by navigating to the Contact section and verifying all links work and the form (if present) submits successfully.

**Acceptance Scenarios**:

1. **Given** a visitor on the Contact section, **When** they view the content, **Then** they see LinkedIn, email, and a Smart CV Download button with clear CTAs.
2. **Given** a visitor, **When** they click a contact link, **Then** it opens the appropriate application (email client, LinkedIn profile).
3. **Given** a visitor, **When** they view the contact section, **Then** they see a brief professional availability statement.

---

### User Story 8 - About / Bio Section (Priority: P2)

A visitor reads a compelling professional summary that positions Lucas as a BI/Analytics expert who combines business acumen with technical execution.

**Why this priority**: The About section provides narrative context that job titles and metrics alone cannot convey.

**Independent Test**: Can be tested by navigating to the About section and verifying the bio renders in both languages with key highlights.

**Acceptance Scenarios**:

1. **Given** a visitor on the About section, **When** they read the bio, **Then** they understand Lucas's professional identity: BI Analyst + Production Engineer who bridges business and technology.
2. **Given** a visitor, **When** they view the About section, **Then** they see key stats (4+ years experience, 140+ initiatives, 85+ improvements, 18 automations).
3. **Given** a visitor, **When** they view the About section, **Then** they see professional recommendations/testimonials.

---

### Edge Cases

- What happens when a visitor accesses a locale-prefixed URL that doesn't exist (e.g., `/fr/projects`)? → Redirect to default locale.
- How does the system handle a browser locale that is neither PT-BR nor EN-US? → Default to PT-BR.
- What happens on extremely narrow viewports (< 320px)? → Maintain readability with single-column layout.
- What happens if a project has no impact metrics? → Display "In progress" badge instead of empty metrics.
- What happens when JS is disabled? → Core content MUST still be readable (progressive enhancement).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Site MUST support full bilingual content switching between PT-BR and EN-US via a visible language toggle.
- **FR-002**: Site MUST auto-detect browser locale and set initial language accordingly (PT-BR fallback).
- **FR-003**: URL structure MUST reflect active locale (e.g., `/en/projects`, `/pt/projetos`).
- **FR-004**: Hero section MUST display: name, professional headline, value proposition, key metrics, and professional photo/avatar.
- **FR-005**: Experience section MUST render a visual timeline with all professional positions, dates, descriptions, and quantified achievements.
- **FR-006**: Projects section MUST display project cards with: title, description, impact metrics, technology badges, and category tags.
- **FR-007**: Projects MUST be filterable by technology and category.
- **FR-008**: Skills section MUST group competencies by category with project cross-references.
- **FR-009**: Certifications section MUST display 50+ certifications grouped by domain, filterable by year/domain.
- **FR-010**: Education section MUST show degree, university, capstone project, and INOVA FEI award.
- **FR-011**: Contact section MUST provide LinkedIn, email, and a Smart CV Download button (no GitHub or WhatsApp).
- **FR-012**: Site MUST be fully responsive across mobile, tablet, and desktop breakpoints.
- **FR-013**: Site MUST implement dark mode as default with optional light mode toggle.
- **FR-014**: All portfolio content (projects, experience, certifications) MUST be sourced from structured data files (JSON/YAML), not hardcoded in components.
- **FR-015**: Site MUST implement proper SEO with title tags, meta descriptions, Open Graph tags, and JSON-LD structured data.
- **FR-016**: Navigation MUST include smooth scroll to sections with active state indicators.
- **FR-017**: Site MUST include micro-animations for element transitions, hover effects, and scroll reveals.
- **FR-018**: Site MUST include a downloadable CV/Resume option (PDF) in both languages.
- **FR-019**: Section ordering MUST be: Hero -> Projects -> Experience -> Skills -> About -> Certifications -> Education -> Contact.

### Key Entities

- **Profile**: Name, headline, bio (PT-BR + EN-US), photo, social links, availability status.
- **Experience**: Company, title, employment type, date range, location, description (PT-BR + EN-US), metrics, technologies.
- **Project**: Title, description (PT-BR + EN-US), category, date range, impact metrics, technologies, association.
- **Skill**: Name, category, proficiency level, related projects.
- **Certification**: Title, issuer, date, credential ID, credential URL, associated skills.
- **Education**: Institution, degree, field, date range, description, activities, awards.
- **Recommendation**: Author name, author title, relationship, text (PT-BR + EN-US).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Lighthouse Performance score ≥ 90 on mobile and desktop.
- **SC-002**: Lighthouse Accessibility score ≥ 90.
- **SC-003**: Lighthouse SEO score ≥ 95.
- **SC-004**: Language switching completes in < 200ms with no layout shift.
- **SC-005**: All 18 key entities (experience entries, projects, certifications) render correctly in both languages.
- **SC-006**: Time to Interactive (TTI) < 3 seconds on 4G connection.
- **SC-007**: All project cards display at least one quantifiable impact metric.
- **SC-008**: Site passes WCAG 2.1 AA automated audit with zero critical violations.

## Assumptions

- The site will be a static single-page application (SPA) or multi-page static site — no server-side runtime required.
- Professional photo/avatar will be provided by Lucas or generated during development.
- Content data files will be pre-authored in both languages by Lucas (or drafted by the agent and refined).
- Initial deployment target is a static hosting provider (e.g., Vercel, Netlify, GitHub Pages).
- No contact form with backend processing in v1; direct links to LinkedIn/email are sufficient.
- No blog or CMS integration in v1 — content updates happen via data file edits.
- Mobile-first responsive design with breakpoints at 375px, 768px, 1024px, and 1440px.

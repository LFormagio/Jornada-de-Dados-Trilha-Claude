# Product Requirements Document (PRD): formagio.tech

## 1. Executive Summary
**Project Name:** formagio.tech
**Concept:** A premium, bilingual (PT-BR / EN-US) professional portfolio and personal brand website for Lucas Formagio.
**Role:** Business Intelligence Analyst & Analytics Engineer.
**Primary Audience:** Recruiters, Technical Directors, C-level Executives, and potential consulting clients.
**Core Objective:** Position Lucas as an authority in BI, Data Engineering, Automation, and AI by showcasing quantifiable impact, a solid career trajectory, and a vast array of technical certifications.

## 2. Brand & Aesthetic Direction
**Style:** Corporate & Traditional
**Vibe:** Conservative, neutral, reliable, and highly professional.
**Inspirations:** Top-tier consulting firms (McKinsey, IBM, Deloitte, Bain).
**Color Palette (Navy & Silver):**
- **Primary Background:** `#1a2332` (Dark Navy)
- **Secondary Background (Cards):** `#1f2b3d`
- **Light Mode Background:** `#f8f9fa` (Off-white)
- **Primary Text:** `#e2e8f0` (Silver/Light Gray)
- **Secondary Text:** `#94a3b8` (Medium Gray)
- **Accent Color:** `#2563eb` (IBM Corporate Blue)
- **Hover Accent:** `#3b82f6`
- **Borders:** `#2d3a4d`
- **Success/Metrics:** `#22c55e`

**Typography:** Clean, strong, and highly readable sans-serif (e.g., Inter).
**Theme:** Dark mode by default, with a toggle for Light mode.
**Animations:** Subtle and elegant. Soft scroll-reveals, smooth hover effects, and count-up animations for numbers. No distracting or overly complex interactions.

## 3. Architecture & Tech Stack
- **Approach:** Single-page application (SPA) layout with anchor scrolling.
- **Core Stack:** Vite + Vanilla JS/CSS/HTML.
- **Rationale:** Absolute maximum simplicity and performance. No heavy frameworks (like Next.js or React) are needed since the site is content-heavy and static.
- **Deployment:** Vercel.
- **Data Management:** "Content-as-Code". All portfolio data (projects, experience, skills) will reside in structured JSON files, heavily decoupled from the UI components.
- **Internationalization (i18n):** Custom lightweight JS solution managing state between PT-BR and EN-US. URL routing handles language state (e.g., `/en/`, `/pt/`).

## 4. Section Architecture & User Flow
The site is structured as a single continuous scroll, ordered strategically to present results before history ("Show, don't tell").

**Scroll Order:**
1. **Hero Section**
2. **Projects (Showcase)**
3. **Experience**
4. **Skills**
5. **About**
6. **Certifications**
7. **Education**
8. **Contact**

## 5. Detailed Functional Requirements

### 5.1 Global Features
- **Bilingual Toggle:** Seamless switching between Portuguese and English.
- **Theme Toggle:** Switch between Dark (Navy) and Light themes.
- **Sticky Navigation:** Glassmorphism navbar that highlights the active section on scroll.
- **Responsive Design:** Mobile-first approach, fully responsive up to ultra-wide desktop breakpoints.

### 5.2 Hero Section
- **Composition:** Value proposition headline + impact metrics (e.g., "140+ iniciativas") + professional statement + data visualization elements + professional photo (using the cutout version with removed background).
- **CTA:** Primary actions guiding the user to Projects or Contact.

### 5.3 Projects
- **Display:** 6 to 8 highly curated, high-impact projects.
- **Card Design:** Focused on metrics. Each card highlights 1-2 massive numbers (e.g., "45k+ lines/month"), tech stack badges, and a "View Details" button.
- **Details:** Clicking a project opens a detailed modal or expandable section with the full case study.
- **Filtering:** Users can filter projects by category (BI, AI, Automation, etc.).

### 5.4 Experience
- **Focus:** The +5 years trajectory at Avnet.
- **Structure:** A unified Avnet card that highlights the current "BI Analyst" role with full metrics, while previous roles (Sales Rep, Intern) are presented compactly to show upward progression.

### 5.5 Skills
- **Display:** Grid of badges categorized logically (BI & Analytics, Data Engineering, Automation, AI & ML, SAP, Programming).
- **Visual Hierarchy:** Primary skills (e.g., Power BI, Fabric, DAX, Python) are visually larger or highlighted. Includes tool icons.

### 5.6 About
- **Content:** Concise professional biography (3-4 sentences).
- **Social Proof:** Includes 2 embedded LinkedIn recommendations.
- **Languages:** Badges indicating spoken language proficiency (PT Native, EN C1, ES Basic).

### 5.7 Certifications
- **Display:** Grid displaying issuer logos (Anthropic, Databricks, Microsoft, etc.).
- **Summary Badge:** Prominent "50+ Certifications" badge.
- **Interaction:** A "View All" or "Expand" button to reveal the exhaustive list without cluttering the main scroll.

### 5.8 Education
- **Content:** Production Engineering degree at FEI, highlighting the capstone project and the 2nd place INOVA FEI award.

### 5.9 Contact
- **CTAs:** Three equally balanced main calls to action:
  1. Connect on LinkedIn (Primary focus).
  2. Send an Email.
  3. Download CV (Smart button that downloads the PDF corresponding to the currently selected site language).
- **Exclusions:** No GitHub or WhatsApp links to maintain executive formality.

## 6. Success Metrics & Acceptance Criteria
- **Performance:** Lighthouse score ≥ 90 across all categories (Performance, Accessibility, Best Practices, SEO).
- **Load Time:** LCP (Largest Contentful Paint) < 2.5s.
- **SEO:** Proper implementation of semantic HTML, meta tags, Open Graph tags, and JSON-LD structured data.
- **Accessibility:** WCAG 2.1 AA compliance (keyboard navigation, contrast ratios, aria-labels).
- **Content Integrity:** All JSON data files properly render bilingual content without layout breakage.

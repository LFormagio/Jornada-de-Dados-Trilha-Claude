# Tasks: formagio.tech — Professional Portfolio & Personal Brand

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Vite project with vanilla JavaScript (no framework) in repo root
- [x] T002 [P] Create CSS foundation in `src/styles/` (tokens.css, reset.css, base.css, layout.css, animations.css)
- [x] T003 [P] Setup basic `src/index.html` skeleton and `src/main.js` entrypoint
- [x] T004 [P] Create asset directories (`src/assets/images`, `src/assets/icons`, `src/assets/fonts`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**🚨 CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Implement i18n engine in `src/i18n/i18n.js` with URL routing support
- [x] T006 [P] Create initial locale files `src/i18n/pt-br.json` and `src/i18n/en-us.json`
- [x] T007 [P] Implement Theme toggle utility in `src/utils/theme.js`
- [x] T008 [P] Implement Scroll Reveal utility via Intersection Observer in `src/utils/scroll-reveal.js`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First Impression & Navigation (Priority: P1) 🏆 MVP

**Goal**: Hero section with value prop, navigation, and language/theme toggles.

**Independent Test**: Load homepage and verify hero renders with avatar, metrics, and that language toggle changes text without reload.

### Implementation for User Story 1

- [x] T009 [P] [US1] Create Profile data source in `src/data/profile.json`
- [x] T010 [P] [US1] Implement LangToggle component in `src/components/lang-toggle/lang-toggle.js` and `lang-toggle.css`
- [x] T011 [P] [US1] Implement ThemeToggle component in `src/components/theme-toggle/theme-toggle.js` and `theme-toggle.css`
- [x] T012 [US1] Implement Navbar component in `src/components/navbar/navbar.js` and `navbar.css` (depends on Lang/Theme toggles)
- [x] T013 [US1] Implement Hero component in `src/components/hero/hero.js` and `hero.css` based on contract
- [x] T014 [US1] Integrate Hero and Navbar into `src/index.html` and bootstrap in `src/main.js`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 3 - Project Showcase (Priority: P1)

**Goal**: Filterable grid of project cards with detailed modal/expansion view and impact metrics.
*(Note: Ordered before Experience as per new PRD)*

**Independent Test**: Navigate to Projects section and verify project cards render, filter works, and clicking expands details.

### Implementation for User Story 3

- [x] T015 [P] [US3] Create Projects data source in `src/data/projects.json`
- [x] T016 [P] [US3] Add Projects UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [x] T017 [US3] Implement Projects component (grid & filters) in `src/components/projects/projects.js` and `projects.css`
- [x] T018 [US3] Integrate Projects component into `src/index.html` and `src/main.js`

**Checkpoint**: At this point, User Stories 1 AND 3 should both work independently

---

## Phase 5: User Story 2 - Professional Experience Timeline (Priority: P1)

**Goal**: Vertical timeline displaying career progression (Unified Avnet card + previous roles).

**Independent Test**: Navigate to Experience section and verify timeline entries render with expansion functionality.

### Implementation for User Story 2

- [x] T019 [P] [US2] Create Experience data source in `src/data/experience.json`
- [x] T020 [P] [US2] Add Experience UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [x] T021 [US2] Implement Experience component (timeline & unified card) in `src/components/experience/experience.js` and `experience.css`
- [x] T022 [US2] Integrate Experience component into `src/index.html` and `src/main.js`

**Checkpoint**: All P1 user stories should now be independently functional

---

## Phase 6: User Story 4 - Skills Ecosystem (Priority: P2)

**Goal**: Visual display of technical and soft skills organized by category.

**Independent Test**: Navigate to Skills section and verify skills render by category with hover effects.

### Implementation for User Story 4

- [ ] T023 [P] [US4] Create Skills data source in `src/data/skills.json`
- [ ] T024 [P] [US4] Add Skills UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [ ] T025 [US4] Implement Skills component in `src/components/skills/skills.js` and `skills.css`
- [ ] T026 [US4] Integrate Skills component into `src/index.html` and `src/main.js`

---

## Phase 7: User Story 8 - About / Bio Section (Priority: P2)

**Goal**: Professional summary positioning Lucas as a BI/Analytics expert.

**Independent Test**: Read the bio in both languages with key highlights and stats.

### Implementation for User Story 8

- [ ] T027 [P] [US8] Create Recommendations data source in `src/data/recommendations.json`
- [ ] T028 [P] [US8] Add About UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [ ] T029 [US8] Implement About component in `src/components/about/about.js` and `about.css`
- [ ] T030 [US8] Integrate About component into `src/index.html` and `src/main.js`

---

## Phase 8: User Story 5 - Certifications & Continuous Learning (Priority: P2)

**Goal**: 50+ certifications visually represented by a grid of prominent logos and an expandable list.

**Independent Test**: View the logos grid, the 50+ badge, and test the "View all" expansion.

### Implementation for User Story 5

- [ ] T031 [P] [US5] Create Certifications data source in `src/data/certifications.json`
- [ ] T032 [P] [US5] Add Certifications UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [ ] T033 [US5] Implement Certifications component (Logos Grid) in `src/components/certifications/certifications.js` and `certifications.css`
- [ ] T034 [US5] Integrate Certifications component into `src/index.html` and `src/main.js`

---

## Phase 9: User Story 6 - Education & Awards (Priority: P2)

**Goal**: Academic background with capstone project impact and INOVA FEI award.

**Independent Test**: View Education section and verify capstone metrics render correctly.

### Implementation for User Story 6

- [ ] T035 [P] [US6] Create Education data source in `src/data/education.json`
- [ ] T036 [P] [US6] Add Education UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [ ] T037 [US6] Implement Education component in `src/components/education/education.js` and `education.css`
- [ ] T038 [US6] Integrate Education component into `src/index.html` and `src/main.js`

---

## Phase 10: User Story 7 - Contact & Call to Action (Priority: P2)

**Goal**: Professional contact section with LinkedIn, Email, and Smart CV Download.

**Independent Test**: Verify contact links and CV download button work correctly.

### Implementation for User Story 7

- [ ] T039 [P] [US7] Add Contact UI strings to `src/i18n/pt-br.json` and `en-us.json`
- [ ] T040 [US7] Implement Contact component in `src/components/contact/contact.js` and `contact.css`
- [ ] T041 [US7] Implement Footer component in `src/components/footer/footer.js` and `footer.css`
- [ ] T042 [US7] Integrate Contact and Footer components into `src/index.html` and `src/main.js`

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T043 [P] Add WebP images and SVG icons to `src/assets/images` and `src/assets/icons`
- [ ] T044 [P] Implement semantic HTML and ARIA roles across all components for WCAG 2.1 AA compliance
- [ ] T045 Update `src/index.html` with JSON-LD ProfilePage schema, Meta tags, and Open Graph tags
- [ ] T046 Run Lighthouse audits (Performance, Accessibility, SEO) and fix issues to reach 90+ scores
- [ ] T047 Run quickstart.md validation guide manually

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-10)**: All depend on Foundational phase completion
  - Proceed sequentially from Phase 3 (Hero) to Phase 10 (Contact)
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **Other Stories (P1/P2)**: Can start after Foundational (Phase 2). They are independently testable via their respective data JSONs and DOM injection, but naturally stack below the Hero section.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Data JSON files across different stories can be generated in parallel
- UI strings in i18n files can be added in parallel
- Different components (e.g., Skills and Education) can be implemented in parallel by different workers once foundational utilities are in place.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Hero & Navigation)
4. **STOP and VALIDATE**: Verify the hero renders and the language toggle works.

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 (Hero) -> MVP
3. Add User Story 3 (Projects) -> Value demonstrated
4. Add User Story 2 (Experience) -> Context provided
5. Add remaining P2 stories (Skills, About, Certifications, Education, Contact).
6. Polish with SEO and Accessibility.

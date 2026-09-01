# Contract: Project Showcase

## Component: `ProjectShowcase`

### Purpose
Filterable grid of project cards with detailed modal/expansion view.
Each card prominently displays impact metrics and technology stack.

### HTML Structure
```html
<section id="projects" class="projects section" aria-labelledby="projects-heading">
  <div class="section__container">
    <h2 id="projects-heading" class="section__title" data-i18n="projects.title">
      Projetos
    </h2>
    <p class="section__subtitle" data-i18n="projects.subtitle">
      Soluções com impacto mensurável
    </p>

    <!-- Filter bar -->
    <div class="projects__filters" role="toolbar" aria-label="Project filters">
      <div class="projects__filter-group" role="radiogroup"
           aria-label="Filter by category">
        <button class="projects__filter projects__filter--active"
                role="radio" aria-checked="true"
                data-filter="all" id="filter-all"
                data-i18n="projects.filter.all">Todos</button>
        <button class="projects__filter"
                role="radio" aria-checked="false"
                data-filter="bi-products" id="filter-bi"
                data-i18n="projects.filter.bi">BI Products</button>
        <button class="projects__filter"
                role="radio" aria-checked="false"
                data-filter="automation" id="filter-automation"
                data-i18n="projects.filter.automation">Automação</button>
        <button class="projects__filter"
                role="radio" aria-checked="false"
                data-filter="ai-solutions" id="filter-ai"
                data-i18n="projects.filter.ai">IA</button>
        <button class="projects__filter"
                role="radio" aria-checked="false"
                data-filter="data-engineering" id="filter-data"
                data-i18n="projects.filter.data">Data Engineering</button>
      </div>
    </div>

    <!-- Project grid -->
    <div class="projects__grid" role="list" aria-label="Project list">
      <!-- Repeated for each project -->
      <article class="project-card" role="listitem"
               data-category="bi-products" data-project-id="quote-flow-tracker"
               id="project-quote-flow-tracker" tabindex="0">
        <div class="project-card__header">
          <span class="project-card__category-badge"
                data-i18n-dynamic="project.category">
            Produtos de BI
          </span>
          <span class="project-card__date">ago 2023 – presente</span>
        </div>

        <h3 class="project-card__title" data-i18n-dynamic="project.title">
          Quote Flow Tracker
        </h3>

        <p class="project-card__description" data-i18n-dynamic="project.shortDescription">
          Produto de BI que monitora e analisa 45.000+ linhas de cotações/mês...
        </p>

        <div class="project-card__metrics">
          <div class="project-card__metric">
            <span class="project-card__metric-value">45.000+</span>
            <span class="project-card__metric-label"
                  data-i18n-dynamic="project.metric.1.label">linhas/mês</span>
          </div>
          <div class="project-card__metric">
            <span class="project-card__metric-value">~50%</span>
            <span class="project-card__metric-label"
                  data-i18n-dynamic="project.metric.2.label">redução no tempo</span>
          </div>
        </div>

        <div class="project-card__technologies">
          <span class="tech-badge">Power BI</span>
          <span class="tech-badge">DAX</span>
          <span class="tech-badge">SAP BW</span>
        </div>

        <button class="project-card__expand-btn"
                aria-label="View project details"
                data-i18n="projects.viewDetails" id="expand-quote-flow">
          Ver detalhes →
        </button>
      </article>
      <!-- End repeated -->
    </div>
  </div>
</section>

<!-- Project detail modal -->
<div class="project-modal" id="project-modal" role="dialog"
     aria-modal="true" aria-labelledby="project-modal-title" hidden>
  <div class="project-modal__overlay" id="project-modal-overlay"></div>
  <div class="project-modal__content">
    <button class="project-modal__close" id="project-modal-close"
            aria-label="Close project details">&times;</button>
    <div class="project-modal__body" id="project-modal-body">
      <!-- Dynamically populated from project data -->
    </div>
  </div>
</div>
```

### Behavior
- Filter buttons toggle active state and filter grid with CSS animations.
- Filtered-out cards animate out (scale + fade), filtered-in cards animate in.
- Project cards have hover effect: lift + accent border glow + subtle shadow.
- Clicking a card or "View details" opens a modal with full project information.
- Modal includes: full description, all metrics, all technologies, timeline,
  association, and detailed highlights.
- Modal closes via close button, overlay click, or Escape key.
- Focus is trapped within modal while open (accessibility).

### Responsive Breakpoints
- `≥ 1024px`: 3-column grid.
- `768px–1023px`: 2-column grid.
- `< 768px`: Single column, full-width cards.
- Filters: horizontal scroll on mobile with overflow-x auto.

### Card Visual Design
- Background: `var(--color-bg-secondary)` with subtle border.
- Hover: `translateY(-4px)`, `box-shadow` increase, border color accent.
- Metrics displayed with larger font and accent color for values.
- Tech badges: pill-shaped, muted background, small text.
- Category badge: top-left, colored per category.

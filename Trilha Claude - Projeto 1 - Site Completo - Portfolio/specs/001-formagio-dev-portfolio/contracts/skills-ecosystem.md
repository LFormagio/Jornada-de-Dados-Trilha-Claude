# Contract: Skills Ecosystem

## Component: `SkillsEcosystem`

### Purpose
Visual display of technical and soft skills organized by category,
with project cross-references showing practical application context.

### HTML Structure
```html
<section id="skills" class="skills section" aria-labelledby="skills-heading">
  <div class="section__container">
    <h2 id="skills-heading" class="section__title" data-i18n="skills.title">
      Skills & Tecnologias
    </h2>
    <p class="section__subtitle" data-i18n="skills.subtitle">
      Ferramentas e competências aplicadas em projetos reais
    </p>

    <div class="skills__grid">
      <!-- One group per category -->
      <div class="skills__category" id="skills-bi-analytics">
        <h3 class="skills__category-title" data-i18n="skills.category.bi">
          BI & Analytics
        </h3>
        <div class="skills__badges" role="list">
          <div class="skill-badge skill-badge--primary" role="listitem"
               data-skill-id="power-bi" id="skill-power-bi" tabindex="0">
            <img class="skill-badge__icon" src="/assets/icons/power-bi.svg"
                 alt="" width="24" height="24" aria-hidden="true" />
            <span class="skill-badge__name">Power BI</span>
            <div class="skill-badge__tooltip" role="tooltip">
              <span data-i18n="skills.usedIn">Usado em:</span>
              <ul>
                <li>Quote Flow Tracker</li>
                <li>Sales Data Intelligence System</li>
                <li>Customer Financial Overview Suite</li>
              </ul>
            </div>
          </div>
          <!-- More skill badges -->
        </div>
      </div>
      <!-- More categories: Data Engineering, Automation, AI & ML, Programming, ERP/SAP -->
    </div>
  </div>
</section>
```

### Behavior
- Skills are grouped by category in a responsive grid.
- Primary skills (`skill-badge--primary`) have larger size, accent border,
  and prominent visual weight.
- Hovering/focusing a skill badge shows a tooltip listing related projects.
- Scroll-reveal animation for each category group (staggered).
- Skill badges have subtle scale(1.05) hover effect.

### Responsive Breakpoints
- `≥ 1024px`: 3-column category grid.
- `768px–1023px`: 2-column category grid.
- `< 768px`: Single column, full-width categories.

---

# Contract: Certifications

## Component: `Certifications`

### Purpose
Display of 50+ certifications grouped by domain with filtering and
a compact expandable layout.

### HTML Structure
```html
<section id="certifications" class="certifications section"
         aria-labelledby="certifications-heading">
  <div class="section__container">
    <h2 id="certifications-heading" class="section__title"
        data-i18n="certifications.title">
      Certificações
    </h2>
    <p class="section__subtitle" data-i18n="certifications.subtitle">
      50+ certificações em contínua evolução
    </p>

    <!-- Certification Logos Grid -->
    <div class="certifications__grid" role="group" aria-label="Certification Issuers">
      <div class="cert-logo-card">
        <img src="/assets/icons/anthropic.svg" alt="Anthropic" width="48" height="48" loading="lazy" />
      </div>
      <div class="cert-logo-card">
        <img src="/assets/icons/microsoft.svg" alt="Microsoft" width="48" height="48" loading="lazy" />
      </div>
      <div class="cert-logo-card">
        <img src="/assets/icons/databricks.svg" alt="Databricks" width="48" height="48" loading="lazy" />
      </div>
      <div class="cert-logo-card">
        <img src="/assets/icons/nvidia.svg" alt="NVIDIA" width="48" height="48" loading="lazy" />
      </div>
      <!-- More issuer logos -->
      
      <div class="cert-count-badge">
        <span class="cert-count-badge__value">50+</span>
        <span class="cert-count-badge__label" data-i18n="certifications.total">Certificações</span>
      </div>
    </div>

    <!-- Show more button -->
    <button class="certifications__show-more" id="cert-show-more"
            data-i18n="certifications.showMore">
      Visualizar todas as certificações
    </button>
  </div>
</section>
```

### Behavior
- Grid displays prominent logos of certification issuers.
- The "50+" badge serves as a visual anchor emphasizing volume.
- Clicking "Visualizar todas as certificações" opens a full list view (modal or expandable section) with detailed credential cards.
- Count badge on section title shows total count.

### Responsive Breakpoints
- `≥ 1024px`: 5-column grid for logos.
- `768px–1023px`: 4-column grid.
- `< 768px`: 3-column grid.

# Contract: Experience Timeline

## Component: `ExperienceTimeline`

### Purpose
Vertical timeline displaying career progression at Avnet, with expandable
entries showing achievements and technologies.

### HTML Structure
```html
<section id="experience" class="experience section" aria-labelledby="experience-heading">
  <div class="section__container">
    <h2 id="experience-heading" class="section__title" data-i18n="experience.title">
      Experiência
    </h2>
    <p class="section__subtitle" data-i18n="experience.subtitle">
      Minha trajetória profissional
    </p>

    <div class="timeline" role="list" aria-label="Career timeline">
      <!-- Repeated for each experience entry -->
      <article class="timeline__item" role="listitem"
               data-experience-id="avnet" id="exp-avnet">
        <div class="timeline__marker" aria-hidden="true">
          <div class="timeline__dot"></div>
          <div class="timeline__line"></div>
        </div>

        <div class="timeline__card timeline__card--unified">
          <div class="timeline__header">
            <div class="timeline__company">
              <img class="timeline__company-logo" src="/assets/images/avnet-logo.webp"
                   alt="Avnet" width="40" height="40" loading="lazy" />
              <div class="timeline__company-info">
                <h3 class="timeline__company-name">Avnet</h3>
                <span class="timeline__duration" data-i18n-dynamic="experience.avnet.duration">
                  5 anos 10 meses
                </span>
              </div>
            </div>
          </div>

          <!-- Current/Primary Role -->
          <div class="timeline__role timeline__role--primary">
            <div class="timeline__role-header">
              <h4 class="timeline__title" data-i18n-dynamic="experience.bi-analyst.title">
                Analista de Business Intelligence
              </h4>
              <span class="timeline__date">nov 2022 – presente</span>
            </div>
            
            <p class="timeline__description" data-i18n-dynamic="experience.bi-analyst.description">
              Desenvolvimento e evolução de produtos de BI...
            </p>

            <button class="timeline__expand-btn" id="exp-expand-avnet"
                    aria-expanded="false"
                    aria-controls="exp-details-avnet"
                    data-i18n="experience.expand">
              Ver detalhes
            </button>

            <div class="timeline__details" id="exp-details-avnet" hidden aria-hidden="true">
              <ul class="timeline__achievements" role="list">
                <li class="timeline__achievement" data-i18n-dynamic="experience.achievement.1">
                  Liderança do ciclo ponta a ponta...
                </li>
              </ul>
              <div class="timeline__metrics">
                <div class="timeline__metric">
                  <span class="timeline__metric-value">140+</span>
                  <span class="timeline__metric-label" data-i18n="experience.metric.initiatives">iniciativas</span>
                </div>
              </div>
              <div class="timeline__technologies">
                <span class="timeline__tech-badge">Power BI</span>
                <span class="timeline__tech-badge">Microsoft Fabric</span>
              </div>
            </div>
          </div>

          <!-- Previous Roles (Compact) -->
          <div class="timeline__previous-roles">
            <div class="timeline__role timeline__role--compact">
              <div class="timeline__role-header">
                <h4 class="timeline__title" data-i18n-dynamic="experience.sales-rep.title">
                  Representante de Vendas Internas
                </h4>
                <span class="timeline__date">fev 2021 – out 2022</span>
              </div>
            </div>
            <div class="timeline__role timeline__role--compact">
              <div class="timeline__role-header">
                <h4 class="timeline__title" data-i18n-dynamic="experience.intern.title">
                  Estagiário de Vendas Internas
                </h4>
                <span class="timeline__date">mar 2019 – fev 2021</span>
              </div>
            </div>
          </div>
        </div>
      </article>
      <!-- End repeated -->
    </div>
  </div>
</section>
```

### Behavior
- Timeline entries appear with scroll-reveal animation (staggered).
- Timeline markers (dots + line) animate sequentially on scroll.
- Expand/collapse button toggles detail panel with slide-down animation.
- Technology badges use same visual style as project tech badges (consistency).
- Current position shows pulsing "active" dot indicator.

### Responsive Breakpoints
- `≥ 768px`: Timeline line on left, cards offset to the right.
- `< 768px`: Timeline line hidden, cards stack vertically as full-width cards.

# Contract: Hero Section

## Component: `Hero`

### Purpose
Full-viewport hero section that establishes Lucas's professional identity
at first glance. Includes name, headline, value proposition with animated
metrics, and a call-to-action.

### HTML Structure
```html
<section id="hero" class="hero" aria-labelledby="hero-heading">
  <div class="hero__container">
    <div class="hero__content">
      <div class="hero__greeting">
        <span class="hero__greeting-text" data-i18n="hero.greeting">
          Olá, eu sou
        </span>
      </div>

      <h1 id="hero-heading" class="hero__name">Lucas Formagio</h1>

      <p class="hero__headline" data-i18n="hero.headline">
        Analista de Business Intelligence
      </p>

      <p class="hero__tagline" data-i18n="hero.tagline">
        Transformo dados e processos em soluções escaláveis
      </p>

      <div class="hero__metrics" aria-label="Key achievements">
        <div class="hero__metric" id="hero-metric-1">
          <span class="hero__metric-value" data-count="4">4+</span>
          <span class="hero__metric-label" data-i18n="hero.metric.years">
            anos de experiência
          </span>
        </div>
        <div class="hero__metric" id="hero-metric-2">
          <span class="hero__metric-value" data-count="140">140+</span>
          <span class="hero__metric-label" data-i18n="hero.metric.initiatives">
            iniciativas gerenciadas
          </span>
        </div>
        <div class="hero__metric" id="hero-metric-3">
          <span class="hero__metric-value" data-count="85">85+</span>
          <span class="hero__metric-label" data-i18n="hero.metric.improvements">
            melhorias entregues
          </span>
        </div>
        <div class="hero__metric" id="hero-metric-4">
          <span class="hero__metric-value" data-count="18">18</span>
          <span class="hero__metric-label" data-i18n="hero.metric.automations">
            automações em produção
          </span>
        </div>
      </div>

      <div class="hero__actions">
        <a href="#projects" class="hero__cta hero__cta--primary"
           data-i18n="hero.cta.projects" id="hero-cta-projects">
          Ver Projetos
        </a>
        <a href="#contact" class="hero__cta hero__cta--secondary"
           data-i18n="hero.cta.contact" id="hero-cta-contact">
          Entre em Contato
        </a>
      </div>
    </div>

    <div class="hero__visual">
      <div class="hero__avatar-wrapper">
        <img class="hero__avatar" src="/assets/images/Linkedinpic-removebg-preview (2).png"
             alt="Lucas Formagio" width="400" height="400" />
        <div class="hero__avatar-glow" aria-hidden="true"></div>
      </div>
      <!-- Decorative data visualization elements -->
      <div class="hero__decoration" aria-hidden="true">
        <div class="hero__decoration-grid"></div>
        <div class="hero__decoration-dots"></div>
      </div>
    </div>
  </div>

  <div class="hero__scroll-indicator" aria-hidden="true">
    <span class="hero__scroll-text" data-i18n="hero.scroll">
      Role para baixo
    </span>
    <div class="hero__scroll-arrow"></div>
  </div>
</section>
```

### Behavior
- Full viewport height (`min-height: 100vh`).
- Staggered entrance animation: greeting → name → headline → metrics → CTAs.
- Metric values animate with count-up effect when hero enters viewport.
- Avatar is placed over subtle geometric data elements.
- Scroll indicator pulses softly at bottom center.
- CTAs have subtle hover scale.

### Responsive Breakpoints
- `≥ 1024px`: Two-column layout (content left, avatar right).
- `768px–1023px`: Stacked layout, centered, reduced avatar size.
- `< 768px`: Single column, smaller avatar, compact metrics grid (2×2).

### Animation Timeline
| Element | Delay | Duration | Effect |
|---------|-------|----------|--------|
| Greeting | 0ms | 600ms | fade-in + slide-up |
| Name | 200ms | 600ms | fade-in + slide-up |
| Headline | 400ms | 600ms | fade-in + slide-up |
| Tagline | 500ms | 600ms | fade-in + slide-up |
| Metrics | 700ms | 800ms | fade-in + count-up |
| CTAs | 900ms | 600ms | fade-in + slide-up |
| Avatar | 300ms | 1000ms | fade-in + scale(0.9→1) |
| Decoration | 500ms | 1200ms | fade-in |

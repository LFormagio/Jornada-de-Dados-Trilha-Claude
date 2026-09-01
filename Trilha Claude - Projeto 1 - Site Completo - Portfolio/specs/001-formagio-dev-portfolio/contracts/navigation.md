# Contract: Navigation System

## Component: `Navbar`

### Purpose
Sticky top navigation bar with logo/name, section links, language toggle,
and theme toggle. Uses glassmorphism backdrop blur effect.

### HTML Structure
```html
<nav id="navbar" class="navbar" role="navigation" aria-label="Main navigation">
  <div class="navbar__container">
    <a href="#hero" class="navbar__logo" aria-label="Lucas Formagio - Home">
      <span class="navbar__logo-text">LF</span>
      <span class="navbar__logo-name">Lucas Formagio</span>
    </a>

    <button class="navbar__toggle" id="nav-toggle"
            aria-expanded="false" aria-controls="nav-menu"
            aria-label="Toggle navigation menu">
      <span class="navbar__toggle-bar"></span>
      <span class="navbar__toggle-bar"></span>
      <span class="navbar__toggle-bar"></span>
    </button>

    <div class="navbar__menu" id="nav-menu" role="menubar">
      <a href="#projects" class="navbar__link" role="menuitem"
         data-i18n="nav.projects">Projetos</a>
      <a href="#experience" class="navbar__link" role="menuitem"
         data-i18n="nav.experience">Experiência</a>
      <a href="#skills" class="navbar__link" role="menuitem"
         data-i18n="nav.skills">Skills</a>
      <a href="#about" class="navbar__link" role="menuitem"
         data-i18n="nav.about">Sobre</a>
      <a href="#certifications" class="navbar__link" role="menuitem"
         data-i18n="nav.certifications">Certificações</a>
      <a href="#education" class="navbar__link" role="menuitem"
         data-i18n="nav.education">Formação</a>
      <a href="#contact" class="navbar__link" role="menuitem"
         data-i18n="nav.contact">Contato</a>
    </div>

    <div class="navbar__actions">
      <!-- Lang toggle component mounted here -->
      <div id="lang-toggle-mount"></div>
      <!-- Theme toggle component mounted here -->
      <div id="theme-toggle-mount"></div>
    </div>
  </div>
</nav>
```

### Behavior
- Sticky positioning with `position: sticky; top: 0`.
- Glassmorphism: `backdrop-filter: blur(12px)` with semi-transparent background.
- Active section highlighting via Intersection Observer on scroll.
- Smooth scroll to target section on link click.
- Mobile: hamburger toggle reveals full-screen overlay menu.
- Navbar shrinks (reduced padding) after scrolling past hero section.

### Responsive Breakpoints
- `≥ 1024px`: Full horizontal menu visible.
- `< 1024px`: Hamburger toggle, full-screen overlay menu.

---

## Component: `LangToggle`

### Purpose
Language switcher between PT-BR and EN-US.

### HTML Structure
```html
<div class="lang-toggle" id="lang-toggle" role="radiogroup"
     aria-label="Select language">
  <button class="lang-toggle__btn lang-toggle__btn--active"
          role="radio" aria-checked="true"
          data-lang="pt" id="lang-btn-pt">PT</button>
  <button class="lang-toggle__btn"
          role="radio" aria-checked="false"
          data-lang="en" id="lang-btn-en">EN</button>
</div>
```

### Behavior
- Clicking a language button triggers `i18n.setLocale(lang)`.
- Active button receives `--active` modifier class.
- URL updates to reflect locale prefix without page reload.
- Preference stored in `localStorage` as `preferred-lang`.

---

## Component: `ThemeToggle`

### Purpose
Dark/light mode switcher.

### HTML Structure
```html
<button class="theme-toggle" id="theme-toggle"
        aria-label="Toggle dark/light mode"
        aria-pressed="false">
  <svg class="theme-toggle__icon theme-toggle__icon--sun" aria-hidden="true">...</svg>
  <svg class="theme-toggle__icon theme-toggle__icon--moon" aria-hidden="true">...</svg>
</button>
```

### Behavior
- Toggles `data-theme="light"` attribute on `<html>`.
- Default: dark mode (no attribute or `data-theme="dark"`).
- Preference stored in `localStorage` as `preferred-theme`.
- Respects `prefers-color-scheme` media query on first visit.
- Smooth 300ms transition on all color custom properties.

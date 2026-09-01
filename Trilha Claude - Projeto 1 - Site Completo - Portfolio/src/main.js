// src/main.js
import './styles/index.css';

// Import Utilities
import { initTheme } from './utils/theme.js';
import { initScrollReveal } from './utils/scroll-reveal.js';
import * as i18n from './i18n/i18n.js';

// Import Components
import { initThemeToggle } from './components/theme-toggle/theme-toggle.js';
import { initLangToggle } from './components/lang-toggle/lang-toggle.js';
import { initNavbar } from './components/navbar/navbar.js';
import { initHero } from './components/hero/hero.js';
import { initProjects } from './components/projects/projects.js';
import { initExperience } from './components/experience/experience.js';
import { initSkills } from './components/skills/skills.js';
import { initAbout } from './components/about/about.js';
import { initCertifications } from './components/certifications/certifications.js';
import { initEducation } from './components/education/education.js';
import { initContact } from './components/contact/contact.js';

document.addEventListener('DOMContentLoaded', async () => {
  // 1. Initialize utilities (theme first to avoid flash)
  initTheme();
  
  // 2. Initialize i18n
  await i18n.init();
  
  // 3. Initialize components
  initThemeToggle();
  initLangToggle();
  initNavbar();
  initHero();
  initProjects();
  initExperience();
  initSkills();
  initAbout();
  initCertifications();
  initEducation();
  initContact();
  
  // 4. Initialize scroll animations
  initScrollReveal();

  console.log('App initialized');
});

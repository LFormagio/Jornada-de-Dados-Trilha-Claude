// src/components/about/about.js
import aboutData from '../../data/about.json';
import { getLocale } from '../../i18n/i18n.js';

export function initAbout() {
  const bioContainer = document.getElementById('about-bio');
  const langContainer = document.getElementById('about-languages');
  if (!bioContainer || !langContainer) return;

  renderAbout(bioContainer, langContainer);

  document.addEventListener('locale-changed', () => {
    renderAbout(bioContainer, langContainer);
  });
}

function renderAbout(bioContainer, langContainer) {
  const locale = getLocale();
  
  // Render bio
  bioContainer.textContent = aboutData.bio[locale] || aboutData.bio['pt'];

  // Render languages
  langContainer.innerHTML = '';
  aboutData.languages.forEach(lang => {
    const el = document.createElement('div');
    el.className = 'language-badge anim-fade-up';
    el.innerHTML = `
      <span class="language-badge__name">${lang.name[locale] || lang.name['pt']}</span>
      <span class="language-badge__level">${lang.level[locale] || lang.level['pt']}</span>
    `;
    langContainer.appendChild(el);
  });
}

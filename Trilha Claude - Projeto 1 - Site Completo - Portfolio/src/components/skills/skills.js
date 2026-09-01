// src/components/skills/skills.js
import skillsData from '../../data/skills.json';
import { getLocale, t } from '../../i18n/i18n.js';

export function initSkills() {
  const container = document.getElementById('skills-container');
  if (!container) return;

  const categoryStates = {};
  skillsData.forEach((_, idx) => {
    categoryStates[idx] = false; // false = hide non-primary
  });

  const render = () => {
    const locale = getLocale();
    container.innerHTML = '';
    
    skillsData.forEach((cat, idx) => {
      const el = document.createElement('div');
      el.className = 'skill-category anim-in';
      el.style.animationDelay = `${idx * 50}ms`;
      
      const showAll = categoryStates[idx];
      const primarySkills = cat.skills.filter(s => s.primary);
      const visibleSkills = showAll ? cat.skills : primarySkills;
      
      const hasMore = cat.skills.length > primarySkills.length;
      
      let skillsHtml = '';
      visibleSkills.forEach(skill => {
        const className = skill.primary ? 'skill-badge skill-badge--primary' : 'skill-badge';
        skillsHtml += `<span class="${className}">${skill.name}</span>`;
      });
      
      el.innerHTML = `
        <h3 class="skill-category__title">${cat.category[locale] || cat.category['pt']}</h3>
        <div class="skill-category__list">
          ${skillsHtml}
        </div>
        ${hasMore && !showAll ? `<button class="skill-category__btn-more">Ver mais</button>` : ''}
      `;
      
      container.appendChild(el);
      
      const btn = el.querySelector('.skill-category__btn-more');
      if (btn) {
        btn.addEventListener('click', () => {
          categoryStates[idx] = true;
          render();
        });
      }
    });
  };

  render();
  document.addEventListener('locale-changed', render);
}

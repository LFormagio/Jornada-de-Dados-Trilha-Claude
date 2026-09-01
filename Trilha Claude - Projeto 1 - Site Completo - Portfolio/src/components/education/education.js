// src/components/education/education.js
import eduData from '../../data/education.json';
import { getLocale } from '../../i18n/i18n.js';

export function initEducation() {
  const container = document.getElementById('education-container');
  if (!container) return;

  renderEducation(container);

  document.addEventListener('locale-changed', () => {
    renderEducation(container);
  });
}

function renderEducation(container) {
  const locale = getLocale();
  container.innerHTML = '';

  eduData.forEach(edu => {
    const el = document.createElement('div');
    el.className = 'edu-card anim-fade-up';
    
    let highlightsHtml = '';
    if (edu.highlights) {
      edu.highlights.forEach(h => {
        highlightsHtml += `<li class="edu-card__highlight">${h[locale] || h['pt']}</li>`;
      });
    }

    el.innerHTML = `
      <div class="edu-card__header">
        <div class="edu-card__title">
          <h3 class="edu-card__degree">${edu.degree[locale] || edu.degree['pt']}</h3>
          <span class="edu-card__institution">${edu.institution}</span>
        </div>
        <div class="edu-card__date">${typeof edu.date === 'string' ? edu.date : (edu.date[locale] || edu.date['pt'])}</div>
      </div>
      <p class="edu-card__description">${edu.description[locale] || edu.description['pt']}</p>
      ${highlightsHtml ? `<ul class="edu-card__highlights">${highlightsHtml}</ul>` : ''}
    `;
    
    container.appendChild(el);
  });
}

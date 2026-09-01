// src/components/experience/experience.js
import expData from '../../data/experience.json';
import { getLocale } from '../../i18n/i18n.js';

export function initExperience() {
  const container = document.querySelector('.timeline');
  if (!container) return;

  renderExperience(expData, container);

  document.addEventListener('locale-changed', () => {
    // Preserve expanded state before re-rendering
    const expandedIds = [];
    document.querySelectorAll('.timeline__expand-btn').forEach(btn => {
      if (btn.getAttribute('aria-expanded') === 'true') {
        expandedIds.push(btn.id.replace('exp-expand-', ''));
      }
    });

    renderExperience(expData, container);

    // Restore expanded state
    expandedIds.forEach(id => {
      const btn = document.getElementById(`exp-expand-${id}`);
      if (btn) {
        btn.setAttribute('aria-expanded', 'true');
        const details = document.getElementById(`exp-details-${id}`);
        if (details) {
          details.removeAttribute('hidden');
          details.setAttribute('aria-hidden', 'false');
          btn.textContent = getLocale() === 'pt' ? 'Ocultar detalhes' : 'Hide details';
        }
      }
    });
  });
}

function renderExperience(data, container) {
  const locale = getLocale();
  container.innerHTML = '';

  data.forEach(exp => {
    const article = document.createElement('article');
    article.className = 'timeline__item anim-fade-up';
    article.setAttribute('role', 'listitem');
    article.id = `exp-${exp.id}`;

    // Achievements
    let achievementsHtml = '';
    exp.primaryRole.achievements.forEach(ach => {
      achievementsHtml += `<li class="timeline__achievement">${ach[locale] || ach['pt']}</li>`;
    });

    // Metrics
    let metricsHtml = '';
    if (exp.primaryRole.metrics) {
      exp.primaryRole.metrics.forEach(m => {
        metricsHtml += `
          <div class="timeline__metric">
            <span class="timeline__metric-value">${m.value}</span>
            <span class="timeline__metric-label">${m.label[locale] || m.label['pt']}</span>
          </div>
        `;
      });
    }

    // Tech
    let techHtml = '';
    const MAX_VISIBLE_TECH = 5;
    
    if (exp.primaryRole.technologies && exp.primaryRole.technologies.length > 0) {
      const visibleTech = exp.primaryRole.technologies.slice(0, MAX_VISIBLE_TECH);
      const hiddenTech = exp.primaryRole.technologies.slice(MAX_VISIBLE_TECH);
      
      let visibleHtml = '';
      visibleTech.forEach(tech => {
        visibleHtml += `<span class="tech-badge">${tech}</span>`;
      });
      
      let hiddenHtml = '';
      hiddenTech.forEach(tech => {
        hiddenHtml += `<span class="tech-badge">${tech}</span>`;
      });
      
      if (hiddenTech.length > 0) {
        techHtml = `
          <div class="experience-card__tech">
            <div class="tech-visible" style="display:flex; flex-wrap:wrap; gap:var(--spacing-2); margin-bottom:var(--spacing-2);">${visibleHtml}</div>
            <div class="tech-hidden" style="display:none; flex-wrap:wrap; gap:var(--spacing-2); margin-bottom:var(--spacing-2);">${hiddenHtml}</div>
            <button class="tech-toggle-btn" style="background:none; border:none; color:var(--color-primary); font-size:var(--font-size-xs); cursor:pointer; padding:0; font-weight:bold; text-decoration:underline;">${locale === 'pt' ? 'Ver mais' : 'View more'} (${hiddenTech.length})</button>
          </div>
        `;
      } else {
        techHtml = `
          <div class="experience-card__tech">
            <div style="display:flex; flex-wrap:wrap; gap:var(--spacing-2);">${visibleHtml}</div>
          </div>
        `;
      }
    }

    // Previous Roles
    let previousRolesHtml = '';
    if (exp.previousRoles && exp.previousRoles.length > 0) {
      let rolesHtml = '';
      exp.previousRoles.forEach(role => {
        let techBadges = '';
        if (role.technologies) {
          role.technologies.forEach(t => {
            techBadges += `<span class="timeline__tech-badge tech-badge">${t}</span>`;
          });
        }
        
        rolesHtml += `
          <div class="timeline__role timeline__role--compact">
            <div class="timeline__role-header">
              <h4 class="timeline__title">${role.title[locale] || role.title['pt']}</h4>
              <span class="timeline__date">${role.date[locale] || role.date['pt']}</span>
            </div>
            ${role.description ? `<p class="timeline__description">${role.description[locale] || role.description['pt']}</p>` : ''}
            ${techBadges ? `<div class="timeline__technologies">${techBadges}</div>` : ''}
          </div>
        `;
      });
      previousRolesHtml = `
        <div class="timeline__previous-roles">
          ${rolesHtml}
        </div>
      `;
    }

    const expandText = locale === 'pt' ? 'Ver detalhes' : 'View details';

    // Since we don't have the logo image (avnet-logo.png), we will use an initial letter or generic icon
    const companyInitial = exp.company.charAt(0);

    article.innerHTML = `
      <div class="timeline__marker" aria-hidden="true">
        <div class="timeline__dot"></div>
        <div class="timeline__line"></div>
      </div>

      <div class="timeline__card timeline__card--unified">
        <div class="timeline__header">
          <div class="timeline__company">
            <div style="width: 40px; height: 40px; background: var(--color-bg-primary); color: var(--color-accent-primary); display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 4px; font-size: 20px;">
              ${companyInitial}
            </div>
            <div class="timeline__company-info">
              <h3 class="timeline__company-name">${exp.company}</h3>
              <span class="timeline__duration">${exp.duration[locale] || exp.duration['pt']}</span>
            </div>
          </div>
        </div>

        <div class="timeline__role timeline__role--primary">
          <div class="timeline__role-header">
            <h4 class="timeline__title">${exp.primaryRole.title[locale] || exp.primaryRole.title['pt']}</h4>
            <span class="timeline__date">${exp.primaryRole.date[locale] || exp.primaryRole.date['pt']}</span>
          </div>
          
          <p class="timeline__description">${exp.primaryRole.description[locale] || exp.primaryRole.description['pt']}</p>

          <button class="timeline__expand-btn" id="exp-expand-${exp.id}" aria-expanded="false" aria-controls="exp-details-${exp.id}">
            ${expandText}
          </button>

          <div class="timeline__details" id="exp-details-${exp.id}" hidden aria-hidden="true">
            <ul class="timeline__achievements" role="list">
              ${achievementsHtml}
            </ul>
            <div class="timeline__metrics">
              ${metricsHtml}
            </div>
            <div class="timeline__technologies">
              ${techHtml}
            </div>
          </div>
        </div>
        
        ${previousRolesHtml}
      </div>
    `;

    container.appendChild(article);

    // Add toggle event listener
    const toggleBtn = article.querySelector('.tech-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const hiddenDiv = article.querySelector('.tech-hidden');
        const isHidden = hiddenDiv.style.display === 'none';
        
        if (isHidden) {
          hiddenDiv.style.display = 'flex';
          e.target.textContent = locale === 'pt' ? 'Ver menos' : 'View less';
        } else {
          hiddenDiv.style.display = 'none';
          const hiddenCount = exp.primaryRole.technologies.length - MAX_VISIBLE_TECH;
          e.target.textContent = `${locale === 'pt' ? 'Ver mais' : 'View more'} (${hiddenCount})`;
        }
      });
    }
  });

  // Setup expand listeners
  container.querySelectorAll('.timeline__expand-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const isExpanded = btn.getAttribute('aria-expanded') === 'true';
      const controlsId = btn.getAttribute('aria-controls');
      const details = document.getElementById(controlsId);
      
      if (isExpanded) {
        btn.setAttribute('aria-expanded', 'false');
        details.setAttribute('hidden', '');
        details.setAttribute('aria-hidden', 'true');
        btn.textContent = getLocale() === 'pt' ? 'Ver detalhes' : 'View details';
      } else {
        btn.setAttribute('aria-expanded', 'true');
        details.removeAttribute('hidden');
        details.setAttribute('aria-hidden', 'false');
        btn.textContent = getLocale() === 'pt' ? 'Ocultar detalhes' : 'Hide details';
      }
    });
  });
}

// src/components/projects/projects.js
import projectsData from '../../data/projects.json';
import { getLocale } from '../../i18n/i18n.js';

export function initProjects() {
  const grid = document.querySelector('.projects__grid');
  const filters = document.querySelectorAll('.projects__filter');
  
  if (!grid) return;

  // Render initial projects
  renderProjects(projectsData, grid);

  // Setup filters
  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update active state
      filters.forEach(f => {
        f.classList.remove('projects__filter--active');
        f.setAttribute('aria-checked', 'false');
      });
      btn.classList.add('projects__filter--active');
      btn.setAttribute('aria-checked', 'true');

      // Filter data
      const filterValue = btn.getAttribute('data-filter');
      const filtered = filterValue === 'all' 
        ? projectsData 
        : projectsData.filter(p => p.category === filterValue);

      // Animate out
      const cards = grid.querySelectorAll('.project-card');
      cards.forEach(card => card.classList.add('anim-out'));

      // Wait for animation then re-render
      setTimeout(() => {
        renderProjects(filtered, grid);
      }, 300);
    });
  });

  // Listen for locale changes to re-render
  document.addEventListener('locale-changed', () => {
    const activeFilterBtn = document.querySelector('.projects__filter--active');
    const filterValue = activeFilterBtn ? activeFilterBtn.getAttribute('data-filter') : 'all';
    const filtered = filterValue === 'all' 
        ? projectsData 
        : projectsData.filter(p => p.category === filterValue);
    
    // We update without animation on language change
    renderProjects(filtered, grid);
  });
}

function renderProjects(projects, container) {
  const locale = getLocale();
  container.innerHTML = '';
  
  projects.forEach(project => {
    const card = document.createElement('article');
    card.className = 'project-card anim-in';
    card.setAttribute('role', 'listitem');
    card.setAttribute('data-category', project.category);
    card.setAttribute('tabindex', '0');

    // Build category badge string (mapping internal to display)
    const categoryDisplayMap = {
      'bi-products': 'BI Products',
      'automation': 'Automação',
      'ai-solutions': 'IA',
      'data-engineering': 'Data Engineering'
    };
    
    let metricsHtml = '';
    project.metrics.forEach(m => {
      metricsHtml += `
        <div class="project-card__metric">
          <span class="project-card__metric-value">${m.value}</span>
          <span class="project-card__metric-label">${m.label[locale] || m.label['pt']}</span>
        </div>
      `;
    });

    let techsHtml = '';
    const MAX_VISIBLE_TECH = 3;
    
    if (project.technologies && project.technologies.length > 0) {
      const visibleTech = project.technologies.slice(0, MAX_VISIBLE_TECH);
      const hiddenTech = project.technologies.slice(MAX_VISIBLE_TECH);
      
      let visibleHtml = '';
      visibleTech.forEach(tech => {
        visibleHtml += `<span class="tech-badge">${tech}</span>`;
      });
      
      let hiddenHtml = '';
      hiddenTech.forEach(tech => {
        hiddenHtml += `<span class="tech-badge">${tech}</span>`;
      });
      
      if (hiddenTech.length > 0) {
        techsHtml = `
          <div class="project-card__tech">
            <div class="tech-visible" style="display:flex; flex-wrap:wrap; gap:var(--spacing-2); margin-bottom:var(--spacing-2);">${visibleHtml}</div>
            <div class="tech-hidden" style="display:none; flex-wrap:wrap; gap:var(--spacing-2); margin-bottom:var(--spacing-2);">${hiddenHtml}</div>
            <button class="tech-toggle-btn" style="background:none; border:none; color:var(--color-primary); font-size:var(--font-size-xs); cursor:pointer; padding:0; font-weight:bold; text-decoration:underline;">${locale === 'pt' ? 'Ver mais' : 'View more'} (${hiddenTech.length})</button>
          </div>
        `;
      } else {
        techsHtml = `
          <div class="project-card__tech">
            <div style="display:flex; flex-wrap:wrap; gap:var(--spacing-2);">${visibleHtml}</div>
          </div>
        `;
      }
    }

    card.innerHTML = `
      <div class="project-card__header">
        <span class="project-card__category-badge">${categoryDisplayMap[project.category] || project.category}</span>
        <span class="project-card__date">${project.date}</span>
      </div>
      <h3 class="project-card__title">${project.title}</h3>
      <p class="project-card__description">${project.shortDescription[locale] || project.shortDescription['pt']}</p>
      
      <div class="project-card__metrics">
        ${metricsHtml}
      </div>
      
      <div class="project-card__technologies" style="margin-bottom: var(--spacing-6);">
        ${techsHtml}
      </div>
    `;
    
    container.appendChild(card);
    
    // Add toggle event listener
    const toggleBtn = card.querySelector('.tech-toggle-btn');
    if (toggleBtn) {
      // Prevent card click when clicking the button
      toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const hiddenDiv = card.querySelector('.tech-hidden');
        const isHidden = hiddenDiv.style.display === 'none';
        
        if (isHidden) {
          hiddenDiv.style.display = 'flex';
          e.target.textContent = locale === 'pt' ? 'Ver menos' : 'View less';
        } else {
          hiddenDiv.style.display = 'none';
          const hiddenCount = project.technologies.length - MAX_VISIBLE_TECH;
          e.target.textContent = `${locale === 'pt' ? 'Ver mais' : 'View more'} (${hiddenCount})`;
        }
      });
    }
  });
}

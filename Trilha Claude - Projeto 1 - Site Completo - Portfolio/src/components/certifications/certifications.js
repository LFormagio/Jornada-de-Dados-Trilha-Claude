// src/components/certifications/certifications.js
import certsData from '../../data/certifications.json';

export function initCertifications() {
  const container = document.getElementById('certs-container');
  const btnShowAll = document.getElementById('btn-show-all-certs');
  if (!container) return;

  let showAll = false;

  const render = () => {
    container.innerHTML = '';
    const visibleCerts = showAll ? certsData : certsData.slice(0, 4);
    
    visibleCerts.forEach((cert, index) => {
      const el = document.createElement('div');
      el.className = 'cert-card anim-in';
      // Add a slight delay for subsequent cards
      if (index >= 4) {
        el.style.animationDelay = `${(index - 4) * 50}ms`;
      }
      el.innerHTML = `
        <div class="cert-card__name">${cert.name}</div>
        <div class="cert-card__meta">
          <span class="cert-card__issuer">${cert.issuer}</span>
          <span class="cert-card__date">${cert.date}</span>
        </div>
      `;
      container.appendChild(el);
    });

    if (btnShowAll) {
      if (showAll || certsData.length <= 4) {
        btnShowAll.style.display = 'none';
      } else {
        btnShowAll.style.display = 'inline-block';
      }
    }
  };

  render();

  if (btnShowAll) {
    btnShowAll.addEventListener('click', () => {
      showAll = true;
      render();
    });
  }
}

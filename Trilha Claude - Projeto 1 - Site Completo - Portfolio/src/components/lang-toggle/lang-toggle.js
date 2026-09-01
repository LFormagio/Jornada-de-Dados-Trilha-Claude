// src/components/lang-toggle/lang-toggle.js
import { getLocale, setLocale } from '../../i18n/i18n.js';

export function initLangToggle() {
  const toggleGroup = document.getElementById('lang-toggle');
  if (!toggleGroup) return;

  const btns = toggleGroup.querySelectorAll('.lang-toggle__btn');
  
  function updateActiveState(locale) {
    btns.forEach(btn => {
      const isActive = btn.dataset.lang === locale;
      btn.classList.toggle('lang-toggle__btn--active', isActive);
      btn.setAttribute('aria-checked', isActive);
    });
  }

  // Initial state
  updateActiveState(getLocale());

  // Listen for clicks
  btns.forEach(btn => {
    btn.addEventListener('click', async () => {
      const newLocale = btn.dataset.lang;
      if (newLocale !== getLocale()) {
        await setLocale(newLocale);
        updateActiveState(newLocale);
      }
    });
  });

  // Also listen for external locale changes
  document.addEventListener('locale-changed', (e) => {
    updateActiveState(e.detail.locale);
  });
}

// src/utils/theme.js
export function initTheme() {
  const toggleBtn = document.getElementById('theme-toggle');
  
  // Dark mode is default
  let currentTheme = localStorage.getItem('theme') || 'dark';
  
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  // Initial apply
  applyTheme(currentTheme);

  // Setup toggle if element exists
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(currentTheme);
    });
  }
}

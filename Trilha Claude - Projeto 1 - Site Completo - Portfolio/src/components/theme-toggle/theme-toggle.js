// src/components/theme-toggle/theme-toggle.js
export function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;
  
  function updateIcon(theme) {
    const isDark = theme === 'dark';
    toggleBtn.setAttribute('aria-pressed', !isDark);
    
    const sun = toggleBtn.querySelector('.theme-toggle__icon--sun');
    const moon = toggleBtn.querySelector('.theme-toggle__icon--moon');
    
    if (sun && moon) {
      sun.style.display = isDark ? 'block' : 'none';
      moon.style.display = isDark ? 'none' : 'block';
    }
  }

  // Initial state
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
  updateIcon(currentTheme);

  // The actual toggling is handled in src/utils/theme.js, but we need to listen
  // to changes to update the icon if it wasn't handled there.
  // We can just add the click listener here to update the icon
  toggleBtn.addEventListener('click', () => {
    // Small timeout to let theme.js update the attribute first
    setTimeout(() => {
      const theme = document.documentElement.getAttribute('data-theme');
      updateIcon(theme);
    }, 10);
  });
}

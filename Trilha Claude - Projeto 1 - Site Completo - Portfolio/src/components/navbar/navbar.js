// src/components/navbar/navbar.js
export function initNavbar() {
  const navbar = document.getElementById('navbar');
  const toggleBtn = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  const links = document.querySelectorAll('.navbar__link');

  if (!navbar) return;

  // Shrink navbar on scroll
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('navbar--scrolled');
    } else {
      navbar.classList.remove('navbar--scrolled');
    }
  }, { passive: true });

  // Mobile menu toggle
  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
      toggleBtn.setAttribute('aria-expanded', !isExpanded);
      
      // Toggle via CSS class instead of inline styles
      navMenu.classList.toggle('navbar__menu--open', !isExpanded);
    });
  }

  // Handle window resize to reset mobile menu state
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024 && navMenu && navMenu.classList.contains('navbar__menu--open')) {
      navMenu.classList.remove('navbar__menu--open');
      if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });

  // Smooth scroll for internal links
  const smoothLinks = document.querySelectorAll('a[href^="#"]');
  smoothLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href').substring(1);
      if (!targetId) return;
      const targetEl = document.getElementById(targetId);
      
      if (targetEl) {
        e.preventDefault();
        const navHeight = navbar.offsetHeight;
        const targetPos = targetEl.getBoundingClientRect().top + window.scrollY - navHeight;
        
        window.scrollTo({
          top: targetPos,
          behavior: 'smooth'
        });
        
        // Update URL hash without jumping
        if (history.pushState) {
          history.pushState(null, null, '#' + targetId);
        } else {
          window.location.hash = '#' + targetId;
        }

        // Close mobile menu if open
        if (toggleBtn && toggleBtn.getAttribute('aria-expanded') === 'true') {
          toggleBtn.click();
        }
      }
    });
  });

  // Active section highlighting (Intersection Observer)
  const sections = document.querySelectorAll('section[id]');
  if (sections.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          links.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
          });
        }
      });
    }, { rootMargin: '-20% 0px -80% 0px' });

    sections.forEach(sec => observer.observe(sec));
  }
}

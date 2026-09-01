// src/components/hero/hero.js
import { initParticles } from '../../utils/particles.js';
import { initWordCloud } from '../../utils/wordcloud.js';

export function initHero() {
  const hero = document.querySelector('.hero');
  if (!hero) return;

  // Initialize background particles
  initParticles('hero-particles');

  // Initialize 3D Word Cloud
  const competencies = [
    'Power BI', 'Fabric', 'DAX', 'Python', 'SQL', 
    'Analytics Engineering', 'Data Warehousing', 'Data Lakes',
    'ETL', 'SAP BW', 'Power Automate', 'Machine Learning', 
    'Databricks', 'RPA', 'Data Visualization', 'Scikit-Learn',
    'Azure', 'Big Data', 'Dashboarding', 'Business Intelligence'
  ];
  initWordCloud('hero-wordcloud', competencies);

  const metrics = document.querySelectorAll('.hero__metric-value');
  
  if (metrics.length === 0) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateMetrics(metrics);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  // Observe the metrics container
  const metricsContainer = document.querySelector('.hero__metrics');
  if (metricsContainer) {
    observer.observe(metricsContainer);
  }
}

function animateMetrics(metrics) {
  metrics.forEach(metric => {
    const targetValue = parseInt(metric.getAttribute('data-count'), 10);
    if (isNaN(targetValue)) return;
    
    const suffix = metric.textContent.replace(/[0-9]/g, ''); // keep +, % etc.
    const duration = 1500; // ms
    const steps = 60;
    const stepTime = Math.abs(Math.floor(duration / steps));
    let current = 0;
    
    const timer = setInterval(() => {
      current += Math.ceil(targetValue / steps);
      if (current >= targetValue) {
        metric.textContent = targetValue + suffix;
        clearInterval(timer);
      } else {
        metric.textContent = current + suffix;
      }
    }, stepTime);
  });
}

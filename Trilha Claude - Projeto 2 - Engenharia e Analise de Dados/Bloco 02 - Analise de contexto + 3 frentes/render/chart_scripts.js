// render/chart_scripts.js

// Configurações globais do Chart.js para o Open Design Dark Mode
Chart.defaults.color = '#a1a1aa';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(9, 9, 11, 0.9)';
Chart.defaults.plugins.tooltip.titleFont = { family: "'Outfit', sans-serif", size: 14 };
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.1)';
Chart.defaults.plugins.tooltip.borderWidth = 1;

// 1. Gráfico de Categorias (Bar Chart)
const ctxCategory = document.getElementById('categoryChart').getContext('2d');
new Chart(ctxCategory, {
  type: 'bar',
  data: {
    labels: chartData.categories.labels,
    datasets: [{
      label: 'Faturamento (R$)',
      data: chartData.categories.values,
      backgroundColor: 'rgba(79, 209, 197, 0.8)', // accent-primary
      hoverBackgroundColor: 'rgba(79, 209, 197, 1)',
      borderRadius: 6,
      borderSkipped: false
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.05)',
          drawBorder: false
        }
      },
      x: {
        grid: {
          display: false,
          drawBorder: false
        }
      }
    },
    plugins: {
      legend: {
        display: false
      }
    }
  }
});

// 2. Gráfico de Canais (Doughnut Chart)
const ctxChannel = document.getElementById('channelChart').getContext('2d');
new Chart(ctxChannel, {
  type: 'doughnut',
  data: {
    labels: chartData.channels.labels,
    datasets: [{
      data: chartData.channels.values,
      backgroundColor: [
        'rgba(99, 102, 241, 0.8)', // accent-secondary
        'rgba(79, 209, 197, 0.8)', // accent-primary
        'rgba(16, 185, 129, 0.8)'  // success
      ],
      borderWidth: 0,
      hoverOffset: 4
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle'
        }
      }
    }
  }
});

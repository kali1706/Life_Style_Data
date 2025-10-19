window.renderDashboardCharts = function (w) {
  const macroCtx = document.getElementById('macroChart');
  if (macroCtx) {
    new Chart(macroCtx, {
      type: 'pie',
      data: {
        labels: ['Carbs', 'Protein', 'Fat'],
        datasets: [{
          data: [w.macro_avg.carbs, w.macro_avg.protein, w.macro_avg.fat],
          backgroundColor: ['#45aaf2', '#2ecc71', '#f1c40f']
        }]
      },
      options: { responsive: true }
    });
  }

  const calorieCtx = document.getElementById('calorieChart');
  if (calorieCtx) {
    new Chart(calorieCtx, {
      type: 'bar',
      data: {
        labels: ['Burned', 'Intake'],
        datasets: [{
          label: 'kcal',
          data: [w.calories_burned, w.avg_daily_intake],
          backgroundColor: ['#e74c3c', '#8e44ad']
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    });
  }
}

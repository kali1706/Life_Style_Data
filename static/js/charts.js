// Charts.js - Custom JavaScript for Lifestyle Analytics Platform

// Global Chart Configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#495057';

// Color Palette
const colors = {
    primary: '#007bff',
    success: '#28a745',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
    gradients: {
        primary: ['#007bff', '#0056b3'],
        success: ['#28a745', '#1e7e34'],
        warning: ['#ffc107', '#e0a800'],
        danger: ['#dc3545', '#c82333'],
        info: ['#17a2b8', '#117a8b']
    }
};

// Utility Functions
function createGradient(ctx, color1, color2, vertical = true) {
    const gradient = vertical 
        ? ctx.createLinearGradient(0, 0, 0, 400)
        : ctx.createLinearGradient(0, 0, 400, 0);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}

// Dashboard Charts
class DashboardCharts {
    constructor() {
        this.charts = {};
        this.initializeCharts();
    }

    initializeCharts() {
        this.createWeeklyOverviewChart();
        this.createCalorieBalanceChart();
        this.createMacroBreakdownChart();
        this.createHeartRateZoneChart();
        this.createProgressChart();
    }

    createWeeklyOverviewChart() {
        const ctx = document.getElementById('weeklyOverviewChart');
        if (!ctx) return;

        const gradient1 = createGradient(ctx.getContext('2d'), colors.primary, colors.gradients.primary[1]);
        const gradient2 = createGradient(ctx.getContext('2d'), colors.success, colors.gradients.success[1]);

        this.charts.weeklyOverview = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Calories Burned',
                    data: [300, 450, 200, 600, 400, 350, 500],
                    borderColor: colors.primary,
                    backgroundColor: gradient1,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }, {
                    label: 'Calories Consumed',
                    data: [2000, 1800, 2200, 1900, 2100, 2300, 2000],
                    borderColor: colors.success,
                    backgroundColor: gradient2,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: colors.success,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + formatNumber(context.parsed.y) + ' kcal';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            callback: function(value) {
                                return formatNumber(value);
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    createCalorieBalanceChart() {
        const ctx = document.getElementById('calorieBalanceChart');
        if (!ctx) return;

        this.charts.calorieBalance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Calorie Balance',
                    data: [200, -150, 300, -100, 250, 400, -50],
                    backgroundColor: function(context) {
                        const value = context.parsed.y;
                        return value >= 0 ? colors.success : colors.danger;
                    },
                    borderColor: function(context) {
                        const value = context.parsed.y;
                        return value >= 0 ? colors.gradients.success[1] : colors.gradients.danger[1];
                    },
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10,
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed.y;
                                const status = value >= 0 ? 'Surplus' : 'Deficit';
                                return `${status}: ${Math.abs(value)} kcal`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        grid: {
                            color: 'rgba(0,0,0,0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            callback: function(value) {
                                return value + ' kcal';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    createMacroBreakdownChart() {
        const ctx = document.getElementById('macroBreakdownChart');
        if (!ctx) return;

        this.charts.macroBreakdown = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Carbohydrates', 'Proteins', 'Fats'],
                datasets: [{
                    data: [45, 25, 30],
                    backgroundColor: [
                        colors.warning,
                        colors.success,
                        colors.info
                    ],
                    borderColor: [
                        colors.gradients.warning[1],
                        colors.gradients.success[1],
                        colors.gradients.info[1]
                    ],
                    borderWidth: 3,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10,
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '%';
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }

    createHeartRateZoneChart() {
        const ctx = document.getElementById('heartRateZoneChart');
        if (!ctx) return;

        this.charts.heartRateZone = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Recovery', 'Aerobic', 'Threshold', 'Maximum', 'Peak'],
                datasets: [{
                    label: 'Time in Zone (%)',
                    data: [20, 35, 30, 10, 5],
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: colors.primary,
                    borderWidth: 2,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 50,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        pointLabels: {
                            font: {
                                size: 12
                            }
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    createProgressChart() {
        const ctx = document.getElementById('progressChart');
        if (!ctx) return;

        const gradient = createGradient(ctx.getContext('2d'), colors.primary, colors.gradients.primary[1]);

        this.charts.progress = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                datasets: [{
                    label: 'Progress Score',
                    data: [65, 70, 75, 72, 78, 85],
                    borderColor: colors.primary,
                    backgroundColor: gradient,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 3,
                    pointRadius: 8,
                    pointHoverRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10,
                        callbacks: {
                            label: function(context) {
                                return 'Score: ' + context.parsed.y + '/100';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(0,0,0,0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '/100';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    updateChart(chartName, newData) {
        if (this.charts[chartName]) {
            this.charts[chartName].data = newData;
            this.charts[chartName].update('active');
        }
    }

    destroyChart(chartName) {
        if (this.charts[chartName]) {
            this.charts[chartName].destroy();
            delete this.charts[chartName];
        }
    }

    destroyAllCharts() {
        Object.keys(this.charts).forEach(chartName => {
            this.destroyChart(chartName);
        });
    }
}

// Analytics Charts
class AnalyticsCharts {
    constructor() {
        this.charts = {};
        this.initializeCharts();
    }

    initializeCharts() {
        this.createWorkoutTrendsChart();
        this.createNutritionTrendsChart();
        this.createBodyCompositionChart();
        this.createWorkoutTypeDistribution();
    }

    createWorkoutTrendsChart() {
        const ctx = document.getElementById('workoutTrendsChart');
        if (!ctx) return;

        const gradient = createGradient(ctx.getContext('2d'), colors.primary, colors.gradients.primary[1]);

        this.charts.workoutTrends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // Will be populated with actual dates
                datasets: [{
                    label: 'Calories Burned',
                    data: [],
                    borderColor: colors.primary,
                    backgroundColor: gradient,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)',
                            drawBorder: false
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return formatDate(this.getLabelForValue(value));
                            }
                        }
                    }
                }
            }
        });
    }

    createNutritionTrendsChart() {
        const ctx = document.getElementById('nutritionTrendsChart');
        if (!ctx) return;

        this.charts.nutritionTrends = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Carbs',
                    data: [],
                    backgroundColor: colors.warning,
                    borderColor: colors.gradients.warning[1],
                    borderWidth: 2,
                    borderRadius: 4
                }, {
                    label: 'Proteins',
                    data: [],
                    backgroundColor: colors.success,
                    borderColor: colors.gradients.success[1],
                    borderWidth: 2,
                    borderRadius: 4
                }, {
                    label: 'Fats',
                    data: [],
                    backgroundColor: colors.info,
                    borderColor: colors.gradients.info[1],
                    borderWidth: 2,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y + 'g';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        stacked: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            callback: function(value) {
                                return value + 'g';
                            }
                        }
                    },
                    x: {
                        stacked: true,
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    createBodyCompositionChart() {
        const ctx = document.getElementById('bodyCompositionChart');
        if (!ctx) return;

        const gradient = createGradient(ctx.getContext('2d'), colors.success, colors.gradients.success[1]);

        this.charts.bodyComposition = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Weight (kg)',
                    data: [],
                    borderColor: colors.success,
                    backgroundColor: gradient,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y',
                    pointBackgroundColor: colors.success,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }, {
                    label: 'Body Fat %',
                    data: [],
                    borderColor: colors.warning,
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    tension: 0.4,
                    fill: false,
                    yAxisID: 'y1',
                    pointBackgroundColor: colors.warning,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        grid: {
                            color: 'rgba(0,0,0,0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            callback: function(value) {
                                return value + ' kg';
                            }
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    createWorkoutTypeDistribution() {
        const ctx = document.getElementById('workoutTypeChart');
        if (!ctx) return;

        this.charts.workoutType = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: ['Strength', 'Cardio', 'HIIT', 'Yoga', 'Sports'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: [
                        colors.primary,
                        colors.success,
                        colors.danger,
                        colors.info,
                        colors.warning
                    ],
                    borderColor: [
                        colors.gradients.primary[1],
                        colors.gradients.success[1],
                        colors.gradients.danger[1],
                        colors.gradients.info[1],
                        colors.gradients.warning[1]
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        cornerRadius: 10,
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '%';
                            }
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    loadAnalyticsData() {
        fetch('/api/analytics_data')
            .then(response => response.json())
            .then(data => {
                this.updateChartsWithData(data);
            })
            .catch(error => {
                console.error('Error loading analytics data:', error);
            });
    }

    updateChartsWithData(data) {
        // Update workout trends
        if (this.charts.workoutTrends && data.workouts) {
            const dates = data.workouts.map(w => formatDate(w.date));
            const calories = data.workouts.map(w => w.calories_burned);
            
            this.charts.workoutTrends.data.labels = dates;
            this.charts.workoutTrends.data.datasets[0].data = calories;
            this.charts.workoutTrends.update();
        }

        // Update nutrition trends
        if (this.charts.nutritionTrends && data.nutrition) {
            const dates = [...new Set(data.nutrition.map(n => formatDate(n.date)))];
            const carbsByDate = this.aggregateNutritionByDate(data.nutrition, 'carbs');
            const proteinsByDate = this.aggregateNutritionByDate(data.nutrition, 'proteins');
            const fatsByDate = this.aggregateNutritionByDate(data.nutrition, 'fats');

            this.charts.nutritionTrends.data.labels = dates;
            this.charts.nutritionTrends.data.datasets[0].data = carbsByDate;
            this.charts.nutritionTrends.data.datasets[1].data = proteinsByDate;
            this.charts.nutritionTrends.data.datasets[2].data = fatsByDate;
            this.charts.nutritionTrends.update();
        }

        // Update macro breakdown
        if (this.charts.macroBreakdown && data.macro_percentages) {
            this.charts.macroBreakdown.data.datasets[0].data = [
                data.macro_percentages.carbs,
                data.macro_percentages.proteins,
                data.macro_percentages.fats
            ];
            this.charts.macroBreakdown.update();
        }
    }

    aggregateNutritionByDate(nutrition, field) {
        const dateMap = {};
        nutrition.forEach(item => {
            const date = formatDate(item.date);
            if (!dateMap[date]) {
                dateMap[date] = 0;
            }
            dateMap[date] += item[field];
        });
        return Object.values(dateMap);
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard charts if on dashboard page
    if (document.getElementById('weeklyOverviewChart')) {
        window.dashboardCharts = new DashboardCharts();
    }

    // Initialize analytics charts if on analytics page
    if (document.getElementById('workoutTrendsChart')) {
        window.analyticsCharts = new AnalyticsCharts();
        window.analyticsCharts.loadAnalyticsData();
    }
});

// Export for use in other scripts
window.ChartUtils = {
    colors,
    createGradient,
    formatNumber,
    formatDate,
    DashboardCharts,
    AnalyticsCharts
};
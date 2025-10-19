// Chart.js utility functions for Lifestyle Data Analytics Platform

// Global chart configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#6c757d';

// Common chart options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                usePointStyle: true,
                padding: 20
            }
        }
    }
};

// Color palette for charts
const chartColors = {
    primary: 'rgba(0, 123, 255, 0.8)',
    success: 'rgba(40, 167, 69, 0.8)',
    info: 'rgba(23, 162, 184, 0.8)',
    warning: 'rgba(255, 193, 7, 0.8)',
    danger: 'rgba(220, 53, 69, 0.8)',
    secondary: 'rgba(108, 117, 125, 0.8)',
    light: 'rgba(248, 249, 250, 0.8)',
    dark: 'rgba(52, 58, 64, 0.8)'
};

const chartColorPalette = [
    chartColors.primary,
    chartColors.success,
    chartColors.info,
    chartColors.warning,
    chartColors.danger,
    chartColors.secondary,
    chartColors.light,
    chartColors.dark
];

// BMI Trend Chart
function createBMITrendChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'BMI',
                data: data.data || [],
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'BMI Value',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return `BMI: ${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

// Calorie Balance Chart
function createCalorieBalanceChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels || [],
            datasets: data.datasets || []
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Calories',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1
                }
            }
        }
    });
}

// Macro Distribution Chart
function createMacroDistributionChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels || [],
            datasets: [{
                data: data.data || [],
                backgroundColor: data.backgroundColor || chartColorPalette.slice(0, data.labels?.length || 3),
                borderWidth: 3,
                borderColor: '#fff',
                hoverOffset: 10
            }]
        },
        options: {
            ...commonOptions,
            maintainAspectRatio: true,
            plugins: {
                ...commonOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed}g (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Workout Distribution Chart
function createWorkoutDistributionChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels || [],
            datasets: [{
                data: data.data || [],
                backgroundColor: chartColorPalette.slice(0, data.labels?.length || 5),
                borderWidth: 2,
                borderColor: '#fff',
                hoverOffset: 15
            }]
        },
        options: {
            ...commonOptions,
            maintainAspectRatio: true,
            plugins: {
                ...commonOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} workouts (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Heart Rate Trend Chart
function createHeartRateChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: data.datasets || []
        },
        options: {
            ...commonOptions,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Heart Rate (BPM)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y} BPM`;
                        }
                    }
                }
            }
        }
    });
}

// Progress Chart
function createProgressChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'Current',
                data: data.current || [],
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }, {
                label: 'Target',
                data: data.target || [],
                borderColor: chartColors.success,
                backgroundColor: 'rgba(40, 167, 69, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: chartColors.success,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                borderDash: [5, 5]
            }]
        },
        options: {
            ...commonOptions,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: chartColors.primary,
                    borderWidth: 1
                }
            }
        }
    });
}

// Utility function to create sample data
function generateSampleData(type, days = 30) {
    const data = {
        labels: [],
        data: [],
        datasets: []
    };
    
    for (let i = days - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        data.labels.push(date.toISOString().split('T')[0]);
    }
    
    switch (type) {
        case 'bmi':
            data.data = data.labels.map(() => 22 + Math.random() * 4 - 2);
            break;
        case 'calorie_balance':
            data.datasets = [
                {
                    label: 'Calories Consumed',
                    data: data.labels.map(() => 1800 + Math.random() * 400 - 200),
                    backgroundColor: chartColors.primary
                },
                {
                    label: 'Calories Burned',
                    data: data.labels.map(() => 1500 + Math.random() * 300 - 150),
                    backgroundColor: chartColors.success
                }
            ];
            break;
        case 'macro':
            data.labels = ['Carbs', 'Proteins', 'Fats'];
            data.data = [45, 25, 30];
            data.backgroundColor = [chartColors.primary, chartColors.success, chartColors.warning];
            break;
        case 'workout':
            data.labels = ['Strength', 'Cardio', 'HIIT', 'Yoga', 'Other'];
            data.data = [8, 12, 6, 4, 2];
            break;
        case 'heart_rate':
            data.datasets = [
                {
                    label: 'Average BPM',
                    data: data.labels.map(() => 120 + Math.random() * 40 - 20),
                    backgroundColor: chartColors.primary,
                    borderColor: chartColors.primary
                },
                {
                    label: 'Max BPM',
                    data: data.labels.map(() => 160 + Math.random() * 30 - 15),
                    backgroundColor: chartColors.danger,
                    borderColor: chartColors.danger
                }
            ];
            break;
    }
    
    return data;
}

// Export functions for global use
window.createBMITrendChart = createBMITrendChart;
window.createCalorieBalanceChart = createCalorieBalanceChart;
window.createMacroDistributionChart = createMacroDistributionChart;
window.createWorkoutDistributionChart = createWorkoutDistributionChart;
window.createHeartRateChart = createHeartRateChart;
window.createProgressChart = createProgressChart;
window.generateSampleData = generateSampleData;
window.chartColors = chartColors;
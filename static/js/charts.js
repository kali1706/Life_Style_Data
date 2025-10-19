// Custom JavaScript for Lifestyle Analytics Platform

// Chart default configurations
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = true;
Chart.defaults.plugins.legend.position = 'bottom';

// Color palette
const colors = {
    primary: '#3498db',
    success: '#2ecc71',
    danger: '#e74c3c',
    warning: '#f39c12',
    info: '#3498db',
    purple: '#9b59b6',
    orange: '#e67e22'
};

// Utility function to format numbers
function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

// Utility function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
    });
}

// Create a basic chart
function createChart(canvasId, type, labels, datasets, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    return new Chart(ctx.getContext('2d'), {
        type: type,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            ...options
        }
    });
}

// Create workout history chart
function createWorkoutChart(data) {
    return createChart(
        'workoutChart',
        'bar',
        data.dates.map(formatDate),
        [{
            label: 'Calories Burned',
            data: data.calories,
            backgroundColor: colors.danger,
            borderColor: colors.danger,
            borderWidth: 1
        }],
        {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Calories'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Calories: ' + formatNumber(context.parsed.y);
                        }
                    }
                }
            }
        }
    );
}

// Create macro distribution pie chart
function createMacroChart(carbs, protein, fat) {
    return createChart(
        'macroChart',
        'pie',
        ['Carbs', 'Protein', 'Fat'],
        [{
            data: [carbs, protein, fat],
            backgroundColor: [colors.primary, colors.success, colors.warning]
        }],
        {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    );
}

// Create weight trend chart
function createWeightTrendChart(dates, weights) {
    return createChart(
        'weightTrendChart',
        'line',
        dates.map(formatDate),
        [{
            label: 'Weight (kg)',
            data: weights,
            borderColor: colors.info,
            backgroundColor: 'rgba(52, 152, 219, 0.1)',
            fill: true,
            tension: 0.4
        }],
        {
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Weight (kg)'
                    }
                }
            }
        }
    );
}

// Create BMI trend chart
function createBMITrendChart(dates, bmis) {
    return createChart(
        'bmiTrendChart',
        'line',
        dates.map(formatDate),
        [{
            label: 'BMI',
            data: bmis,
            borderColor: colors.purple,
            backgroundColor: 'rgba(155, 89, 182, 0.1)',
            fill: true,
            tension: 0.4
        }],
        {
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'BMI'
                    }
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: 18.5,
                            yMax: 18.5,
                            borderColor: colors.warning,
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Underweight',
                                enabled: true
                            }
                        },
                        line2: {
                            type: 'line',
                            yMin: 25,
                            yMax: 25,
                            borderColor: colors.warning,
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Overweight',
                                enabled: true
                            }
                        }
                    }
                }
            }
        }
    );
}

// Create calorie comparison chart
function createCalorieComparisonChart(dates, consumed, burned) {
    return createChart(
        'calorieComparisonChart',
        'line',
        dates.map(formatDate),
        [
            {
                label: 'Calories Consumed',
                data: consumed,
                borderColor: colors.primary,
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                fill: true,
                tension: 0.4
            },
            {
                label: 'Calories Burned',
                data: burned,
                borderColor: colors.danger,
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                fill: true,
                tension: 0.4
            }
        ],
        {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Calories'
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    );
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
}

// Show loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

// Hide loading spinner
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Fetch dashboard data via AJAX
async function fetchDashboardData() {
    try {
        const response = await fetch('/api/dashboard_data');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        return null;
    }
}

// Fetch workout history via AJAX
async function fetchWorkoutHistory(days = 30) {
    try {
        const response = await fetch(`/api/workout_history?days=${days}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Error fetching workout history:', error);
        return null;
    }
}

// Initialize tooltips (Bootstrap)
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Auto-dismiss alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);

// Export functions for use in templates
window.LifestyleAnalytics = {
    createChart,
    createWorkoutChart,
    createMacroChart,
    createWeightTrendChart,
    createBMITrendChart,
    createCalorieComparisonChart,
    validateForm,
    showLoading,
    hideLoading,
    fetchDashboardData,
    fetchWorkoutHistory,
    formatNumber,
    formatDate
};

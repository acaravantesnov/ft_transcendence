// Función para cargar un script dinámicamente
function loadScript(url) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = url;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`Failed to load script: ${url}`));
        document.head.appendChild(script);
    });
}

// Variables globales para las instancias de gráficos
var pointsScoredChartInstance = null;
var pointsConcededChartInstance = null;

// Función para destruir los gráficos existentes
function destroyCharts() {
    if (pointsScoredChartInstance) {
        pointsScoredChartInstance.destroy();
        pointsScoredChartInstance = null;
    }
    if (pointsConcededChartInstance) {
        pointsConcededChartInstance.destroy();
        pointsConcededChartInstance = null;
    }
}

// Función principal de stats que se ejecuta después de cargar Chart.js
async function stats() {
    const username = document.getElementById('username').textContent;

    try {
        const response = await fetch(`/users/getStats/${username}/`);
        const data = await response.json();

        if (data.error) {
            console.log('Error fetching stats:', data.error);
            return;
        }

        // Verificar y manejar datos
        var totalScored = data.total_scored || 0;
        var totalConceded = data.total_conceded || 0;
        var totalPoints = data.total_points || 1;  // Evitar división por cero

        var pointsScoredPercentage = (totalPoints !== 0) ? (totalScored * 100) / totalPoints : 0;
        var pointsConcededPercentage = (totalPoints !== 0) ? (totalConceded * 100) / totalPoints : 0;

        // Actualizar porcentajes en HTML
        document.getElementById('pointsScoredPercentage').textContent = `${pointsScoredPercentage.toFixed(2)} %`;
        document.getElementById('pointsConcededPercentage').textContent = `${pointsConcededPercentage.toFixed(2)} %`;

        // Destruir gráficos existentes antes de crear nuevos
        destroyCharts();

        // Crear nuevos gráficos
        pointsScoredChartInstance = new Chart(document.getElementById('pointsScoredChart'), {
            type: 'pie',
            data: {
                labels: ['Points Scored'],
                datasets: [{
                    label: 'Points Scored',
                    data: [pointsScoredPercentage, 100 - pointsScoredPercentage],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(0, 0, 0, 0.1)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(0, 0, 0, 0.2)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                            }
                        }
                    }
                }
            }
        });

        pointsConcededChartInstance = new Chart(document.getElementById('pointsConcededChart'), {
            type: 'pie',
            data: {
                labels: ['Points Conceded'],
                datasets: [{
                    label: 'Points Conceded',
                    data: [pointsConcededPercentage, 100 - pointsConcededPercentage],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(0, 0, 0, 0.1)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(0, 0, 0, 0.2)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.log('Error fetching stats data:', error);
    }
}

// Cargar Chart.js dinámicamente y luego ejecutar la función stats
loadScript('https://cdn.jsdelivr.net/npm/chart.js')
    .then(() => {
        stats();  // Ejecuta la función stats después de que Chart.js ha sido cargado
    })
    .catch(error => {
        console.log("Error loading Chart.js:", error);
    });

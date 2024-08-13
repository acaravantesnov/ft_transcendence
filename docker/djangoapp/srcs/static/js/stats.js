async function stats () {
    const username = document.getElementById('username').textContent;
    let pointsScoredChartInstance = null;
    let pointsConcededChartInstance = null;
    fetch(`/users/getStats/${username}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {
                console.error('Error fetching stats:', data.error);
                return;
            }

            const totalScored = data.total_scored;
            const totalConceded = data.total_conceded;
            const totalPossiblePoints = data.total_possible_points;

            const pointsScoredPercentage = (totalScored / totalPossiblePoints) * 100;
            const pointsConcededPercentage = (totalConceded / totalPossiblePoints) * 100;

            // Update percentages in HTML
            document.getElementById('pointsScoredPercentage').textContent = `Points Scored: ${pointsScoredPercentage.toFixed(2)}%`;
            document.getElementById('pointsConcededPercentage').textContent = `Points Conceded: ${pointsConcededPercentage.toFixed(2)}%`;

            if (pointsScoredChartInstance) {
                pointsScoredChartInstance.destroy();
            }
            if (pointsConcededChartInstance) {
                pointsConcededChartInstance.destroy();
            }

            // Create charts
            pointsScoredChartInstance = new Chart(document.getElementById('pointsScoredChart'), {
                type: 'bar',
                data: {
                    labels: ['Points Scored'],
                    datasets: [{
                        label: 'Points Scored',
                        data: [pointsScoredPercentage],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            pointsConcededChartInstance = new Chart(document.getElementById('pointsConcededChart'), {
                type: 'bar',
                data: {
                    labels: ['Points Conceded'],
                    datasets: [{
                        label: 'Points Conceded',
                        data: [pointsConcededPercentage],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching stats data:', error));
}

stats();

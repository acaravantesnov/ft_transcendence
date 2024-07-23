document.addEventListener('DOMContentLoaded', function() {
    const username = document.getElementById('username').textContent;

    fetch(`getDashboard/${username}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('games-won').textContent = data.games_won;
            document.getElementById('games-lost').textContent = data.games_lost;

            const gamesList = document.getElementById('games-list');
            data.games_list.forEach(game => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${game.player1}</td>
                    <td>${game.player2}</td>
                    <td>${game.winner}</td>
                    <td>${game.date}</td>
                    <td>${game.duration}</td>
                    <td>${game.player1_score}</td>
                    <td>${game.player2_score}</td>
                `;
                gamesList.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
});

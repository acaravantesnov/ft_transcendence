//document.addEventListener('DOMContentLoaded', function() {
async function dashboard () {
    console.log('DOM fully loaded and parsed');
    const username = document.getElementById('username').textContent;
    console.log('Username:', username);

    fetch(`/users/getDashboard/${username}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('games-won').textContent = data.games_won || 0;
            document.getElementById('games-lost').textContent = data.games_lost || 0;

            const gamesList = document.getElementById('games-list');
            gamesList.innerHTML = '';
            if (data.games_list.length === 0) {
                gamesList.innerHTML = '<tr><td colspan="7" class="text-center">No games played yet</td></tr>';
            } else {
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
            }
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
}

dashboard();
//});

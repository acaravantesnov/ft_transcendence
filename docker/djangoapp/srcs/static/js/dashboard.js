async function dashboard () {
    const username = document.getElementById('username').textContent;

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
                data.games_list.forEach((game, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${game.player1}</td>
                        <td>${game.player2}</td>
                        <td>${game.winner}</td>
                        <td>${game.date}</td>
                    `;
                    row.addEventListener('click', () => toggleDetails(index));
                    gamesList.appendChild(row);

                    const detailsRow = document.createElement('tr');
                    detailsRow.classList.add('details-row');
                    detailsRow.style.display = 'none';
                    detailsRow.innerHTML = `
                        <td colspan="4">
                            <strong>Duration:</strong> ${game.duration}<br>
                            <strong>${game.player1} Score:</strong> ${game.player1_score}<br>
                            <strong>${game.player2} Score:</strong> ${game.player2_score}
                        </td>
                    `;
                    gamesList.appendChild(detailsRow);
                });
            }
        })
        .catch(error => console.log('Error fetching dashboard data:', error));
}

function toggleDetails(index) {
    const detailsRows = document.querySelectorAll('.details-row');
    const row = detailsRows[index];
    if (row.style.display === 'none') {
        row.style.display = '';
    } else {
        row.style.display = 'none';
    }
}

statsbutton.addEventListener('click', (e) => {
    const event = new CustomEvent('STATSTRIGGER', { detail: { href: `/users/stats/${user.username}` } });
	document.dispatchEvent(event);
});

document.addEventListener('STATSTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

dashboard();
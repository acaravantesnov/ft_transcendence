document.addEventListener("DOMContentLoaded", function() {
    fetchUsers();
    fetchGames();
});

function fetchUsers() {
    fetch('/api/users/')
        .then(response => response.json())
        .then(data => {
            let userList = document.getElementById('user-list');
            userList.innerHTML = `<h2>Usuarios</h2><table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Nombre de usuario</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    ${data.map(user => `
                                        <tr>
                                            <td>${user.id}</td>
                                            <td>${user.username}</td>
                                        </tr>`).join('')}
                                    </tbody>
                                </table>`;
        });
}

function fetchGames() {
    fetch('/api/games/')
        .then(response => response.json())
        .then(data => {
            let gameList = document.getElementById('game-list');
            gameList.innerHTML = `<h2>Juegos</h2><table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Jugador 1</th>
                                            <th>Jugador 2</th>
                                            <th>Puntuación Jugador 1</th>
                                            <th>Puntuación Jugador 2</th>
                                            <th>Fecha de Juego</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    ${data.map(game => `
                                        <tr>
                                            <td>${game.id}</td>
                                            <td>${game.player1.username}</td>
                                            <td>${game.player2.username}</td>
                                            <td>${game.player1_score}</td>
                                            <td>${game.player2_score}</td>
                                            <td>${game.date_played}</td>
                                        </tr>`).join('')}
                                    </tbody>
                                </table>`;
        });
}

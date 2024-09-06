var stats = async () => {

    await fetch(`/users/statistics/${user.username}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('gamesWon').textContent = data.gamesWon;
            document.getElementById('gamesLost').textContent = data.gamesLost;
            document.getElementById('goals').textContent = data.goals;
            document.getElementById('score').textContent = data.score;
        })
        .catch(error => console.log('Error fetching data:', error));
};

stats();
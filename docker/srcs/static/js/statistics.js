var stats = async () => {

    await fetch(`/users/statistics/${currentUsername}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('gamesWon').textContent = data.gamesWon;
            document.getElementById('gamesLost').textContent = data.gamesLost;
            document.getElementById('goals').textContent = data.goals;
        })
        .catch(error => console.error('Error fetching data:', error));
};

stats();
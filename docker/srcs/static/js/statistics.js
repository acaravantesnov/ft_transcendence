var stats = async () => {

    const username = await getCurrentUsername();

    await fetch(`/users/statistics/${username}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('gamesWon').textContent = data.gamesWon;
            document.getElementById('gamesLost').textContent = data.gamesLost;
            document.getElementById('goals').textContent = data.goals;
        })
        .catch(error => console.error('Error fetching data:', error));
};

stats();
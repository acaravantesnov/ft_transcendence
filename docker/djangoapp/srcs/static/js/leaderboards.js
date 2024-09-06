async function leaderboards () {
    try {
        const response = await fetch('/users/getLeaderboards/');
        const data = await response.json();
        const tableBody = document.getElementById('leaderboardTable').getElementsByTagName('tbody')[0];
        data.forEach(element => {
            const row = tableBody.insertRow();
            const rank = row.insertCell(0);
            const username = row.insertCell(1);
            const score = row.insertCell(2);
            rank.textContent = element.rank;
            username.textContent = element.username;
            score.textContent = element.score;
        });
    } catch (error) {
        console.log('Error:', error);
        alert('An error occurred while fetching the leaderboards. Please try again later.');
    }
}

leaderboards();
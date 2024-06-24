async function leaderboards () {
    try {
        const response = await fetch('/users/leaderboards/');
        const data = await response.json();
        const tableBody = document.getElementById('leaderboardTable').getElementsByTagName('tbody')[0];
        data.array.forEach(element => {
            const row = tableBody.insertRow();
            const rank = row.insertCell(0);
            const username = row.insertCell(1);
            const score = row.insertCell(2);
            rank.innerHTML = element.rank;
            username.innerHTML = element.username;
            score.innerHTML = element.score;
        });
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching the leaderboards. Please try again later.');
    }
}
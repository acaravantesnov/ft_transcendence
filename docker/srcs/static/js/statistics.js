var stats = async () => {
    const response = await fetch('/users/getUsername/');
    const data = await response.json();
    
    const username = data.username;
    const endpoints = {
        gamesWon: `/users/statistics/gamesWon/${username}`,
        gamesLost: `/users/statistics/gamesLost/${username}`,
        goals: `/users/statistics/goals/${username}`,
    };
    for (const [key, url] of Object.entries(endpoints)) {
        await fetch(url)
            .then(response => response.json())
            .then(data => {
                document.getElementById(key).textContent = data;
            })
            .catch(error => console.error('Error fetching data:', error));
    }
};

stats();
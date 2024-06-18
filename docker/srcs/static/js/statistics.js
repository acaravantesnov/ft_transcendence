function initializeStatistics() {
    console.log('initializeStatistics2 function.');
    const fetchElements = document.querySelectorAll('[data-fetch-url]');

    fetchElements.forEach(element => {
        const url = element.getAttribute('data-fetch-url');
        fetchData(url, element.id);
    });

    function fetchData(url, resultElementId) {
        console.log('initializeStatistics3 function.');
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const resultElement = document.getElementById(resultElementId);
                resultElement.textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    }
}

initializeStatistics();

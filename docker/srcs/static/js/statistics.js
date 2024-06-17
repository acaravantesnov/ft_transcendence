document.addEventListener('DOMContentLoaded', () => {
    // Seleccionar todos los elementos que tienen el atributo data-fetch-url
    const fetchElements = document.querySelectorAll('[data-fetch-url]');

    // Iterar sobre cada elemento y hacer la petición fetch
    fetchElements.forEach(element => {
        const url = element.getAttribute('data-fetch-url');
        fetchData(url, element.id);
    });
});

function fetchData(url, resultElementId) {
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
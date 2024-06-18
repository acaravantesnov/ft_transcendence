document.addEventListener('DOMContentLoaded', function() {
    const ball = document.getElementById('ball');
    const gameArea = document.getElementById('game-area');
    const ballDiameter = 25;
    //console.log('Path:', window.location.pathname);

    const roomName = window.location.pathname.split('/').slice(-2, -1)[0];

    // console.log('Room name:', roomName);
    // console.log('Splitted path:', window.location.pathname.split('/'));
    // console.log('Sliced path:', window.location.pathname.split('/').slice(-2, -1));
    // console.log('Websocket URL:', 'ws://' + window.location.host + '/ws/game2/' + roomName + '/');

    // const socket = new WebSocket('ws://' + window.location.host + '/ws/game2/' + roomName + '/');

    // socket.onmessage = function(e) {
    //     console.log('Message:', e.data);
    //     const data = JSON.parse(e.data);
    //     console.log('Data:', data);
    //     console.log('X:', data.x);
    //     console.log('Y:', data.y);
    //     ball.style.left = data.x + 'px';
    //     ball.style.top = data.y + 'px';

    //     const gameAreaRect = gameArea.getBoundingClientRect();
    //     let newLeft = Math.max(0, Math.min(gameAreaRect.width - ballDiameter, data.x));
    //     let newTop = Math.max(0, Math.min(gameAreaRect.height - ballDiameter, data.y));

    //     ball.style.left = newLeft + 'px';
    //     ball.style.top = newTop + 'px';
    // };
});

let csrftoken = getCookie('csrftoken');

// document.getElementById('playButton').addEventListener('click', function() {
//     fetch('http://0.0.0.0:8000/users/addGame', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrftoken,
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             player1: '{{ request.user.id }}',
//             player2: '',
//             winner: '{{ request.user.id }}',
//             date: '2021-06-01',
//             duration: 10,
//             player1_score: 7,
//             player2_score: 0}),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Success:', data);
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//     });
// });

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
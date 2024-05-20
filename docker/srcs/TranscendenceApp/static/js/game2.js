document.addEventListener('DOMContentLoaded', function() {
    const ball = document.getElementById('ball');
    const gameArea = document.getElementById('game-area');
    console.log('Path:', window.location.pathname);
    const roomName = window.location.pathname.split('/').slice(-2, -1)[0];
    // Log the room name
    console.log('Room name:', roomName);
    // Log the splitted path
    console.log('Splitted path:', window.location.pathname.split('/'));
    // Log the sliced path
    console.log('Sliced path:', window.location.pathname.split('/').slice(-2, -1));
    // Log the websocket URL
    console.log('Websocket URL:', 'ws://' + window.location.host + '/ws/game2/' + roomName + '/');
    const socket = new WebSocket('ws://' + window.location.host + '/ws/game2/' + roomName + '/');

    socket.onmessage = function(e) {
        console.log('Message:', e.data);
        const data = JSON.parse(e.data);
        console.log('Data:', data);
        console.log('X:', data.x);
        console.log('Y:', data.y);
        ball.style.left = data.x + 'px';
        ball.style.top = data.y + 'px';
    };
});

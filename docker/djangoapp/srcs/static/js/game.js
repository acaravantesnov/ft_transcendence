const ball = document.getElementById('ball');
const leftPaddle = document.getElementById('left-paddle');
const rightPaddle = document.getElementById('right-paddle');
const leftScore = document.getElementById('left-score');
const rightScore = document.getElementById('right-score');
const gameArea = document.getElementById('game-area');

const username = window.location.pathname.split('/').slice(-4, -3)[0];
const roomName = window.location.pathname.split('/').slice(-3, -2)[0];
const side = window.location.pathname.split('/').slice(-2, -1)[0];
console.log('username ', username);
console.log('roomName ', roomName);
console.log('side ', side);
const socket = new WebSocket('wss://' + window.location.host + '/ws/game2/' + username + '/' + roomName + '/' + side + '/');

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'game_state') {
        const state = data.state;
        const scaleX = gameArea.clientWidth / 800;
        const scaleY = gameArea.clientHeight / 600;

        ball.style.left = (state.ball_position.x * scaleX) + 'px';
        ball.style.top = (state.ball_position.y * scaleY) + 'px';
        leftPaddle.style.left = (state.left_paddle.x * scaleX)+ 'px';
        leftPaddle.style.top = (state.left_paddle.y * scaleY) + 'px';
        rightPaddle.style.left = (state.right_paddle.x * scaleX) + 'px';
        rightPaddle.style.top = (state.right_paddle.y * scaleY) + 'px';
        leftScore.innerText = state.scores.left;
        rightScore.innerText = state.scores.right;
        console.log('game state', state);
        if (state.game_over.ended) {
            if (state.game_over.winner === 'left') {
                alert('Left player won!');
            } else {
                alert('Right player won!');
            }
            window.location.href = '/';
        }
    }
};

socket.onopen = function(e) {
    socket.send(JSON.stringify({type: 'join'}));
};

document.addEventListener('keydown', function(e) {
    console.log('keydown', e.key);
    let speed = 0;
    if (e.key === 'ArrowUp') {
        speed = -5;
    } else if (e.key === 'ArrowDown') {
        speed = 5;
    }
    if (speed !== 0) {
        socket.send(JSON.stringify({type: 'paddle', speed: speed}));
    }
});

document.addEventListener('keyup', function(e) {
    console.log('keyup', e.key);
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        socket.send(JSON.stringify({type: 'paddle', speed: 0}));
    }
});

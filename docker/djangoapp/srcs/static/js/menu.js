// game.js

let socket = null;
let intervalId = null;

// DOM elements
const ball = document.getElementById('ball');
const leftPaddle = document.getElementById('left-paddle');
const rightPaddle = document.getElementById('right-paddle');
const leftScore = document.getElementById('left-score');
const rightScore = document.getElementById('right-score');
const gameArea = document.getElementById('game-area');

async function gameIA() {
	try {
		const response = await fetch(`/users/play/vsIA/createGame/${user.username}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCoockie('xcsrftoken')
			}
		});
		const data = await response.json;
		if (data.status === 'success') {
			const { room_name } = data.response;
			initializeGame(room_name, 'left');
		}
	} catch (error) { console.error('Error creating vsIA game: ', error); }
}

// Game functions
function initializeGame(roomName, side) {
    clearInterval(intervalId);

    // Show game area and hide waitlist button
    document.getElementById('game-area').style.display = 'block';
    document.getElementById('playMenu').style.display = 'none';
    
    socket = new WebSocket(`wss://${window.location.host}/ws/game2/${user.username}/${roomName}/${side}/`);
    
    socket.onopen = () => socket.send(JSON.stringify({type: 'join'}));
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'game_state') {
            updateGameState(data.state);
        }
    };

    // Update URL without refreshing
    // window.history.pushState({}, '', `/users/play/${user.username}/${roomName}/${side}/`);
}

function updateGameState(state) {
    const scaleX = gameArea.clientWidth / 800;
    const scaleY = gameArea.clientHeight / 600;

    ball.style.left = `${state.ball_position.x * scaleX}px`;
    ball.style.top = `${state.ball_position.y * scaleY}px`;
    leftPaddle.style.left = `${state.left_paddle.x * scaleX}px`;
    leftPaddle.style.top = `${state.left_paddle.y * scaleY}px`;
    rightPaddle.style.left = `${state.right_pa3dle.x * scaleX}px`;
    rightPaddle.style.top = `${state.right_paddle.y * scaleY}px`;
    leftScore.innerText = state.scores.left;
    rightScore.innerText = state.scores.right;

    if (state.game_over.ended) {
        alert(`${state.game_over.winner === 'left' ? 'Left' : 'Right'} player won!`);
        window.location.href = `/users/home/${user.username}`;
    }
}

// Event listeners

vsIA.addEventListener('click', gameIA);

document.addEventListener('keydown', (e) => {
    let speed = 0;
    if (e.key === 'ArrowUp') speed = -5;
    else if (e.key === 'ArrowDown') speed = 5;
    
    if (speed !== 0 && socket) {
        socket.send(JSON.stringify({type: 'paddle', speed}));
    }
});

document.addEventListener('keyup', (e) => {
    if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && socket) {
        socket.send(JSON.stringify({type: 'paddle', speed: 0}));
    }
});

// Initialization

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
const waitlistButton = document.getElementById('waitlistButton');

// Waitlist functions
async function addToWaitlist() {
    try {
        const response = await fetch(`/users/waitlist/addtowaitlist/${user.username}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Added to waitlist:', data);
        } else {
            console.error('Failed to add to waitlist:', data);
        }
    } catch (error) {
        console.error('Error adding to waitlist:', error);
    }
}

async function checkWaitlist() {
    try {
        const response = await fetch(`/users/waitlist/checkwaitlist/${user.username}/`);
        const data = await response.json();
        console.log('Waitlist status:', data);

        if (data.status === 'success') {
            const { room_name, user_left, user_right } = data.response;
            const side = user.username === user_left ? 'left' : (user.username === user_right ? 'right' : 'spectator');
            initializeGame(room_name, side);
        }
    } catch (error) {
        console.error('Error checking waitlist:', error);
    }
}

// Game functions
function initializeGame(roomName, side) {
    clearInterval(intervalId);

    // Show game area and hide waitlist button
    document.getElementById('game-area').style.display = 'block';
    document.getElementById('waitlistButton').style.display = 'none';
    
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
    rightPaddle.style.left = `${state.right_paddle.x * scaleX}px`;
    rightPaddle.style.top = `${state.right_paddle.y * scaleY}px`;
    leftScore.innerText = state.scores.left;
    rightScore.innerText = state.scores.right;

    if (state.game_over.ended) {
        alert(`${state.game_over.winner === 'left' ? 'Left' : 'Right'} player won!`);
        window.location.href = `/users/home/${user.username}`;
    }
}

// Event listeners
waitlistButton.addEventListener('click', addToWaitlist);

document.addEventListener('keydown', (e) => {
    let speed = 0;
    if (e.key === 'ArrowUp') speed = -3;
    else if (e.key === 'ArrowDown') speed = 3;
    
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
function init() {
    user.username = document.body.dataset.username; // Assume username is set in the HTML
    intervalId = setInterval(checkWaitlist, 1000);
}

init();

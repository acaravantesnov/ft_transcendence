// playing.js

// game vars

// var socket = null;
var mode = null;


// DOM elements
var ball = document.getElementById('ball');
var leftPaddle = document.getElementById('left-paddle');
var rightPaddle = document.getElementById('right-paddle');
var leftScore = document.getElementById('left-score');
var rightScore = document.getElementById('right-score');
var gameArea = document.getElementById('game-area');

title = document.getElementsByClassName('display-2')[0].innerHTML = (window.location.toString().search('vsPlayer')>0 ? 'vsPlayer' : window.location.toString().search('tournament')>0 ? 'Tournament' : " ");

/*
async function init_game(str) {
	try {
		const txt = title+str; 
		const response = await fetch(`/users/play/createGame/${txt}/${user.username}/`);
		//const response = await fetch(`/users/tournament/addtowaitingroom/${room_id}/${user.username}`)
		const data = await response.json();
		console.log(data);
		if (data.status === 'success') {
			const room_name = data.room_name;
			const side = 'left';
			console.log(room_name);
			go_to(`/users/playing/${room_name}/${side}/${user.username}`)
			initializeGame(room_name, 'left');
		} else if (data.status === 'waiting') {
			check_waitlist();
		}
	} catch (error) { console.error('Error creating vsIA game: ', error); }
}
*/

/*
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
*/

// Tournament

// Una vez inizializado el torneo comprobar el estado del juego con getgame, mientras esta en waiting, pantalla de espera
//      waiting for _playerX_
//
//     Incluir una secuencia: ready? 3, 2, 1 o algo
//     Mostrar en que level se encuentra y demas



//
// Cuando acabe el juego, volver a la pantalla de waiting
//
// Al acabar el torneo mostrar un trofeo, quiza un podio y algo de informacion del torneo
//
// Regresar a la pantalla inicial de usuario conectado
//

// Game functions
function initializeGame(roomName, side, left_player, right_player) {
    console.log(side);

    // Hide the game elements initially
    toggleGameElements(false);

    // Start the countdown and then initialize the game
    startCountdown(5, left_player, right_player)
        .then(() => {
            // Show the game elements after the countdown
            toggleGameElements(true);

            // Initialize the WebSocket connection and start the game
            startGame(roomName, side);
        });
}

function toggleGameElements(show) {
    const display = show ? 'block' : 'none';
    document.getElementById('countdown').style.display = show ? 'none' : 'block';
    document.getElementById('scores').style.display = display;
    document.getElementById('ball').style.display = display;
    document.getElementById('left-paddle').style.display = display;
    document.getElementById('right-paddle').style.display = display;
}

async function startCountdown(seconds, left_player, right_player) {
    const countdownElement = document.getElementById('countdown');

    while (seconds > 0) {
        countdownElement.innerText = seconds > 3 ? left_player + ' vs ' + right_player : seconds;
        await delay(1000);
        seconds--;
    }
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function startGame(roomName, side) {
    console.log('Starting game...');
    socket = new WebSocket(`wss://${window.location.host}/ws/game2/${user.username}/${roomName}/${side}/`);

    socket.onopen = () => socket.send(JSON.stringify({ type: 'join' }));

    mode = (side === 'local') ? 'local' : 'remote';

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'game_state') {
            updateGameState(data.state);
        }
    };

    console.log(roomName);
    console.log(roomName.search('T'));

    if (roomName.search('T') > 0) {
        socket.onclose = event => {
            sessionStorage.removeItem('roomName');
            sessionStorage.removeItem('side');
            go_to(`/users/play/tournament/${user.username}`);
            go_back_to_wait_for_game(roomName);
        };
    } else {
        socket.onclose = event => {
            sessionStorage.removeItem('roomName');
            sessionStorage.removeItem('side');
            go_to(`/users/home/${user.username}`);
        };
    }

    sessionStorage.setItem('roomName', roomName);
    sessionStorage.setItem('side', side);
    console.log('Saved on local storage');
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
	    socket.close(4000,"Game Over")
    }
}

// Event listeners

document.addEventListener('keydown', (e) => {
    if (mode == 'remote') {
	    let speed = 0;
	    if (e.key === 'ArrowUp') speed = -3;
	    else if (e.key === 'ArrowDown') speed = 3;
	    if (speed !== 0 && socket) {
		    socket.send(JSON.stringify({type: 'paddle', speed}));
	    }

    } else if (mode == 'local') {
    	let right_speed = 0;
    	let left_speed = 0;
    	if (e.key === 'ArrowUp') right_speed = -3;
    	else if (e.key === 'ArrowDown') right_speed = 3;
    	else if (e.key === 'w') left_speed = -3;
    	else if (e.key === 's') left_speed = 3;
    
    	if (right_speed !== 0 && socket) {
        	socket.send(JSON.stringify({type: 'right_paddle', speed: right_speed}));
    	}
    	if (left_speed !== 0 && socket) {
			socket.send(JSON.stringify({type: 'left_paddle', speed: left_speed}));
    	}
    }
});

document.addEventListener('keyup', (e) => {
    if (mode == 'remote') {
		if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && socket) {
			socket.send(JSON.stringify({type: 'paddle', speed: 0}));
		}
    } else if (mode == 'local') {
    	if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && socket) {
        	socket.send(JSON.stringify({type: 'right_paddle', speed: 0}));
    	}
    	if ((e.key === 'w' || e.key === 's') && socket) {
			socket.send(JSON.stringify({type: 'left_paddle', speed: 0}));
    	}
    }
});


// Restore state and reconnect WebSocket on page load
function restore_game() {
    const roomName = sessionStorage.getItem('roomName');
    const side = sessionStorage.getItem('side');
    console.log('Restoring game state from local storage...');
    console.log('data is: ' + roomName + ' ' + side);

    if (roomName && side) {
        console.log('Restoring game state from local storage...');
        startGame(roomName, side);
    }
}

restore_game();
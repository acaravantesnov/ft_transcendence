// play.js


// DOM elements
//var ball = document.getElementById('ball');
//var leftPaddle = document.getElementById('left-paddle');
//var rightPaddle = document.getElementById('right-paddle');
//var leftScore = document.getElementById('left-score');
//var rightScore = document.getElementById('right-score');
//var gameArea = document.getElementById('game-area');

async function gameIA() {
	try {
		const response = await fetch(`/users/play/createGame/AI/${user.username}/`);
		const data = await response.json();
		console.log(data);
		if (data.status === 'success') {
			const room_name = data.room_name;
			console.log(room_name);
			await go_to(`/users/playing/${user.username}`);
            await new Promise(r => setTimeout(r, 1000));
			initializeGame(room_name, 'right', 'AI', user.username);

		}
	} catch (error) { console.error('Error creating vsAI game: ', error); }
}

// To Playing page

// Game functions
/*
function initializeGame(roomName, side) {
    //clearInterval(intervalId);

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

    socket.onclose = event => {
	    //meke popUp
	    window.location.href = `/users/home/${user.username}`;
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
	    socket.close(4000,"Game Over")
    }
}
*/
// Event listeners

vsIA.addEventListener('click', gameIA);

vsPlayer.addEventListener('click', () => go_to(`/users/play/mode/vsPlayer/${user.username}`));

tournament.addEventListener('click', () => go_to(`/users/play/mode/tournament/${user.username}`));

/*
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
*/

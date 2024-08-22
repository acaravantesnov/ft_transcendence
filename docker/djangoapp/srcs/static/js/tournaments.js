// tournaments.js 

var prueba = document.location.pathname.split('/');
console.log(prueba);


popup = document.getElementById('open-popup')
closepopup = document.getElementById('close-popup')
tarea = document.getElementById('tournament-area')

async function join_tournament(room_name) {
	console.log('Aqui si...')
	try {
		const response = await fetch(`/users/tournament/addtowaitingroom/${room_name}/${user.username}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			}
		});
		const data = await response.json();
		if (data.status == 'success') {
			console.log('Aqui tambien...');
			// JoinTournamentToast
			go_to(`/users/play/tournament/${user.username}`);
		}
	} catch (error) {
		console.error(' Error while join {room_name} due to: ', error);
	}
}

/*
 *  Quittin function

async function quit_tournament(room_name) {
	try {
		const response = await fetch(`/users/tournament/`)
		const data = await response.json();
		if (data.status == 'success') {
		}
	} catch (error) {
		console.error(' Error while quitting from {room_name} due to: ', error);
	}
}

*/

async function waiting_tournament_room(room_name) {
	try {
		console.log(room_name);
		const response = await fetch(`/users/tournament/checkwaitingroom/${room_name}`);
		const data = await response.json();
		console.log(data);
		if (data.status == 'ready') {
			console.log(data);
			clearInterval(intervalID);
			gestion_de_waiters('juego', room_name);
		} else if (data.status == 'waiting') {
			console.log('Waiting for turnament');
			// Incluir algo de informacion como la gente que falta para estar ready
		}
	} catch (error) {
		console.error(' Error while entering {room_name} due to: ', error);
	}
}

async function waiting_for_tournament_game(room_name) {
        try {
                const response = await fetch(`/users/tournament/getgame/${room_name}/${user.username}`);
                const data = await response.json();
                if (data.status == 'error') {
			console.log('waiting for game...');
			console.log(data);
                        document.getElementById('text-game').textContent = " is waiting for ";
                        document.getElementById('localPlayer').textContent = "";
                        document.getElementById('rival').textContent = "";

                } else if (data.status == 'success') {
			console.log('Siiuuuu  a jugar');
			console.log(data);
			clearInterval(intervalID);
                        await go_to(`/users/playing/${user.username}/`);
			await new Promise(r => setTimeout(r, 1000));
                        document.getElementById('text-game').textContent = " V.S. "
                        const { room_tournament_name, user_left, user_right } = data.response;
                        const side = user.username === user_left ? 'left' : (user.username === user_right ? 'right' : 'spectator');
                        document.getElementById('localPlayer').textContent = user_left;
                        document.getElementById('rival').textContent = user_right;
                        initializeGame(room_tournament_name, side);
                }

        } catch (error) {
                console.error(' Error while managing the game -- due to: ', error);
        }
}


async function createTournament() {
	try {
		const mode = 'tournamentremote';
		const response = await fetch(`/users/play/createGame/${mode}/${user.username}/`);
		const data = await response.json();
		console.log(data)
		if (data.status == 'success') {
			const responseNT = await fetch(`/users/tournament/addtowaitingroom/${data.room_name}/${user.username}/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken')
				}
			});
			const dataNT = await responseNT.json();
			if (dataNT.status == 'success') {
				document.getElementById('roomName').innerHTML = data.room_name;
			}
		}
	} catch (error) {
		console.error('Error while creating a tournament: ', error);
	}
}

async function getTournaments() {
	try {
		console.log(user.username);
		const response = await fetch(`/users/tournament/gettournaments/${user.username}/`);
		const data = await response.json();
		console.log(data);
		if (data.status == 'success') {
			console.log(data);
			data.tournaments.forEach(element => {
				const a = document.createElement('div');
				a.setAttribute("class", "tournament-div");
				const b = document.createElement('strong');
				b.setAttribute('onclick', `enter_tournament("${element.room_name}", "${user.username}")`);
				b.innerHTML = element.room_name;
				a.appendChild(b);
				a.appendChild(document.createElement("br"));
				const c = document.createElement('i');
				c.innerHTML = "Current members: " + element.players;
				a.appendChild(c);
				
				buttons = document.createElement("span");
				if (element.joined == 'false') {
					buttons.setAttribute("class", "in-line");
					const accept = document.createElement("button");
					accept.setAttribute("type", "button");
					accept.setAttribute("class", "btn btn-success");
					accept.setAttribute("onclick", `join_tournament("${element.room_name}")`);
					const check = document.createElement("i");
					check.setAttribute("class", "fa fa-check");
					accept.appendChild(check);
					buttons.appendChild(accept);
				} else if (element.joined == 'true') {
					const waiting = document.createElement('button');
					waiting.setAttribute("type", "button");
					waiting.setAttribute("class", "btn btn-secondary");
					const w = document.createElement("i");
					w.innerHTML = "Joined";
					waiting.appendChild(w);
					buttons.appendChild(waiting);
					//const reject = document.createElement("button");
					//reject.setAttribute("type", "button");
					//reject.setAttribute("class", "btn btn-danger");
					//reject.setAttribute("onclick", `accept_request(${element.id}, "rejected")`);
					//const cross = document.createElement("i");
					//cross.setAttribute("class", "fa fa-times");
					//reject.appendChild(cross);
					//buttons.appendChild(reject);
				}

				a.appendChild(buttons);
				tarea.appendChild(a);
			});
		}
	} catch (error) {
		console.error('Error while getting tournaments: ', error);
		console.log(user.username);
	}
}

getTournaments();

// Listeners

popup.addEventListener('click', createTournament);
closepopup.addEventListener('click', () => go_to(`/users/play/tournament/${user.username}`))

// Waiters

async function enter_tournament(room_name, username) {
	console.log('Aqui entramos...')
	try {
		const response = await fetch(`/users/tournament/readytoplay/${room_name}/${username}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			}
		});
		const data = await response.json();
		if (data.status == 'success') {
			tarea.parentElement.innerHTML = `<h3><i>Waiting for ${room_name}</i></h3>`;
			gestion_de_waiters('torneo', room_name);
//			intervalID = setInterval(waiting_tournament_room, 3000, room_name);
		}
	}
	catch (error) {
		console.error(' Error while entering room {room_name} due to: ', error);
	}
}


function gestion_de_waiters(flag, room_name) {

	console.log('Aqui tambien...')
	if ( flag == 'torneo'){
		console.log('Pero aqui no')
		intervalID = setInterval(waiting_tournament_room, 1000, room_name);
	} else if (flag == 'juego') {
		intervalID = setInterval(waiting_for_tournament_game, 1000, room_name);
	}
}

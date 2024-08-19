// tournaments.js

popup = document.getElementById('open-popup')
closepopup = document.getElementById('close-popup')
tarea = document.getElementById('tournament-area')

async function join_tournament(room_name) {
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
		const response = await fetch(`/users/tournament/checkwaitingroom/${room_name}`)
		const data = await response.json();
		if (data.status == 'success') {
			console.log(data);
		}
	} catch (error) {
		console.error(' Error while entering {room_name} due to: ', error);
	}
}

async function createTournament() {
	try {
		const mode = 'tournamentremote';
		const response = await fetch(`/users/play/createGame/${mode}/${user.username}/`);
		const data = await response.json();
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
			intervalID = setInterval(waiting_tournament_room, 3000, room_name);
		}
	}
	catch (error) {
		console.error(' Error while entering room {room_name} due to: ', error);
	}
}

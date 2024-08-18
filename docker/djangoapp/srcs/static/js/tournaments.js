// tournaments.js

const popup = document.getElementById('open-popup')

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
		const response = await fetch('/users/tournament/gettournaments/');
		const data = await response.json();
		if (data.status == 'success') {
			console.log(data);
			data.forEach(element => {

			});
		}
	} catch (error) {
		console.error('Error while getting tournaments: ', error);
	}
}

getTournaments();

// Listeners

popup.addEventListener('click', createTournament);

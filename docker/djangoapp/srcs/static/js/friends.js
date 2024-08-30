/*async function users (){
    try {
	const response = await fetch('/users/getUsers/');
   	const data = await response.json();
	const tableBody = document.getElementById('userTable').getElementsByTagName('tbody')[0];
	data.forEach(element => {
		const row = tableBody.insertRow();
		const username = row.insertCell(0);
		const newButton = row.insertCell(1);
		const newLink = document.createElement("a");
		username.textContent = element.username;
		newLink.innerHTML = "SendRequest";
		newLink.setAttribute("href", "/users/send_friend_request/"+element.id);
		newButton.appendChild(newLink);

	});
	    } catch (error) {
	    console.error('Error:', error);
	    alert('An error ocurred while fetching the usersList. Please try again later.');
    }
}*/


async function friend_requests (){
    try {
	const response = await fetch(`/users/getRequests/${user.username}`);
   	const data = await response.json();
	const tableBody = document.getElementById('requestTable').getElementsByTagName('tbody')[0];
	    if (data.length != 0) {
		const a = document.createElement("h2");
		a.setAttribute("class", "text-center");
		a.innerHTML = "Requests";
		tableBody.parentNode.parentNode.before(a);
		const b = document.createElement("thead");
		r = b.insertRow();
		const ra = r.insertCell(0);
		ra.setAttribute("scope", "col");
		ra.outerHTML = "<th>Rank</th>";
		const player = r.insertCell(1);
		player.setAttribute("scope", "col");
		player.outerHTML = "<th>Player</th>";
		const add = r.insertCell(2);
		add.setAttribute("scope", "col");
		add.outerHTML = "<th>Accept</th>";
		
		tableBody.before(b);
	    }
	data.forEach(element => {
		const row = tableBody.insertRow();
		const rank = row.insertCell(0);
		const from_username = row.insertCell(1);
		const buttons = row.insertCell(2);
		from_username.textContent = element.from_username;
		rank.textContent = element.id;

		buttons.setAttribute("class", "in-line");
		const accept = document.createElement("button");
		accept.setAttribute("type", "button");
		accept.setAttribute("class", "btn btn-success");
		accept.setAttribute("onclick", `accept_request(${element.id}, "accepted")`);
		const check = document.createElement("i");
		check.setAttribute("class", "fa fa-check");
		accept.appendChild(check);
		buttons.appendChild(accept);

		const reject = document.createElement("button");
		reject.setAttribute("type", "button");
		reject.setAttribute("class", "btn btn-danger");
		reject.setAttribute("onclick", `accept_request(${element.id}, "rejected")`);
		const cross = document.createElement("i");
		cross.setAttribute("class", "fa fa-times");
		reject.appendChild(cross);
		buttons.appendChild(reject);

	});
	    } catch (error) {
	    console.error('Error:', error);
	    alert('An error ocurred while fetching the requestsList. Please try again later.');
    }
}


async function friends (){
    try {
		const response = await fetch(`/users/getFriendList/${user.username}`);
  		const data = await response.json();
		const tableBody = document.getElementById('friendTable').getElementsByTagName('tbody')[0];
		data.forEach(element => {
			const row = tableBody.insertRow();
			const rank = row.insertCell(0);
			const username = row.insertCell(1);
			const stat = row.insertCell(2);
			rank.textContent = element.order;
			username.textContent = element.username;
			const circle = document.createElement("button");
			if (element.stat == true) { circle.setAttribute("class", "btn btn-success btn-circle"); }
			else { circle.setAttribute("class", "btn btn-danger btn-circle"); }
			stat.appendChild(circle);
		});
	} catch (error) {
		console.error('Error:', error);
		// We don't want the alert in the evaluation
		// alert('An error ocurred while fetching the friendList. Please try again later.');
		}
}


async function autocomplete(inp) {

	var arr = [];
	const response = await fetch('/users/getUsers/');
   	const data = await response.json();
	
	data.forEach(element => {
		arr.push(element.username)
	});

	inp.addEventListener("input", function(e) {

		var val = this.value;

		closeAllLists();
		if (!val) { return false; }

		const tableBody = document.getElementById('userTable').getElementsByTagName('tbody')[0];
		const a = document.createElement("h2");
		a.setAttribute("class", "text-center");
		a.innerHTML = "Users";
		tableBody.parentNode.before(a);
		const b = document.createElement("thead");
		r = b.insertRow();
		const ra = r.insertCell(0);
		ra.setAttribute("scope", "col");
		ra.outerHTML = "<th>Rank</th>";
		const player = r.insertCell(1);
		player.setAttribute("scope", "col");
		player.outerHTML = "<th>Player</th>";
		const add = r.insertCell(2);
		add.setAttribute("scope", "col");
		add.outerHTML = "<th>Add</th>";
		
		tableBody.before(b);



		for (var i = 0; i < arr.length; i++) {
			if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
				data.forEach(element => {
					var flag = false;
					if (arr[i] == element.username) {
					const row = tableBody.insertRow();
					const rank = row.insertCell(0);
					const username = row.insertCell(1);
					const newButton = row.insertCell(2);
					rank.textContent = element.id;
					username.textContent = element.username;
					
					const button = document.createElement("button");
					button.innerHTML = "+";
					button.setAttribute("type", "button");
					button.setAttribute("class", "btn btn-primary");
					button.setAttribute("onclick", `send_request(${element.id})`);
					newButton.appendChild(button);
					}
				});

			}
		}
	});

	function closeAllLists(elmnt) {
		const tableBody = document.getElementById('userTable').getElementsByTagName('tbody')[0];
		const table = document.getElementById('userTable').getElementsByTagName('thead')[0];
		const title = document.getElementById('userTable').parentNode.getElementsByTagName('h2')[0];
		const l = tableBody.rows.length;

		for (var i = 0; i < l; i++) {
			tableBody.deleteRow(0);
		}
		if (title) { title.remove(); }
		if (table) { table.remove(); }
	}
}

async function send_request(userID) {

	const responseReq = await fetch(`/users/send_friend_request/${userID}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
		}
	});
	const data = await responseReq.json();

	if (data.status === 'success') { sentRequestToast(); } else { notSentRequestToast(); }
}

async function accept_request(requestID, accepted) {

	const responseReq = await fetch(`/users/accept_friend_request/${requestID}${accepted}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
		}
	});
	const data = await responseReq.json();

	if (data.status === "success") { acceptedRequestToast(); } else { rejectedRequestToast(); }
	const event = new CustomEvent('REQTRIGGER', { detail: { href: `/users/friends/${user.username}` } });
	document.dispatchEvent(event);
}

document.addEventListener('REQTRIGGER', (e) => {
	const { href } = e.detail;
	const event = {
		preventDefault: () => {},
		target: { href }
	};
	route(event);
});

function notSentRequestToast() {
	
	var toast = new bootstrap.Toast(document.getElementById('notSentRequestToast'));
	toast.show();
}

function sentRequestToast() {

	var toast = new bootstrap.Toast(document.getElementById('sentRequestToast'));
	toast.show();
}
function rejectedRequestToast() {
	
	var toast = new bootstrap.Toast(document.getElementById('rejectedRequestToast'));
	toast.show();
}

function acceptedRequestToast() {

	var toast = new bootstrap.Toast(document.getElementById('acceptedRequestToast'));
	toast.show();
}


//users();
friend_requests();
friends();
autocomplete(document.getElementById("myInput"));

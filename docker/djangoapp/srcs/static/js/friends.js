async function users (){
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
}


async function friend_requests (){
    try {
	const response = await fetch(`/users/getRequests/${user.username}`);
   	const data = await response.json();
	const tableBody = document.getElementById('requestTable').getElementsByTagName('tbody')[0];
	data.forEach(element => {
		const row = tableBody.insertRow();
		const from_username = row.insertCell(0);
		const newButton = row.insertCell(1);
		const to_username = row.insertCell(2);
		const newLink = document.createElement("a");
		from_username.textContent = element.from_username;
		to_username.textContent = element.to_username;
		newLink.innerHTML = "AcceptRequest";
		newLink.setAttribute("href", "/users/accept_friend_request/"+element.id);
		newButton.appendChild(newLink);

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
		stat.textContent = element.stat;
	});
	    } catch (error) {
	    console.error('Error:', error);
	    alert('An error ocurred while fetching the friendList. Please try again later.');
    }
}

users();
friend_requests();
friends();

/*$('#friends').keyup(function(e){
	query = $("#friends").val();
	$.ajax({
		data: {'nombre': query},
		url: '/users/friends/',
		type: 'get',
		success: function(data) {
			console.log(data[0].username);
		},
		error: function(message) {
			console.log(message)
		}
	});
});*/

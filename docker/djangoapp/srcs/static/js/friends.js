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


async function autocomplete(inp) {

	var arr = [];
	const response = await fetch('/users/getUsers/');
   	const data = await response.json();

	data.forEach(element => {
		arr.push(element.username)
	});

	var currentFocus;

	inp.addEventListener("input", function(e) {


		var a, b, i, val = this.value;

		
		closeAllLists();
		if (!val) { return false; }
		currentFocus = -1;

		a = document.createElement("div");
		a.setAttribute("id", this.id + "autocomplete-list");
		a.setAttribute("class", "autocomplete-items");
		this.parentNode.appendChild(a);

		for (i = 0; i < arr.length; i++) {
			if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
				b = document.createElement("div");
				b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
				b.innerHTML += arr[i].substr(val.length);
				b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
				
				b.addEventListener("click", function(e) {
					inp.value = this.getElementByTagName("input")[0].value;
					closeAllLists();
				});
				a.appendChild(b);
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

			}
		}
	});

	inp.addEventListener("keydown", function(e) {
		var x = document.getElementById(this.id + "autocomplete-list");

		if (x) x = x.getElementByTagName("div");
		if (e.keyCode == 40) {
			currentFocus++;
			addActive(x);
		} else if (e.keyCode == 38) {
			currentFocus--;
			addActive(x);
		} else if (e.keyCode == 13) {
			e.preventDefault();
			if (currentFocus > -1) {
				if (x) x[currentFocus].click();
			}
		}
	});

	function addActive(x) {
		if (!x) return false;
		removeActive(x);

		if (currentFocus >= x.length) currentFocus = 0;
		if (currentFocus < 0) currentFocus = (x.length - 1);
		x[currentFocus].classList.add("autocomplete-active");
	}
	function removeActive(x) {
		for (var i = 0; i < x.length; i++) {
			x[i].classList.remove("autocomplete-active");
		}
	}
	function closeAllLists(elmnt) {
		var x = document.getElementsByClassName("autocomplete-items");
		const tableBody = document.getElementById('userTable').getElementsByTagName('tbody')[0];
		for (var i = 0; i < x.length; i++) {
			if (elmnt != x[i] && elmnt != inp) {
				x[i].parentNode.removeChild(x[i]);
				tableBody.deleteRow(i);
			}
		}
	}

	document.addEventListener("click", function (e) {
		closeAllLists(e.target);
	})
}

//users();
friend_requests();
friends();
autocomplete(document.getElementById("myInput"));

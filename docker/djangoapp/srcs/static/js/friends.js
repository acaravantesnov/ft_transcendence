async function friends (){
    try {
	const response = await fetch("/users/getFriends/");
   	const data = await response.json();
	const tableBody = document.getElementById().getElementsByagName()[0];
	data.forEach(element => {
		const row = tableBody.insertRow();
		const rank = row.insertCell(0);
		const username = row.insertCell(1);
	}
    } catch (error) {
	    console.error('Error:', error);
	    alert('An error ocurred while fetching the friendList. Please try again later.');
    }
}

friends();

$('#searchFriends').keyup(function(e){
	query = $("#searchFriends").val();
	$.ajax({
		data: {'nombre': query},
		url: '',
		type: 'get',
		success: function(data) {
			console.log(data[0].username);
		},
		error: function(message) {
			console.log(message)
		}
	});
});

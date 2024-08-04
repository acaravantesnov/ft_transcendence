

document.getElementById('username').innerHTML = `<h5>${user.username}</h5>`;
document.getElementById('first_name').innerHTML = `<h5>First name: </h5>${user.first_name}`;
document.getElementById('last_name').innerHTML = `<h5>Last name: </h5>${user.last_name}`;
document.getElementById('email').innerHTML = `<h5>Email: </h5>${user.email}`;
document.getElementById('last_login').innerHTML = `<h5>Last login: </h5>${user.last_login}`;
document.getElementById('date_joined').innerHTML = `<h5>Date joined: </h5>${user.date_joined}`;

document.getElementById('avatar').innerHTML = `<img src="${user.avatar}" alt="logo" class="image-center" style="width: 15vh; height: 15vh;">`;

//document.getElementById('edit_profile').getElementsByTagName('a')[0].setAttribute("href", "/users/editProfile/");
//document.getElementById('change_password').getElementsByTagName('a')[0].setAttribute("href", `/users/changePassword/${user.username}`);
//document.getElementById('choose_avatar').getElementsByTagName('a')[0].setAttribute("href", `/users/editProfile/${user.username}`);


async function updateAvatar() {

	const formData = new FormData();
	
	formData.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
	formData.append('avatar', document.getElementById('id_avatar').files[0]);

	try {
		const response = await fetch('/users/profile/updateAvatar/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': formData('csrfmiddlewaretoken'), 
			},
			body: formData,
		});

		if (!response.ok) { throw new Error('Network response was not ok'); }

		const responseData = await response.json();

		if (responseData === 'success') {
			successfulUpdateAvatarToast();
			const event = new CustomEvent('UPDATEAVATARTRIGGER', { detail: { href: `/users/profile/${user.username}`} });
			document.dispatchEvent(event);
		} else { unsuccessfulUpdateAvatarToast(); }
	} catch (error) {
		console.error('Error: ', error);
		unsuccessfulUpdateAvatarToast('An error ocurred while updating your avatar. Please try again later.');
	}
}

document.addEventListener('UPDATEAVATARTRIGGER', (e) => {
	const { href } = e.detail;
	const event = {
		preventDefault: () => {},
		target: { href }
	};
	route(event);
});

function unsuccessfulUpdateAvatarToast(message)
{
    var toast = new bootstrap.Toast(document.getElementById('unsuccessfulUpdateAvatarToast'))
    document.getElementById('unsuccessUpdateAvatar').textContent = message;
    toast.show()
}

function successfulUpdateAvatarToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulUpdateAvatarToast'))
    toast.show()
}


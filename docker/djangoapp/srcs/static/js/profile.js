document.getElementById('edit_profile').addEventListener('click', (e) => {
	route(e);
});
document.getElementById('change_password').addEventListener('click', (e) => {
	route(e);
});
avatar_flag = false;
document.getElementById('choose_avatar').addEventListener('click', (e) =>{

	if (!avatar_flag) {
		document.getElementById('avatarDiv').innerHTML = '<label for="id_avatar">Avatar</label><input type="file" name="avatar" id="id_avatar" class="form-control"><input type="submit" value="Submit" class="btn btn-primary">'; avatar_flag = true;
	} else { document.getElementById('avatarDiv').innerHTML = ""; avatar_flag = false; }
});

async function updateAvatar() {

	const formData = new FormData();

	formData.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
	formData.append('avatar', document.getElementById('id_avatar').files[0]);

	try {
		const response = await fetch(`/users/updateAvatar/${user.username}/`, {
			method: 'POST',
			body: formData,
		});

		if (!response.ok) { throw new Error('Network response was not ok'); }

		const responseData = await response.json();

		if (responseData === 'success') {
			successfulUpdateAvatarToast();
			const event = new CustomEvent('UPDATEAVATARTRIGGER', { detail: { href: `/users/profile/${user.username}` } });
			document.dispatchEvent(event);
		} else { unsuccessfulUpdateAvatarToast('Error'); }
	} catch (error) {
		console.log('Error: ', error);
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

async function refresh_profile() {
    await updateUser();
	document.getElementById('username').innerHTML = `<i>${user.username}</i>`;
	document.getElementById('first_name').innerHTML = `<i>${user.first_name}</i>`;
	document.getElementById('last_name').innerHTML = `<i>${user.last_name}</i>`;
	document.getElementById('email').innerHTML = `<i>${user.email}</i>`;
	document.getElementById('last_login').innerHTML = `<i>${user.last_login}</i>`;
	document.getElementById('date_joined').innerHTML = `<i>${user.date_joined}</i>`;

	document.getElementById('avatar').innerHTML = `<img src="${user.avatar}" alt="logo" class="image-center" style="width: 15vh; height: 15vh;">`;
	document.getElementById('avatar_2').innerHTML = `<i>${user.avatar}</i>`;
}
refresh_profile();

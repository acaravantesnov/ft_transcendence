async function submitNewProfile(event) {

    const newProfileTrigger = document.getElementById('editProfileForm');
    if (newProfileTrigger)
    {
	    const formData = new FormData(event.target);

	    const formObject = {};
	    formData.forEach((value, key) => {
		    formObject[key] = value;
	    });

	    try {
		    const response = await fetch(`/users/editProfile/updateProfile/${user.username}/`, {
			    method: 'POST',
			    headers: {
				    'Content-Type': 'application/json',
				    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
			    },
			    body: JSON.stringify(formObject)
		    });

		    if (!response.ok) { throw new Error('Network response was not ok'); }

		    const responseData = await response.json();

		    if (responseData.status === 'success') {
			    successfulEditProfileToast();
			    const event = new CustomEvent('EDITPRFLTRIGGER', { detail: { href: `/users/profile/${user.username}` } });
			    document.dispatchEvent(event);
		    } else { unsuccessfulEditProfileToast(errorMessage); }
	    } catch (error) {
		    console.error('Error:', error);
		    unsuccessfulEditProfileToast('An error occurred while updating profile. Please try again later.');
	    }
    }
}

document.addEventListener('EDITPRFLTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

function unsuccessfulEditProfileToast(message)
{
    var toast = new bootstrap.Toast(document.getElementById('unsuccessfulEditProfileToast'))
    document.getElementById('unsuccessfulEditProfile').textContent = message;
    toast.show()
}

function successfulEditProfileToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulEditProfileToast'))
    toast.show()
}

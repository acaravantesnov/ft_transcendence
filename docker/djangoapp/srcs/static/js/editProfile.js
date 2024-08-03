async function submitNewProfile(event) {
    event.preventDefault();

    const formObject = {'username': document.getElementById('id_username').value, // If it is not possible to check again the username, delete this step.
    			'first_name': document.getElementById('id_first_name').value,
	    		'last_name': document.getElementById('id_last_name').value,
	    		'email': document.getElementById('id_email').value }
    console.log(formObject);



    try {
        const response = await fetch(`/users/editProfile/updateProfile/${user.username}/`, {
            method: 'POST',
	    headers: {
		    'Content-Type': 'application/json',
		    'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
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

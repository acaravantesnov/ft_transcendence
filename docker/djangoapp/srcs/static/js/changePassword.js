async function submitNewPassword()
{
    const newPasswordTrigger = document.getElementById('newPasswordForm');
    if (newPasswordTrigger) {
        // Gather form data
        const formData = new FormData(event.target);

        // Convert form data to a JSON object
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        try {
            const response = await fetch(`/users/changePassword/updatePassword/${user.username}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: JSON.stringify(formObject)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const responseData = await response.json();

            if (responseData.status == 'success') {
                successfulPassToast();
                let str = '/users/home/' + formObject.username;
                const event = new CustomEvent('NEWPASSWORDTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            } else {
                unsuccessfulPassToast(responseData.message);
            }
        } catch (error) {
            console.log('Error:', error);
        }
    }
}

async function redirectSignUp(event)
{
    route(event);
}

document.addEventListener('NEWPASSWORDTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

function successfulPassToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulPassToast'))
    toast.show()
}

function unsuccessfulPassToast(message)
{
    var toast = new bootstrap.Toast(document.getElementById('unsuccessfulPassToast'))
    toast.show()
}

async function submitSignIn()
{
    const signInTrigger = document.getElementById('mySignInForm');
    if (signInTrigger) {
        // Gather form data
        const formData = new FormData(event.target);

        // Convert form data to a JSON object
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        try {
            const response = await fetch('/users/checkCredentials/', {
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
                successfulLoginToast();
                let str = '/users/home/' + formObject.username;
                const event = new CustomEvent('SIGNINTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            } else {
                unsuccessfulLoginToast(responseData.message);
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

document.addEventListener('SIGNINTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

function successfulLoginToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulLoginToast'))
    toast.show()
}

function unsuccessfulLoginToast(message)
{
    var toast = new bootstrap.Toast(document.getElementById('unsuccessfulLoginToast'))
    toast.show()
}

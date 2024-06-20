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
                let str = '/users/home/' + formObject.username;
                const event = new CustomEvent('SIGNINTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            } else {
                alert(responseData.message); // Show error message on failure
            }
        } catch (error) {
            console.error('Error:', error);
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
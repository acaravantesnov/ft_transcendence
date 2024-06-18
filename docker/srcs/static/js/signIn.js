async function submitSignIn()
{
    const signInTrigger = document.getElementById('mySignInForm');
    if (signInTrigger) {
        console.log('signInTrigger');
        // Gather form data
        const formData = new FormData(event.target);

        // Convert form data to a JSON object
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        try {
            const response = await fetch('checkCredentials/', {
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
                // Create an event to be passed to the route function, this will change the url and load the appropriate content
                let str = '/users/game/' + formObject.username;
                const event = new CustomEvent('TRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            } else {
                alert(responseData.message); // Show error message on failure
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// Add an event listener for the custom 'TRIGGER' event outside the function to avoid re-registration
document.addEventListener('TRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

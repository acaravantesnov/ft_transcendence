async function submitSignUp(event)
{
    event.preventDefault();
    const signUpTrigger = document.getElementById('mySignUpForm');
    if (signUpTrigger) {
        // Gather form data
        const formData = new FormData(event.target);

        // Convert form data to a JSON object
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        try {
            const response = await fetch('createUser/', {
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
                const event = new CustomEvent('TRIGGER', { detail: { href: '/users/home/' } });
                document.dispatchEvent(event);
            } else {
                let errorMessage;
                for (let key in responseData.message) {
                    if (responseData.message.hasOwnProperty(key)) {
                        errorMessage += `\n${key}: ${responseData.message[key][0]}`;
                    }
                }
                alert(errorMessage);
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
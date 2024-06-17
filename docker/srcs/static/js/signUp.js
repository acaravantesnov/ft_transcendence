async function submitSignUp()
{
    const signUpTrigger = document.getElementById('mySignUpForm');
    if (signUpTrigger) {
        console.log('signUpTrigger');
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
                // Redirect to the URL provided in the response from the root URL
                window.location.href = responseData['redirect_url'];
            } else {
                alert(responseData.message); // Show error message on failure
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

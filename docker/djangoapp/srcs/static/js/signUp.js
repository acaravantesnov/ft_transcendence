async function submitSignUp(event) {
    event.preventDefault();
    const formData = new FormData();

    // Append fields individually
    formData.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    formData.append('username', document.getElementById('id_username').value);
    formData.append('first_name', document.getElementById('id_first_name').value);
    formData.append('last_name', document.getElementById('id_last_name').value);
    formData.append('email', document.getElementById('id_email').value);
    formData.append('password', document.getElementById('id_password').value);
    formData.append('confirm_password', document.getElementById('id_confirm_password').value);
    if (document.getElementById('id_avatar').files.length > 0) {
        formData.append('avatar', document.getElementById('id_avatar').files[0]);
    }
    else {
        formData.append('avatar', '/avatars/default.png');
    }

    try {
        const response = await fetch('/users/signUp/createUser/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();

        if (responseData.status === 'success') {
            successfulSignUpToast();
            const event = new CustomEvent('SIGNUPTRIGGER', { detail: { href: '/users/home/Guest' } });
            document.dispatchEvent(event);
        } else {
            let errorMessage = '';
            for (let key in responseData.message) {
                if (responseData.message.hasOwnProperty(key)) {
                    errorMessage += `\n${key}: ${responseData.message[key][0]}`;
                }
            }
            unsuccessfulSignUpToast(errorMessage);
        }
    } catch (error) {
        console.log('Error:', error);
        unsuccessfulSignUpToast('An error occurred while signing up. Please try again later.');
    }
}

document.addEventListener('SIGNUPTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

function unsuccessfulSignUpToast(message)
{
    var toast = new bootstrap.Toast(document.getElementById('unsuccessfulSignUpToast'))
    document.getElementById('unsuccessfulSignUp').textContent = message;
    toast.show()
}

function successfulSignUpToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulSignUpToast'))
    toast.show()
}

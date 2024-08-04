document.querySelectorAll('.cmon').forEach(function(element) {
    element.addEventListener('click', (e) => {
        var checkIfLoggedIn = async (e) => {

            if (user.username != 'Guest')
            {
                let str = e.target.href + user.username + '/';
                const event = new CustomEvent('CMONTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            }
        }
        e.preventDefault();
        checkIfLoggedIn(e);
    });
});

document.addEventListener('CMONTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    // If offcanvas is open, close it
    if (document.querySelector('.offcanvas.show')) {
        hideOffcanvas();
    }
    route(event);
});

document.getElementById('brand').addEventListener('click', (e) => {
    route(e);
});

document.getElementById('navbar-avatar').addEventListener('click', showOffcanvas);

document.getElementById('signOut').addEventListener('click', (e) => {
	signOut();
	hideOffcanvas();
	successfulLogoutToast();
	route(e);
});

async function signOut() {
	
	const a = await fetch(`/users/signOut/${user.username}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken'),
		}
	});
	const data = await a.json();
	console.log(data);
}

function successfulLogoutToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulLogoutToast'))
    toast.show()
}

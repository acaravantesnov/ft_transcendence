document.querySelectorAll('.cmon').forEach(function(element) {
    element.addEventListener('click', (e) => {

        var checkIfLoggedIn = async (e) => {

            if (e.target.href.endsWith('change_language/en/') || e.target.href.endsWith('change_language/es/') || e.target.href.endsWith('change_language/fr/'))
            {
                let str = e.target.href;
                const event = new CustomEvent('CMONTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            }
            else if (user.username != 'Guest')
            {
                if (e.target.href.endsWith('play/'))
                {
                    // Check if user has a game in progress
                    try {
                        const response = await fetch(`/users/play/checkGameExists/${user.username}/`);
                        const data = await response.json();
                        console.log('Check game status:', data);

                        if (data.status === 'success') {
                            const { room_name, user_left, user_right } = data.data;
                            let side = 'spectator';
                            if (user.username === user_left && user.username == user_right) {
                                side = 'local';
                            }
                            else if (user.username === user_left) {
                                side = 'left';
                            }
                            else if (user.username === user_right) {
                                side = 'right';
                            }
                            console.log('Side:', side);
                            await go_to(`/users/playing/${user.username}`)
                            await new Promise(r => setTimeout(r, 1500));
                            // initializeGame(room_name, side, user_left, user_right);
                            startGame(room_name, side);
                            // End the function here
                            return;
                        }
                    } catch (error) {
                        console.error('Error checking if user has a game in progress:', error);
                    }
                }
                let str = e.target.href + user.username + '/';
                const event = new CustomEvent('CMONTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            }
            else if (e.target.href.endsWith('leaderboards/'))
            {
                let str = e.target.href + 'Guest/';
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
    e.preventDefault();
    let str = '/users/home/' + user.username;
    const event = new CustomEvent('CMONTRIGGER', { detail: { href: str } });
    document.dispatchEvent(event);
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
}

function successfulLogoutToast()
{
    var toast = new bootstrap.Toast(document.getElementById('successfulLogoutToast'))
    toast.show()
}

var myCollapse = document.getElementById('navbarNav');
var bsCollapse = new bootstrap.Collapse(myCollapse, {
    toggle: false
});

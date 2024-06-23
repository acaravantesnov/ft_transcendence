document.querySelectorAll('.cmon').forEach(function(element) {
    element.addEventListener('click', (e) => {
        var checkIfLoggedIn = async (e) => {

            if (user.username != 'Guest')
            {
                let str = e.target.href + user.username + '/';
                const event = new CustomEvent('COMTRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            }
        }
        e.preventDefault();
        checkIfLoggedIn(e);
    });
});

document.addEventListener('COMTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

document.getElementById('brand').addEventListener('click', (e) => {
    route(e);
});

document.getElementById('signOut').addEventListener('click', (e) => {
    async function signOut() {
        await fetch('/users/signOut/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
    }
    signOut();
    closeOffcanvas();
    route(e);
});
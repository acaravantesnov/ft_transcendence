var user = {
    username: 'Guest',
    avatar: 'default.png'
};

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

async function updateUser() {
    try {
        let res = await fetch('/users/getUserInfo/');
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        user = await res.json();
        document.getElementById('offcanvasExampleLabel').innerHTML = user.username;
        document.getElementById('navbar-avatar').innerHTML = `<img src="/static/avatars/${user.avatar}" alt="logo" style="width: 50px; height: 50px;">`;
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

setInterval(updateUser, 500);

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

var routes = {
    404: {
        urlPattern: '404',
        title: '404 - Page not found',
        description: '404 - Page not found'
    },
    '/users/signIn/': {
        urlPattern: '/users/signIn/',
        title: 'Sign In',
        description: 'Sign In'
    },
    '/users/signUp/': {
        urlPattern: '/users/signUp/',
        title: 'Sign Up',
        description: 'Sign Up'
    },
}

/*
    Takes an event object as an argument. If the event object is not provided, it will default to
    the window.event object.
    Prevents the default action of the event object.
    Updates the browser’s history stack and the URL without reloading the page.
    locationhandler is called to load the appropriate content based on the new URL
*/
const route = (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, '', event.target.href);
    locationHandler();
}

const locationHandler = async () => {
    const location = window.location.pathname;
    if (location.length == 0) {
        location = '/';
    }
    let html = '';

    if (location == '/') // '/'
    {
        const url = `/users/home/${user.username}`;
        html = await fetch(url).then(res => res.text());
    }
    else if (location == '/users/home/') { // '/users/home/'
        const url = `/users/home/${user.username}`;
        html = await fetch(url).then(res => res.text());
    }
    else if (location.startsWith('/users/home/')) { // '/users/home/<str:username>/'
        html = await fetch(location).then(res => res.text());
    }
    else if (location.startsWith('/users/waitlist/')) { // '/users/waitlist/<str:username>/'
        console.log('location ', location);
        html = await fetch(location).then(res => res.text());
    }
    else if (location.startsWith('/users/play/')) { // '/users/play/<str:username>/<str:room_name>/<str:side>/'
        html = await fetch(location).then(res => res.text());
    }
    else if (location.startsWith('/users/leaderboards/')) { // '/users/leaderboards/<str:username>/'
        html = await fetch(location).then(res => res.text());
    }
    else if (location.startsWith('/users/profile/')) { // '/users/profile/<str:username>/'
        html = await fetch(location).then(res => res.text());
    }
    else { // routes
        const route = routes[location] || routes[404];
        html = await fetch(route.urlPattern).then(res => res.text());
    }

    insertHTML(html, document.getElementById('content'));
}

window.onpopstate = locationHandler;
window.route = route;

locationHandler();
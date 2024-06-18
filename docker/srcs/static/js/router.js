document.querySelectorAll('.cmon').forEach(function(element) {
    element.addEventListener('click', (e) => {
        var checkIfLoggedIn = async (e) => {
            const response = await fetch('/users/getUsername/');
            const data = await response.json();

            const username = data.username;

            if (username == 'Guest') {
                route(e);
            } else {
                let str = '/users/game/' + username;
                const event = new CustomEvent('TRIGGER', { detail: { href: str } });
                document.dispatchEvent(event);
            }
        }

        e.preventDefault();
        checkIfLoggedIn(e);
    });
});

document.getElementById('signOut').addEventListener('click', (e) => {
    route(e);
});

document.addEventListener('TRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    route(event);
});

const routes = {
    404: {
        urlPattern: '404',
        title: '404 - Page not found',
        description: '404 - Page not found'
    },
    '/': {
        urlPattern: 'users/',
        title: 'Home',
        description: 'Home'
    },
    '/users/': {
        urlPattern: 'users/',
        title: 'Users',
        description: 'Users'
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
    '/users/signOut/': {
        urlPattern: '/users/signOut/',
        title: 'Sign Out',
        description: 'Sign Out'
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
    //Think this first if statement is not needed
    if (location === '/') {
        html = await fetch('/users/').then(res => res.text());
        document.getElementById('content').innerHTML = html;
    }
    else if (location.startsWith('/users/game/')) {
        const username = location.split('/').pop();
        const url = `/users/game/${username}`;
        html = await fetch(url).then(res => res.text());
        document.getElementById('content').innerHTML = html;
    }
    else {
        const route = routes[location] || routes[404];
        html = await fetch(route.urlPattern).then(res => res.text());
        document.getElementById('content').innerHTML = html;
    }

    insertHTML(html, document.getElementById('content'));
}

window.onpopstate = locationHandler;
window.route = route;

locationHandler();
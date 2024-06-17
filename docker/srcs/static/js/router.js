
document.querySelectorAll('.cmon').forEach(function(element) {
    element.addEventListener('click', (e) => {
        console.log('RouterEventListener');
        const {target} = e;
        if (!target.matches('nav a')) {
            return;
        }
        e.preventDefault();
        route();
    });
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
    '/users/game/': {
        urlPattern: '/users/game/',
        title: 'Signed',
        description: 'Signed'
    },
}

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
    // Check if location is '/users/game/', followed by the username.
    // If true, then redirect to '/users/game/<str:username>'.
    console.log(location);
    if (location.startsWith('/users/game/')) {
        const username = location.split('/').pop();
        const url = `/users/game/${username}`;
        const html = await fetch(url).then(res => res.text());
        document.getElementById('content').innerHTML = html;
    }
    else {
        const route = routes[location] || routes[404];
        const html = await fetch(route.urlPattern).then(res => res.text());
        document.getElementById('content').innerHTML = html;
    }
}

window.onpopstate = locationHandler;
window.route = route;

locationHandler();
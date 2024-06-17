document.querySelectorAll('.cmon').forEach(function(element) {
    element.addEventListener('click', (e) => {
        console.log('RouterEventListener, route:', e.target.href);
        e.preventDefault();
        route(e);
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
    '/users/game/': {
        urlPattern: '/users/game/',
        title: 'Signed',
        description: 'Signed'
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
    console.log('Router, route:', event.target.href);
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
    console.log("location:", location);
    let html = '';
    //Think this first if statement is not needed
    if (location === '/') {
        html = await fetch('/users/').then(res => res.text());
        document.getElementById('content').innerHTML = html;
        console.log('Loaded /');
    }
    else if (location.startsWith('/users/game/')) {
        const username = location.split('/').pop();
        const url = `/users/game/${username}`;
        html = await fetch(url).then(res => res.text());
        document.getElementById('content').innerHTML = html;
        console.log('Loaded game.html for user:', username);
    }
    else {
        const route = routes[location] || routes[404];
        html = await fetch(route.urlPattern).then(res => res.text());
        document.getElementById('content').innerHTML = html;
        console.log('Loaded route:', route.urlPattern);
    }
}

window.onpopstate = locationHandler;
window.route = route;

locationHandler();
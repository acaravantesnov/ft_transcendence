const startsWithRoutes = [
    '/users/home/',
    '/users/waitlist/',
    '/users/play/',
    '/users/leaderboards/',
    '/users/profile/',
    '/users/friends/'
]

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
    if ((location == '/') || (location == '/users/home/')) {
        html = await fetch(`/users/home/${user.username}`).then(res => res.text());
    }
    else if (startsWithRoutes.some(route => location.startsWith(route))) {
        html = await fetch(location).then(res => res.text());
    }
    else { // routes
        const route = routes[location] || routes[404];
        html = await fetch(route.urlPattern).then(res => res.text());
    }
	window.alert(route);

    insertHTML(html, document.getElementById('content'));
}

window.onpopstate = locationHandler;
window.route = route;

locationHandler();

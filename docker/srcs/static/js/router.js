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
        title: 'Game',
        description: 'Game'
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
    console.log('route function. route:', event.target.href);
    window.history.pushState({}, '', event.target.href);
    locationHandler();
}

const locationHandler = async () => {
    const location = window.location.pathname;
    if (location.length == 0) {
        location = '/';
    }
    console.log("locationHandler function. location:", location);
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

function insertHTML(html, dest, append=false){
    // if no append is requested, clear the target element
    if(!append) dest.innerHTML = '';
    // create a temporary container and insert provided HTML code
    let container = document.createElement('div');
    container.innerHTML = html;
    // cache a reference to all the scripts in the container
    let scripts = container.querySelectorAll('script');
    // get all child elements and clone them in the target element
    let nodes = container.childNodes;
    for( let i=0; i< nodes.length; i++) dest.appendChild( nodes[i].cloneNode(true) );
    // force the found scripts to execute...
    for( let i=0; i< scripts.length; i++){
        let script = document.createElement('script');
        script.type = scripts[i].type || 'text/javascript';
        if( scripts[i].hasAttribute('src') ) script.src = scripts[i].src;
        script.innerHTML = scripts[i].innerHTML;
        document.head.appendChild(script);
        document.head.removeChild(script);
    }
    // done!
    return true;
}

window.onpopstate = locationHandler;
window.route = route;

locationHandler();
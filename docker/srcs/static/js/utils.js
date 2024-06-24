function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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

// Function to show the offcanvas
function showOffcanvas() {
    const offcanvas = document.getElementById('offcanvasExample');
    const existingBackdrop = document.querySelector('.offcanvas-backdrop');

    // Show offcanvas
    offcanvas.classList.add('show');
    offcanvas.style.display = 'block';

    // Add backdrop if it doesn't exist
    if (!existingBackdrop) {
        const backdrop = document.createElement('div');
        backdrop.className = 'offcanvas-backdrop fade show';
        backdrop.addEventListener('click', hideOffcanvas); // Add event listener to hide on click
        document.body.appendChild(backdrop);
    }
}

// Function to hide the offcanvas
function hideOffcanvas() {
    const offcanvas = document.getElementById('offcanvasExample');
    const backdrop = document.querySelector('.offcanvas-backdrop');

    // Hide offcanvas
    offcanvas.classList.remove('show');
    offcanvas.style.display = 'none';

    // Remove backdrop
    if (backdrop) {
        backdrop.classList.remove('show');
        backdrop.classList.add('fade-out');
        backdrop.removeEventListener('click', hideOffcanvas); // Remove event listener
        setTimeout(() => {
            backdrop.remove();
        }, 150); // Matches the fade-out duration
    }
}

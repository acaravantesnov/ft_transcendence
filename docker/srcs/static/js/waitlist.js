let intervalId = null;

async function addtowaitlist() {

    await fetch(`/users/waitlist/addtowaitlist/${currentUsername}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {})
        .catch(error => console.error('Error fetching data:', error));
};

document.getElementById('waitlistButton').addEventListener('click', function() {
    addtowaitlist();
});


async function checkwaitlist() {

    console.log(currentUsername);
    const response = await fetch(`/users/waitlist/checkwaitlist/${currentUsername}/`)
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error fetching data:', error));
    console.log(response);

    if (response.status == 'success') {
        let str = '';
        if (response.response.user_left == currentUsername) {
            str = '/users/play/' + currentUsername + '/' + response.response.room_name + '/left/';
        } else if (response.response.user_right == currentUsername) {
            str = '/users/play/' + currentUsername + '/' + response.response.room_name + '/right/';
        } else {
            str = '/users/play/' + currentUsername + '/' + response.response.room_name + '/spectator/';
        }
        console.log(str);
        const event = new CustomEvent('WAITLISTTRIGGER', { detail: { href: str } });
        document.dispatchEvent(event);
    }
};

document.addEventListener('WAITLISTTRIGGER', (e) => {
    const { href } = e.detail;
    const event = {
        preventDefault: () => {},
        target: { href }
    };
    if (intervalId !== null) {
        clearInterval(intervalId);
        console.log('Interval cleared');
    }
    console.log('Navigating to:', e.detail.href);
    route(event);
});

intervalId = setInterval(checkwaitlist, 5000);
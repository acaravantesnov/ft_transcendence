async function addtowaitlist() {

    const username = await getCurrentUsername();

    await fetch(`/users/waitlist/addtowaitlist/${username}/`, {
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

    const username = await getCurrentUsername();

    var response = await fetch(`/users/waitlist/checkwaitlist/${username}/`)
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error fetching data:', error));

    if (response.status == 'success') {
        let str = '';
        if (response.response.user_left == username) {
            str = '/users/play/' + username + '/' + response.response.room_name + '/left/';
        } else if (response.response.user_right == username) {
            str = '/users/play/' + username + '/' + response.response.room_name + '/right/';
        } else {
            str = '/users/play/' + username + '/' + response.response.room_name + '/spectator/';
        }
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
    route(event);
});

setInterval(checkwaitlist, 5000);
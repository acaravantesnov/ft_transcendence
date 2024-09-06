var user = {
    username: 'Guest',
    avatar: '/media/avatars/default.png'
};

async function updateUser() {
    try {
        let res = await fetch('/users/getUserInfo/');
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        user = await res.json();
        document.getElementById('offcanvasExampleLabel').innerHTML = user.username;
        document.getElementById('profile').innerHTML = user.profile_text;
        document.getElementById('friends').innerHTML = user.friends_text;
        document.getElementById('dashboard').innerHTML = user.dashboard_text;
        document.getElementById('sign_out').innerHTML = user.sign_out_text;
        document.getElementById('navbar-avatar').innerHTML = `<img src="${user.avatar}" alt="logo" style="width: 50px; height: 50px;">`;
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

setInterval(updateUser, 500);

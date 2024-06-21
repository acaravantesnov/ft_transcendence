document.getElementById('username').innerHTML = user.username;
document.getElementById('first_name').innerHTML = user.first_name;
document.getElementById('last_name').innerHTML = user.last_name;
document.getElementById('email').innerHTML = user.email;
document.getElementById('last_login').innerHTML = user.last_login;
document.getElementById('date_joined').innerHTML = user.date_joined;
document.getElementById('avatar').innerHTML = `<img src="/static/avatars/${user.avatar}" alt="logo" style="width: 50px; height: 50px;">`;
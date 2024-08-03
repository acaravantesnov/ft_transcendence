

document.getElementById('username').innerHTML = `<h5>${user.username}</h5>`;
document.getElementById('first_name').innerHTML = `<h5>First name: </h5>${user.first_name}`;
document.getElementById('last_name').innerHTML = `<h5>Last name: </h5>${user.last_name}`;
document.getElementById('email').innerHTML = `<h5>Email: </h5>${user.email}`;
document.getElementById('last_login').innerHTML = `<h5>Last login: </h5>${user.last_login}`;
document.getElementById('date_joined').innerHTML = `<h5>Date joined: </h5>${user.date_joined}`;

document.getElementById('avatar').innerHTML = `<img src="${user.avatar}" alt="logo" class="image-center" style="width: 15vh; height: 15vh;">`;

document.getElementById('edit_profile').getElementsByTagName('a')[0].setAttribute("href", "/users/editProfile/");
document.getElementById('change_password').getElementsByTagName('a')[0].setAttribute("href", `/users/changePassword/${user.username}`);
//document.getElementById('choose_avatar').getElementsByTagName('a')[0].setAttribute("href", `/users/editProfile/${user.username}`);

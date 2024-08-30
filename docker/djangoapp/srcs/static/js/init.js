
async function init () {

    const formDataAI = new FormData();
    const formDataM = new FormData();
    const formDataD = new FormData();
    const formDataA = new FormData();
    const formDataAl = new FormData();

    // Append fields individually
    formDataAI.append('username', 'AI');
    formDataAI.append('first_name', 'diegoantolin');
    formDataAI.append('last_name', 'galaxyBrain');
    formDataAI.append('email', 'AI@dagdag.mad');
    formDataAI.append('password', 'tutu');
    formDataAI.append('confirm_password', 'tutu');
    formDataAI.append('avatar', '/avatars/default.png');
    
    // Append fields individually
    formDataM.append('username', 'mortega');
    formDataM.append('first_name', 'Manuel');
    formDataM.append('last_name', 'Ortega');
    formDataM.append('email', 'mortega@42.fr');
    formDataM.append('password', '42');
    formDataM.append('confirm_password', '42');
    formDataM.append('avatar', '/avatars/default.png');

    // Append fields individually
    formDataD.append('username', 'digarcia');
    formDataD.append('first_name', 'Diego');
    formDataD.append('last_name', 'Garcia');
    formDataD.append('email', 'digarcia@42.fr');
    formDataD.append('password', '42');
    formDataD.append('confirm_password', '42');
    formDataD.append('avatar', '/avatars/default.png');

    // Append fields individually
    formDataA.append('username', 'acaravan');
    formDataA.append('first_name', 'Alberto');
    formDataA.append('last_name', 'Caravantes');
    formDataA.append('email', 'acaravan@42.fr');
    formDataA.append('password', '42');
    formDataA.append('confirm_password', '42');
    formDataA.append('avatar', '/avatars/default.png');

    // Append fields individually
    formDataAl.append('username', 'alaguila');
    formDataAl.append('first_name', 'Alex');
    formDataAl.append('last_name', 'Aguila');
    formDataAl.append('email', 'alaguila@42.fr');
    formDataAl.append('password', '42');
    formDataAl.append('confirm_password', '42');
    formDataAl.append('avatar', '/avatars/default.png');

		const responseIA = await fetch('/users/signUp/createUser/', {
			method: 'POST',
			body: formDataAI,
		});
		const responseM = await fetch('/users/signUp/createUser/', {
			method: 'POST',
			body: formDataM,
		});
		const responseD = await fetch('/users/signUp/createUser/', {
			method: 'POST',
			body: formDataD,
		});
		const responseA = await fetch('/users/signUp/createUser/', {
			method: 'POST',
			body: formDataA,
		});
		const responseAl = await fetch('/users/signUp/createUser/', {
			method: 'POST',
			body: formDataAl,
		});

}

init();

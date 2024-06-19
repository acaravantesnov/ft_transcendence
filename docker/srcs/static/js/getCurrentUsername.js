const getCurrentUsername = async () => {
    const response = await fetch('/users/getCurrentUsername/');
    const data = await response.json();
    const username = data.username;

    return username;
}
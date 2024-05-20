document.addEventListener('DOMContentLoaded', function() {
    const ball = document.getElementById('ball');
    let ballX = 50;
    let ballY = 50;
    let ballSpeedX = 2;
    let ballSpeedY = 2;

    function moveBall() {
        ballX += ballSpeedX;
        ballY += ballSpeedY;

        if (ballX + ball.offsetWidth >= window.innerWidth || ballX <= 0) {
            ballSpeedX *= -1;
        }

        if (ballY + ball.offsetHeight >= window.innerHeight || ballY <= 0) {
            ballSpeedY *= -1;
        }

        ball.style.left = ballX + 'px';
        ball.style.top = ballY + 'px';
        
        requestAnimationFrame(moveBall);
    }

    moveBall();
});

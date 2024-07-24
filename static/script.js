document.addEventListener('DOMContentLoaded', function() {
    function updateTime() {
        const now = new Date();
        const hours = now.getHours() % 12 || 12; 
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = now.getHours() >= 12 ? 'PM' : 'AM'; 
        const formattedTime = `${hours}:${minutes}:${seconds} ${ampm}`;
        document.getElementById('current-time').textContent = "IST "+formattedTime;
    }
    updateTime();
    setInterval(updateTime, 1000);
});

function toggleFullScreen(element) {
    if (!document.fullscreenElement) {
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        } else if (element.webkitRequestFullscreen) { 
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { 
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { 
            document.msExitFullscreen();
        }
    }
}
document.addEventListener('DOMContentLoaded', function() {
    function startTimer() {
        let seconds = 0;
        const timerElement = document.getElementById('timer');
        function updateTimerDisplay() {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const remainingSeconds = seconds % 60;
            const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
            timerElement.textContent = "Current Session "+formattedTime;
        }
        function incrementTimer() {
            seconds++;
            updateTimerDisplay();
        }
        updateTimerDisplay();
        setInterval(incrementTimer, 1000); 
    }
    startTimer();
});
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('start-button').addEventListener('click', () => {
        fetch('/start_radar', {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                console.log('Radar started successfully');
                const statusSpan = document.querySelector('.active-status');
                statusSpan.textContent = ' ACTIVE';
                statusSpan.style.color = 'green';
            } else {
                console.error('Failed to start radar');
            }
        }).catch(error => {
            console.error('Error starting radar:', error);
        });
    });

    document.getElementById('stop-button').addEventListener('click', () => {
        fetch('/stop_radar', {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                console.log('Radar stopped successfully');
                const statusSpan = document.querySelector('.active-status');
                statusSpan.textContent = 'IN-ACTIVE';
                statusSpan.style.color = 'red';
            } else {
                console.error('Failed to stop radar');
            }
        }).catch(error => {
            console.error('Error stopping radar:', error);
        });
    });
});


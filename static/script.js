document.addEventListener('DOMContentLoaded', function() {
    // Function to update the current time
    function updateTime() {
        const now = new Date();
        const hours = now.getHours() % 12 || 12; // Convert to 12-hour format
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = now.getHours() >= 12 ? 'PM' : 'AM'; // Determine AM/PM
        const formattedTime = `${hours}:${minutes}:${seconds} ${ampm}`;
        document.getElementById('current-time').textContent = "IST "+formattedTime;
    }

    // Initial call to display the time immediately
    updateTime();
    // Update time every second
    setInterval(updateTime, 1000);
});

function toggleFullScreen(element) {
    if (!document.fullscreenElement) {
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.mozRequestFullScreen) { // Firefox
            element.mozRequestFullScreen();
        } else if (element.webkitRequestFullscreen) { // Chrome, Safari and Opera
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) { // IE/Edge
            element.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { // Firefox
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { // Chrome, Safari and Opera
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { // IE/Edge
            document.msExitFullscreen();
        }
    }
}
document.addEventListener('DOMContentLoaded', function() {
    // Function to start the timer after the website is launched
    function startTimer() {
        let seconds = 0;
        const timerElement = document.getElementById('timer');

        // Function to update the timer display
        function updateTimerDisplay() {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const remainingSeconds = seconds % 60;
            const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
            timerElement.textContent = "Current Session "+formattedTime;
        }

        // Function to increment the timer
        function incrementTimer() {
            seconds++;
            updateTimerDisplay();
        }

        // Start the timer
        updateTimerDisplay();
        setInterval(incrementTimer, 1000); // Increment the timer every second
    }

    // Start the timer after the website is launched
    startTimer();
});

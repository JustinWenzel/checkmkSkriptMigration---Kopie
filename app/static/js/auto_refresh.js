let dropdown = document.getElementById("refreshSelect");
let refreshTimer = null;


window.addEventListener('DOMContentLoaded', function() {
    let savedValue = localStorage.getItem('refreshInterval');
    if (savedValue) {
        dropdown.value = savedValue;
        startRefreshTimer(parseInt(savedValue));
    }
});

dropdown.addEventListener("change", function() {
    let seconds = parseInt(this.value);
    
    
    localStorage.setItem('refreshInterval', seconds);
    
    
    startRefreshTimer(seconds);
});


function startRefreshTimer(seconds) {
    
    // Stop old timer otherwise it would run in background (setInterval, clearInterval)
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
    
    //Reload will be executed every time interval is reached
    if (seconds > 0) {
        refreshTimer = setInterval(function() {
            location.reload();
        }, seconds * 1000);
    }
}
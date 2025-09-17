// Timer functionality for workouts and rest periods

class Timer {
    constructor() {
        this.workoutStartTime = null;
        this.workoutTimer = null;
        this.restTimer = null;
        this.restStartTime = null;
        this.restDuration = 0;
        this.isResting = false;
        this.init();
    }

    init() {
        this.createTimerElements();
    }

    createTimerElements() {
        // Ensure timer display elements exist
        if (!document.getElementById('workoutTimer')) {
            console.warn('Workout timer element not found');
        }
        
        if (!document.getElementById('restTimer')) {
            console.warn('Rest timer element not found');
        }
    }

    startWorkoutTimer() {
        this.workoutStartTime = Date.now();
        this.workoutTimer = setInterval(() => {
            this.updateWorkoutTimer();
        }, 1000);
        
        console.log('Workout timer started');
    }

    stopWorkoutTimer() {
        if (this.workoutTimer) {
            clearInterval(this.workoutTimer);
            this.workoutTimer = null;
            console.log('Workout timer stopped');
        }
    }

    updateWorkoutTimer() {
        if (!this.workoutStartTime) return;

        const elapsed = Math.floor((Date.now() - this.workoutStartTime) / 1000);
        const formattedTime = this.formatTime(elapsed);
        
        const timerElement = document.getElementById('workoutTimer');
        if (timerElement) {
            timerElement.textContent = formattedTime;
        }
    }

    startRestTimer(duration = 90) {
        this.restDuration = duration;
        this.restStartTime = Date.now();
        this.isResting = true;

        // Show rest timer UI
        const restTimerElement = document.getElementById('restTimer');
        if (restTimerElement) {
            restTimerElement.style.display = 'block';
            restTimerElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // Start countdown
        this.restTimer = setInterval(() => {
            this.updateRestTimer();
        }, 1000);

        // Play rest notification sound (if available)
        this.playSound('rest_start');

        console.log(`Rest timer started for ${duration} seconds`);
    }

    updateRestTimer() {
        if (!this.restStartTime) return;

        const elapsed = Math.floor((Date.now() - this.restStartTime) / 1000);
        const remaining = this.restDuration - elapsed;

        if (remaining <= 0) {
            this.completeRest();
            return;
        }

        const formattedTime = this.formatTime(remaining);
        const restTimerDisplay = document.getElementById('restTimerDisplay');
        if (restTimerDisplay) {
            restTimerDisplay.textContent = formattedTime;
        }

        // Visual feedback for last 10 seconds
        if (remaining <= 10) {
            const restTimer = document.getElementById('restTimer');
            if (restTimer) {
                restTimer.classList.add('pulse-warning');
            }
        }

        // Audio feedback for last 3 seconds
        if (remaining <= 3 && remaining > 0) {
            this.playSound('countdown');
        }
    }

    completeRest() {
        this.stopRestTimer();
        this.playSound('rest_complete');
        
        // Show completion notification
        this.showRestCompleteNotification();
    }

    stopRestTimer() {
        if (this.restTimer) {
            clearInterval(this.restTimer);
            this.restTimer = null;
        }

        this.isResting = false;
        this.restStartTime = null;

        // Hide rest timer UI
        const restTimerElement = document.getElementById('restTimer');
        if (restTimerElement) {
            restTimerElement.style.display = 'none';
            restTimerElement.classList.remove('pulse-warning');
        }

        console.log('Rest timer stopped');
    }

    skipRest() {
        this.completeRest();
    }

    showRestCompleteNotification() {
        // Create notification
        const notification = document.createElement('div');
        notification.className = 'alert alert-success alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1060; min-width: 300px;';
        
        notification.innerHTML = `
            <div class="text-center">
                <h5><i data-feather="clock" class="me-2"></i>Rest Complete!</h5>
                <p class="mb-2">Ready for your next set?</p>
                <button type="button" class="btn btn-success btn-sm" onclick="this.parentElement.parentElement.remove()">
                    Let's Go!
                </button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);

        // Update feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    playSound(type) {
        // Audio feedback for timer events
        if ('speechSynthesis' in window) {
            let text = '';
            
            switch (type) {
                case 'rest_start':
                    text = 'Rest time started';
                    break;
                case 'countdown':
                    text = 'Almost done';
                    break;
                case 'rest_complete':
                    text = 'Rest complete, ready for next set';
                    break;
                default:
                    return;
            }

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.volume = 0.5;
            utterance.rate = 1;
            utterance.pitch = 1;
            
            // Only speak if user hasn't disabled it
            const audioEnabled = localStorage.getItem('fittracker_audio_enabled');
            if (audioEnabled !== 'false') {
                speechSynthesis.speak(utterance);
            }
        }
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    getWorkoutDuration() {
        if (!this.workoutStartTime) return 0;
        return Math.floor((Date.now() - this.workoutStartTime) / 1000);
    }

    getFormattedWorkoutDuration() {
        return this.formatTime(this.getWorkoutDuration());
    }

    // Preset rest intervals
    setRestInterval(type) {
        const intervals = {
            short: 60,    // 1 minute
            medium: 90,   // 1.5 minutes
            long: 180,    // 3 minutes
            strength: 300 // 5 minutes
        };

        const duration = intervals[type] || 90;
        this.startRestTimer(duration);
    }

    // Audio settings
    toggleAudio() {
        const currentSetting = localStorage.getItem('fittracker_audio_enabled');
        const newSetting = currentSetting === 'false' ? 'true' : 'false';
        localStorage.setItem('fittracker_audio_enabled', newSetting);
        
        return newSetting === 'true';
    }

    isAudioEnabled() {
        return localStorage.getItem('fittracker_audio_enabled') !== 'false';
    }
}

// Add CSS for timer animations
const timerStyle = document.createElement('style');
timerStyle.textContent = `
    .pulse-warning {
        animation: pulse-red 1s infinite;
    }
    
    @keyframes pulse-red {
        0% { border-color: #ffc107; }
        50% { border-color: #dc3545; }
        100% { border-color: #ffc107; }
    }
    
    .workout-timer {
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    .rest-timer {
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 2rem !important;
    }
    
    #restTimer {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    @media (max-width: 768px) {
        .rest-timer {
            font-size: 1.5rem !important;
        }
        
        .workout-timer {
            font-size: 1.2rem !important;
        }
    }
`;
document.head.appendChild(timerStyle);

// Global function for skip rest (called from template)
function skipRest() {
    if (window.timer) {
        window.timer.skipRest();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Timer;
}

// FitTracker Main Application JavaScript

class FitTrackerApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupPWA();
        this.setupNotifications();
        this.setupOfflineHandling();
        this.setupTouchOptimizations();
    }

    setupPWA() {
        // Handle PWA installation
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            
            // Show install button if available
            const installBtn = document.getElementById('installBtn');
            if (installBtn) {
                installBtn.classList.remove('d-none');
                installBtn.addEventListener('click', () => {
                    this.installPWA();
                });
            }
        });

        // Handle PWA installed event
        window.addEventListener('appinstalled', () => {
            console.log('FitTracker PWA installed successfully');
            this.hideInstallPrompt();
        });
    }

    installPWA() {
        if (this.deferredPrompt) {
            this.deferredPrompt.prompt();
            this.deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                } else {
                    console.log('User dismissed the install prompt');
                }
                this.deferredPrompt = null;
            });
        }
    }

    hideInstallPrompt() {
        const installBtn = document.getElementById('installBtn');
        if (installBtn) {
            installBtn.classList.add('d-none');
        }
    }

    setupNotifications() {
        if ('Notification' in window && 'serviceWorker' in navigator) {
            // Request notification permission
            Notification.requestPermission().then((permission) => {
                if (permission === 'granted') {
                    console.log('Notification permission granted');
                    this.scheduleWorkoutReminders();
                }
            });
        }
    }

    scheduleWorkoutReminders() {
        // Schedule daily workout reminders
        const now = new Date();
        const reminderTime = new Date();
        reminderTime.setHours(9, 0, 0, 0); // 9 AM reminder

        if (reminderTime <= now) {
            reminderTime.setDate(reminderTime.getDate() + 1);
        }

        const timeUntilReminder = reminderTime - now;

        setTimeout(() => {
            this.sendWorkoutReminder();
        }, timeUntilReminder);
    }

    sendWorkoutReminder() {
        if (Notification.permission === 'granted') {
            const notification = new Notification('Time for your workout!', {
                body: 'Keep up your fitness routine and achieve your goals.',
                icon: '/static/icons/icon-192.png',
                badge: '/static/icons/icon-192.png',
                tag: 'workout-reminder',
                requireInteraction: true
            });

            notification.onclick = function() {
                window.focus();
                window.location.href = '/dashboard';
                notification.close();
            };
        }
    }

    setupOfflineHandling() {
        // Handle online/offline status
        window.addEventListener('online', () => {
            this.showNetworkStatus('Back online! Your data will sync now.', 'success');
            this.syncOfflineData();
        });

        window.addEventListener('offline', () => {
            this.showNetworkStatus('You\'re offline. Your progress will be saved locally.', 'warning');
        });
    }

    showNetworkStatus(message, type) {
        // Create and show network status alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1060; max-width: 300px;';
        
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    syncOfflineData() {
        // Sync any offline data when back online
        const offlineData = localStorage.getItem('fittracker_offline_data');
        if (offlineData) {
            try {
                const data = JSON.parse(offlineData);
                // Send offline data to server
                this.sendOfflineData(data);
                localStorage.removeItem('fittracker_offline_data');
            } catch (error) {
                console.error('Error syncing offline data:', error);
            }
        }
    }

    sendOfflineData(data) {
        // Implementation for sending offline data to server
        console.log('Syncing offline data:', data);
    }

    setupTouchOptimizations() {
        // Optimize for mobile touch interactions
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });

        // Prevent zoom on double tap for better UX
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    }

    handleTouchStart(event) {
        // Add touch feedback
        const target = event.target.closest('.btn, .card, .exercise-card');
        if (target) {
            target.classList.add('touched');
        }
    }

    handleTouchEnd(event) {
        // Remove touch feedback
        const target = event.target.closest('.btn, .card, .exercise-card');
        if (target) {
            setTimeout(() => {
                target.classList.remove('touched');
            }, 150);
        }
    }

    // Utility methods
    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }

    saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }

    loadFromLocalStorage(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return null;
        }
    }
}

// Add CSS for touch feedback
const style = document.createElement('style');
style.textContent = `
    .touched {
        transform: scale(0.98);
        transition: transform 0.1s ease;
    }
    
    .btn.touched {
        opacity: 0.8;
    }
    
    .exercise-card.touched {
        transform: scale(0.98) translateY(-1px);
    }
`;
document.head.appendChild(style);

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.fitTrackerApp = new FitTrackerApp();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FitTrackerApp;
}

// Workout Tracking JavaScript

class WorkoutTracker {
    constructor(sessionId) {
        this.sessionId = sessionId;
        this.completedExercises = [];
        this.currentExercise = null;
        this.init();
    }

    init() {
        console.log('WorkoutTracker initialized for session:', this.sessionId);
        this.loadProgress();
    }

    loadProgress() {
        // Load any saved progress from localStorage
        const savedProgress = localStorage.getItem(`workout_${this.sessionId}`);
        if (savedProgress) {
            try {
                const progress = JSON.parse(savedProgress);
                this.completedExercises = progress.completedExercises || [];
                this.restoreUI();
            } catch (error) {
                console.error('Error loading workout progress:', error);
            }
        }
    }

    saveProgress() {
        // Save current progress to localStorage
        const progress = {
            sessionId: this.sessionId,
            completedExercises: this.completedExercises,
            timestamp: Date.now()
        };

        try {
            localStorage.setItem(`workout_${this.sessionId}`, JSON.stringify(progress));
        } catch (error) {
            console.error('Error saving workout progress:', error);
        }
    }

    restoreUI() {
        // Restore UI state from saved progress
        this.completedExercises.forEach(exerciseKey => {
            const exerciseBlock = document.querySelector(`[data-exercise="${exerciseKey}"]`);
            if (exerciseBlock) {
                this.markExerciseCompleted(exerciseBlock);
            }
        });
    }

    completeExercise(exerciseKey, exerciseBlock) {
        // Collect exercise data
        const setsData = this.collectSetsData(exerciseBlock);
        
        // Send data to server
        this.sendExerciseData(exerciseKey, setsData)
            .then(response => {
                if (response.success) {
                    this.completedExercises.push(exerciseKey);
                    this.markExerciseCompleted(exerciseBlock);
                    this.saveProgress();
                    
                    // Show success feedback
                    this.showFeedback('Exercise completed!', 'success');
                } else {
                    this.showFeedback('Error saving exercise data', 'error');
                }
            })
            .catch(error => {
                console.error('Error completing exercise:', error);
                this.showFeedback('Error completing exercise', 'error');
            });
    }

    collectSetsData(exerciseBlock) {
        const setRows = exerciseBlock.querySelectorAll('.set-row');
        const setsCompleted = [];
        const repsCompleted = [];
        const weightsUsed = [];

        setRows.forEach(row => {
            const checkbox = row.querySelector('.set-complete');
            const repsInput = row.querySelector('input[name="reps_completed[]"]');
            const weightInput = row.querySelector('input[name="weights_used[]"]');

            setsCompleted.push(checkbox.checked);
            repsCompleted.push(parseInt(repsInput.value) || 0);
            weightsUsed.push(parseFloat(weightInput.value) || 0);
        });

        return {
            sets_completed: setsCompleted,
            reps_completed: repsCompleted,
            weights_used: weightsUsed
        };
    }

    async sendExerciseData(exerciseKey, setsData) {
        const formData = new FormData();
        formData.append('session_id', this.sessionId);
        formData.append('exercise_key', exerciseKey);
        
        setsData.sets_completed.forEach(completed => {
            formData.append('sets_completed[]', completed);
        });
        setsData.reps_completed.forEach(reps => {
            formData.append('reps_completed[]', reps);
        });
        setsData.weights_used.forEach(weight => {
            formData.append('weights_used[]', weight);
        });

        try {
            const response = await fetch('/complete_exercise', {
                method: 'POST',
                body: formData
            });
            return await response.json();
        } catch (error) {
            console.error('Network error:', error);
            
            // Store offline for later sync
            this.storeOfflineData(exerciseKey, setsData);
            
            return { success: true }; // Assume success for offline handling
        }
    }

    storeOfflineData(exerciseKey, setsData) {
        const offlineData = JSON.parse(localStorage.getItem('fittracker_offline_data') || '[]');
        
        offlineData.push({
            type: 'complete_exercise',
            sessionId: this.sessionId,
            exerciseKey: exerciseKey,
            setsData: setsData,
            timestamp: Date.now()
        });

        localStorage.setItem('fittracker_offline_data', JSON.stringify(offlineData));
    }

    markExerciseCompleted(exerciseBlock) {
        const completeButton = exerciseBlock.querySelector('.complete-exercise');
        if (completeButton) {
            completeButton.innerHTML = '<i data-feather="check-circle" class="me-1"></i>Completed';
            completeButton.classList.remove('btn-success');
            completeButton.classList.add('btn-outline-success');
            completeButton.disabled = true;
        }

        // Add completed styling to the entire exercise block
        exerciseBlock.classList.add('exercise-completed');

        // Update feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    showFeedback(message, type) {
        // Create feedback alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of exercise container
        const exerciseContainer = document.getElementById('exerciseContainer');
        exerciseContainer.insertBefore(alertDiv, exerciseContainer.firstChild);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }

    calculateWorkoutStats() {
        const completedCount = this.completedExercises.length;
        const totalExercises = document.querySelectorAll('.exercise-block').length;
        const completionPercentage = totalExercises > 0 ? (completedCount / totalExercises) * 100 : 0;

        return {
            completed: completedCount,
            total: totalExercises,
            percentage: Math.round(completionPercentage)
        };
    }

    getWorkoutSummary() {
        const stats = this.calculateWorkoutStats();
        const totalSets = this.calculateTotalSets();
        const totalVolume = this.calculateTotalVolume();

        return {
            exercisesCompleted: stats.completed,
            totalExercises: stats.total,
            completionPercentage: stats.percentage,
            totalSets: totalSets,
            totalVolume: totalVolume
        };
    }

    calculateTotalSets() {
        let totalSets = 0;
        document.querySelectorAll('.set-complete:checked').forEach(() => {
            totalSets++;
        });
        return totalSets;
    }

    calculateTotalVolume() {
        let totalVolume = 0;
        document.querySelectorAll('.set-complete:checked').forEach(checkbox => {
            const row = checkbox.closest('.set-row');
            const reps = parseInt(row.querySelector('input[name="reps_completed[]"]').value) || 0;
            const weight = parseFloat(row.querySelector('input[name="weights_used[]"]').value) || 0;
            totalVolume += reps * weight;
        });
        return totalVolume;
    }

    cleanup() {
        // Clean up localStorage when workout is finished
        localStorage.removeItem(`workout_${this.sessionId}`);
    }
}

// Add CSS for completed exercises
const workoutStyle = document.createElement('style');
workoutStyle.textContent = `
    .exercise-completed {
        opacity: 0.8;
        background-color: rgba(25, 135, 84, 0.1);
        border-color: rgba(25, 135, 84, 0.2);
    }
    
    .exercise-completed .card-header {
        background-color: rgba(25, 135, 84, 0.1);
    }
    
    .completed-set {
        background-color: rgba(25, 135, 84, 0.2) !important;
    }
    
    .set-row.completed-set input {
        background-color: rgba(25, 135, 84, 0.1);
    }
`;
document.head.appendChild(workoutStyle);

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorkoutTracker;
}

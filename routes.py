from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import WorkoutPlan, WorkoutSession
from datetime import datetime, timedelta
import json

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/dashboard')
@login_required
def dashboard():
    plans = WorkoutPlan.get_by_user(current_user.id)
    sessions = WorkoutSession.get_by_user(current_user.id)
    
    # Get recent sessions for stats
    recent_sessions = [s for s in sessions if s.end_time and 
                      s.end_time > datetime.now() - timedelta(days=30)]
    
    stats = {
        'total_plans': len(plans),
        'total_workouts': len([s for s in sessions if s.end_time]),
        'this_month': len(recent_sessions),
        'streak': calculate_streak(sessions)
    }
    
    return render_template('dashboard.html', plans=plans, stats=stats, recent_sessions=recent_sessions[:5])

@main_routes.route('/create_plan', methods=['GET', 'POST'])
@login_required
def create_plan():
    if request.method == 'POST':
        name = request.form.get('name')
        selected_exercises = request.form.getlist('exercises')
        
        if not name:
            flash("Workout plan name is required.", "error")
            return redirect(url_for('main_routes.create_plan'))
        
        exercises = []
        for exercise_key in selected_exercises:
            sets = request.form.get(f'sets_{exercise_key}', 3, type=int)
            reps = request.form.get(f'reps_{exercise_key}', 10, type=int)
            weight = request.form.get(f'weight_{exercise_key}', 0, type=float)
            
            exercises.append({
                'exercise_key': exercise_key,
                'sets': sets,
                'reps': reps,
                'weight': weight
            })
        
        plan = WorkoutPlan(name=name, user_id=current_user.id, exercises=exercises)
        plan.save()
        
        flash(f"Workout plan '{name}' created successfully!", "success")
        return redirect(url_for('main_routes.dashboard'))
    
    from models import EXERCISE_LIBRARY
    exercises = EXERCISE_LIBRARY
    return render_template('workout_plan.html', exercises=exercises)

@main_routes.route('/exercise_library')
@login_required
def exercise_library():
    from models import EXERCISE_LIBRARY
    exercises = EXERCISE_LIBRARY
    return render_template('exercise_library.html', exercises=exercises)

@main_routes.route('/start_workout/<plan_id>')
@login_required
def start_workout(plan_id):
    plan = WorkoutPlan.get(plan_id)
    
    if not plan or plan.user_id != current_user.id:
        flash("Workout plan not found.", "error")
        return redirect(url_for('main_routes.dashboard'))
    
    session = WorkoutSession(plan_id=plan_id, user_id=current_user.id)
    session.save()
    
    return render_template('track_workout.html', plan=plan, session=session)

@main_routes.route('/complete_exercise', methods=['POST'])
@login_required
def complete_exercise():
    session_id = request.form.get('session_id')
    exercise_key = request.form.get('exercise_key')
    sets_completed = request.form.getlist('sets_completed[]')
    reps_completed = request.form.getlist('reps_completed[]')
    weights_used = request.form.getlist('weights_used[]')
    
    session = WorkoutSession.get(session_id)
    
    if not session or session.user_id != current_user.id:
        return jsonify({'error': 'Session not found'}), 404
    
    exercise_data = {
        'exercise_key': exercise_key,
        'sets': []
    }
    
    for i in range(len(sets_completed)):
        if sets_completed[i] == 'true':
            exercise_data['sets'].append({
                'reps': int(reps_completed[i]) if reps_completed[i] else 0,
                'weight': float(weights_used[i]) if weights_used[i] else 0
            })
    
    session.exercises_completed.append(exercise_data)
    session.save()
    
    return jsonify({'success': True})

@main_routes.route('/finish_workout', methods=['POST'])
@login_required
def finish_workout():
    session_id = request.form.get('session_id')
    notes = request.form.get('notes', '')
    
    session = WorkoutSession.get(session_id)
    
    if not session or session.user_id != current_user.id:
        flash("Workout session not found.", "error")
        return redirect(url_for('main_routes.dashboard'))
    
    session.complete(notes)
    flash("Workout completed! Great job!", "success")
    return redirect(url_for('main_routes.dashboard'))

@main_routes.route('/progress')
@login_required
def progress():
    sessions = WorkoutSession.get_by_user(current_user.id)
    completed_sessions = [s for s in sessions if s.end_time]
    
    # Prepare data for charts
    monthly_data = {}
    exercise_data = {}
    
    for session in completed_sessions:
        month_key = session.end_time.strftime('%Y-%m')
        monthly_data[month_key] = monthly_data.get(month_key, 0) + 1
        
        for exercise in session.exercises_completed:
            exercise_key = exercise['exercise_key']
            total_volume = sum(set_data['reps'] * set_data['weight'] for set_data in exercise['sets'])
            if exercise_key not in exercise_data:
                exercise_data[exercise_key] = []
            exercise_data[exercise_key].append({
                'date': session.end_time.isoformat(),
                'volume': total_volume
            })
    
    return render_template('progress.html', 
                         monthly_data=json.dumps(monthly_data),
                         exercise_data=json.dumps(exercise_data))

def calculate_streak(sessions):
    """Calculate current workout streak"""
    completed_sessions = [s for s in sessions if s.end_time]
    if not completed_sessions:
        return 0
    
    # Sort by end time
    completed_sessions.sort(key=lambda x: x.end_time, reverse=True)
    
    streak = 0
    current_date = datetime.now().date()
    
    for session in completed_sessions:
        session_date = session.end_time.date()
        days_diff = (current_date - session_date).days
        
        if days_diff <= 1 and (streak == 0 or days_diff <= streak + 1):
            streak += 1
            current_date = session_date
        else:
            break
    
    return streak

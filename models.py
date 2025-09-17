from app import db
from flask_login import UserMixin
from datetime import datetime
import uuid

# Exercise library data
EXERCISE_LIBRARY = {
    'push_ups': {
        'name': 'Push-ups',
        'muscle_groups': ['Chest', 'Shoulders', 'Triceps'],
        'description': 'Classic bodyweight exercise for upper body strength',
        'equipment': 'Bodyweight'
    },
    'squats': {
        'name': 'Squats',
        'muscle_groups': ['Quadriceps', 'Glutes', 'Hamstrings'],
        'description': 'Fundamental lower body exercise',
        'equipment': 'Bodyweight'
    },
    'deadlifts': {
        'name': 'Deadlifts',
        'muscle_groups': ['Hamstrings', 'Glutes', 'Back'],
        'description': 'Compound movement for posterior chain',
        'equipment': 'Barbell'
    },
    'bench_press': {
        'name': 'Bench Press',
        'muscle_groups': ['Chest', 'Shoulders', 'Triceps'],
        'description': 'Classic upper body pressing movement',
        'equipment': 'Barbell'
    },
    'pull_ups': {
        'name': 'Pull-ups',
        'muscle_groups': ['Back', 'Biceps'],
        'description': 'Bodyweight pulling exercise',
        'equipment': 'Pull-up bar'
    },
    'lunges': {
        'name': 'Lunges',
        'muscle_groups': ['Quadriceps', 'Glutes'],
        'description': 'Single-leg strength exercise',
        'equipment': 'Bodyweight'
    },
    'planks': {
        'name': 'Planks',
        'muscle_groups': ['Core', 'Shoulders'],
        'description': 'Isometric core strengthening exercise',
        'equipment': 'Bodyweight'
    },
    'rows': {
        'name': 'Rows',
        'muscle_groups': ['Back', 'Biceps'],
        'description': 'Horizontal pulling movement',
        'equipment': 'Dumbbells'
    }
}

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    workout_plans = db.relationship('WorkoutPlan', backref='owner', lazy=True, cascade='all, delete-orphan')
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, email, username, google_id=None):
        self.email = email
        self.username = username
        self.google_id = google_id
        
    @staticmethod
    def get(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_google_id(google_id):
        return User.query.filter_by(google_id=google_id).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    exercises = db.Column(db.JSON, nullable=False, default=list)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    workout_sessions = db.relationship('WorkoutSession', backref='plan', lazy=True)
    
    def __init__(self, name, user_id, exercises=None):
        self.name = name
        self.user_id = user_id
        self.exercises = exercises or []
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @staticmethod
    def get_by_user(user_id):
        return WorkoutPlan.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get(plan_id):
        return WorkoutPlan.query.get(plan_id)

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = db.Column(db.String(36), db.ForeignKey('workout_plans.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    exercises_completed = db.Column(db.JSON, nullable=False, default=list)
    notes = db.Column(db.Text, nullable=True, default="")
    
    def __init__(self, plan_id, user_id):
        self.plan_id = plan_id
        self.user_id = user_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def complete(self, notes=""):
        self.end_time = datetime.utcnow()
        self.notes = notes
        return self.save()
    
    @staticmethod
    def get_by_user(user_id):
        return WorkoutSession.query.filter_by(user_id=user_id).order_by(WorkoutSession.start_time.desc()).all()
    
    @staticmethod
    def get(session_id):
        return WorkoutSession.query.get(session_id)
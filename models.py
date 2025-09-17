import os
from flask_login import UserMixin
from pymongo import MongoClient
from datetime import datetime
import uuid
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client.fittracker

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

class User(UserMixin):
    def __init__(self, email, username, google_id=None, user_id=None, created_at=None, fitness_level='unspecified'):
        self.id = user_id or str(uuid.uuid4())
        self.email = email
        self.username = username
        self.google_id = google_id
        self.fitness_level = fitness_level if fitness_level in ['beginner', 'intermediate', 'advanced', 'unspecified'] else 'unspecified'
        self.created_at = created_at or datetime.utcnow()
        
    @staticmethod
    def get(user_id):
        user_data = db.users.find_one({"_id": user_id})
        if user_data:
            return User(
                email=user_data['email'],
                username=user_data['username'],
                google_id=user_data.get('google_id'),
                user_id=user_data['_id'],
                created_at=user_data.get('created_at'),
                fitness_level=user_data.get('fitness_level', 'unspecified')
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        user_data = db.users.find_one({"email": email})
        if user_data:
            return User(
                email=user_data['email'],
                username=user_data['username'],
                google_id=user_data.get('google_id'),
                user_id=user_data['_id'],
                created_at=user_data.get('created_at'),
                fitness_level=user_data.get('fitness_level', 'unspecified')
            )
        return None
    
    @staticmethod
    def get_by_google_id(google_id):
        user_data = db.users.find_one({"google_id": google_id})
        if user_data:
            return User(
                email=user_data['email'],
                username=user_data['username'],
                google_id=user_data.get('google_id'),
                user_id=user_data['_id'],
                created_at=user_data.get('created_at'),
                fitness_level=user_data.get('fitness_level', 'unspecified')
            )
        return None
    
    def save(self):
        user_doc = {
            "_id": self.id,
            "email": self.email,
            "username": self.username,
            "google_id": self.google_id,
            "fitness_level": self.fitness_level,
            "created_at": self.created_at
        }
        db.users.update_one(
            {"_id": self.id},
            {"$set": user_doc},
            upsert=True
        )
        return self

class WorkoutPlan:
    def __init__(self, name, user_id, exercises=None, level='unspecified', plan_id=None, created_at=None):
        self.id = plan_id or str(uuid.uuid4())
        self.name = name
        self.user_id = user_id
        self.exercises = exercises or []
        self.level = level if level in ['beginner', 'intermediate', 'advanced', 'unspecified'] else 'unspecified'
        self.created_at = created_at or datetime.utcnow()
    
    def save(self):
        plan_doc = {
            "_id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "exercises": self.exercises,
            "level": self.level,
            "created_at": self.created_at
        }
        db.workout_plans.update_one(
            {"_id": self.id},
            {"$set": plan_doc},
            upsert=True
        )
        return self
    
    @staticmethod
    def get_by_user(user_id, level=None):
        query = {"user_id": user_id}
        if level:
            query["level"] = level
        
        plans = []
        for plan_data in db.workout_plans.find(query).sort("created_at", -1):
            plans.append(WorkoutPlan(
                name=plan_data['name'],
                user_id=plan_data['user_id'],
                exercises=plan_data.get('exercises', []),
                level=plan_data.get('level', 'unspecified'),
                plan_id=plan_data['_id'],
                created_at=plan_data.get('created_at')
            ))
        return plans
    
    @staticmethod
    def get(plan_id):
        plan_data = db.workout_plans.find_one({"_id": plan_id})
        if plan_data:
            return WorkoutPlan(
                name=plan_data['name'],
                user_id=plan_data['user_id'],
                exercises=plan_data.get('exercises', []),
                level=plan_data.get('level', 'unspecified'),
                plan_id=plan_data['_id'],
                created_at=plan_data.get('created_at')
            )
        return None

class WorkoutSession:
    def __init__(self, plan_id, user_id, session_id=None, start_time=None, end_time=None, exercises_completed=None, notes=""):
        self.id = session_id or str(uuid.uuid4())
        self.plan_id = plan_id
        self.user_id = user_id
        self.start_time = start_time or datetime.utcnow()
        self.end_time = end_time
        self.exercises_completed = exercises_completed or []
        self.notes = notes
    
    def save(self):
        session_doc = {
            "_id": self.id,
            "plan_id": self.plan_id,
            "user_id": self.user_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "exercises_completed": self.exercises_completed,
            "notes": self.notes
        }
        db.workout_sessions.update_one(
            {"_id": self.id},
            {"$set": session_doc},
            upsert=True
        )
        return self
    
    def complete(self, notes=""):
        self.end_time = datetime.utcnow()
        self.notes = notes
        return self.save()
    
    @staticmethod
    def get_by_user(user_id):
        sessions = []
        for session_data in db.workout_sessions.find({"user_id": user_id}).sort("start_time", -1):
            sessions.append(WorkoutSession(
                plan_id=session_data['plan_id'],
                user_id=session_data['user_id'],
                session_id=session_data['_id'],
                start_time=session_data.get('start_time'),
                end_time=session_data.get('end_time'),
                exercises_completed=session_data.get('exercises_completed', []),
                notes=session_data.get('notes', "")
            ))
        return sessions
    
    @staticmethod
    def get(session_id):
        session_data = db.workout_sessions.find_one({"_id": session_id})
        if session_data:
            return WorkoutSession(
                plan_id=session_data['plan_id'],
                user_id=session_data['user_id'],
                session_id=session_data['_id'],
                start_time=session_data.get('start_time'),
                end_time=session_data.get('end_time'),
                exercises_completed=session_data.get('exercises_completed', []),
                notes=session_data.get('notes', "")
            )
        return None
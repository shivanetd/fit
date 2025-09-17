from flask_login import UserMixin
from datetime import datetime
import uuid

class User(UserMixin):
    def __init__(self, email, username, google_id=None):
        self.id = str(uuid.uuid4())
        self.email = email
        self.username = username
        self.google_id = google_id
        self.created_at = datetime.now()
        
    @staticmethod
    def get(user_id):
        from app import app
        return app.storage['users'].get(user_id)
    
    @staticmethod
    def get_by_email(email):
        from app import app
        for user in app.storage['users'].values():
            if user.email == email:
                return user
        return None
    
    def save(self):
        from app import app
        app.storage['users'][self.id] = self
        return self

class WorkoutPlan:
    def __init__(self, name, user_id, exercises=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.user_id = user_id
        self.exercises = exercises or []
        self.created_at = datetime.now()
    
    def save(self):
        from app import app
        app.storage['workout_plans'][self.id] = self
        return self
    
    @staticmethod
    def get_by_user(user_id):
        from app import app
        return [plan for plan in app.storage['workout_plans'].values() 
                if plan.user_id == user_id]

class WorkoutSession:
    def __init__(self, plan_id, user_id):
        self.id = str(uuid.uuid4())
        self.plan_id = plan_id
        self.user_id = user_id
        self.start_time = datetime.now()
        self.end_time = None
        self.exercises_completed = []
        self.notes = ""
    
    def save(self):
        from app import app
        app.storage['workout_sessions'][self.id] = self
        return self
    
    def complete(self, notes=""):
        self.end_time = datetime.now()
        self.notes = notes
        return self.save()
    
    @staticmethod
    def get_by_user(user_id):
        from app import app
        return [session for session in app.storage['workout_sessions'].values() 
                if session.user_id == user_id]

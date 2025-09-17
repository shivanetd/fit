import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for PWA functionality
CORS(app)

# Configure MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")

# Configure Flask-Session to use MongoDB
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = None  # Will be set after mongo initialization
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'fittracker:'
app.config['SESSION_MONGODB_DB'] = 'fittracker'
app.config['SESSION_MONGODB_COLLECT'] = 'sessions'

# Initialize MongoDB
mongo = PyMongo(app)

# Set MongoDB for sessions
app.config['SESSION_MONGODB'] = mongo.cx

# Initialize Flask-Session
Session(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main_routes.index'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get(user_id)

# Register blueprints
from google_auth import google_auth
app.register_blueprint(google_auth)

from routes import main_routes
app.register_blueprint(main_routes)

# Exercise library data - moved from storage to a simple dictionary
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
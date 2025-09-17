// MongoDB initialization script for FitTracker application
// This script creates the application user with proper permissions

db = db.getSiblingDB('fittracker');

// Create application user
db.createUser({
  user: 'fittracker_user',
  pwd: process.env.MONGO_PASSWORD || 'change_in_production',
  roles: [
    {
      role: 'readWrite',
      db: 'fittracker'
    }
  ]
});

// Create indexes for performance
db.workout_plans.createIndex({ "user_id": 1, "level": 1, "created_at": -1 });
db.workout_sessions.createIndex({ "user_id": 1, "start_time": -1 });
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "google_id": 1 }, { unique: true, sparse: true });

print('FitTracker database initialized successfully');
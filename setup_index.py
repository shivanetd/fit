#!/usr/bin/env python3
"""
Script to set up database indexes and backfill existing workout plans with fitness levels
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import mongo

def setup_database():
    with app.app_context():
        try:
            # Check database connection
            mongo.db.command('ping')
            print("✓ MongoDB connection successful")
            
            # Count existing plans
            plans_count = mongo.db.workout_plans.count_documents({})
            print(f"✓ Found {plans_count} existing workout plans")
            
            # Create compound index for efficient querying
            index_name = 'user_level_created_idx'
            try:
                result = mongo.db.workout_plans.create_index([
                    ('user_id', 1),
                    ('level', 1), 
                    ('created_at', -1)
                ], name=index_name)
                print(f"✓ Created index: {result}")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"✓ Index {index_name} already exists")
                else:
                    print(f"✗ Index creation failed: {e}")
            
            # Backfill existing plans without level field
            plans_without_level = mongo.db.workout_plans.count_documents({
                'level': {'$exists': False}
            })
            
            if plans_without_level > 0:
                print(f"✓ Found {plans_without_level} plans without level field")
                result = mongo.db.workout_plans.update_many(
                    {'level': {'$exists': False}},
                    {'$set': {'level': 'unspecified'}}
                )
                print(f"✓ Updated {result.modified_count} plans with default level 'unspecified'")
            else:
                print("✓ All plans already have level field")
            
            # List current indexes
            indexes = list(mongo.db.workout_plans.list_indexes())
            print("\n✓ Current indexes:")
            for idx in indexes:
                print(f"  - {idx['name']}: {idx.get('key', 'N/A')}")
                
            print("\n✓ Database setup completed successfully!")
            
        except Exception as e:
            print(f"✗ Error setting up database: {e}")
            return False
    return True

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
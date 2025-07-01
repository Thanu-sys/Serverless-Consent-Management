#!/usr/bin/env python3
"""
Startup script for the Consent Management API
This script will:
1. Create the database if it doesn't exist
2. Seed initial data
3. Start the Flask server
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly set up"""
    load_dotenv()
    
    # Check if DATABASE_URL is set
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        print("Please create a .env file with your database configuration")
        return False
    
    print("✓ Environment variables loaded")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_database():
    """Create database and tables"""
    print("Creating database and tables...")
    try:
        # Import and run database creation
        from create_db import create_database
        create_database()
        
        # Import and run app to create tables
        from app import app, db
        with app.app_context():
            db.create_all()
        
        print("✓ Database and tables created")
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def seed_data():
    """Seed initial data"""
    print("Seeding initial data...")
    try:
        from seed_data import seed_data
        seed_data()
        print("✓ Initial data seeded")
        return True
    except Exception as e:
        print(f"Error seeding data: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print("API endpoints will be available at: http://localhost:5000/api")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    """Main startup function"""
    print("Consent Management API Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Seed data
    if not seed_data():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 
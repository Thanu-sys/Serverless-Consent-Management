from app import app, db, Purpose
from datetime import datetime

def seed_data():
    with app.app_context():
        # Check if we already have purposes
        if Purpose.query.count() > 0:
            print("Database already has purposes, skipping seed data.")
            return

        # Create some test purposes
        purposes = [
            Purpose(
                name="Marketing Communications",
                description="Receive marketing emails and promotional offers"
            ),
            Purpose(
                name="Analytics",
                description="Allow us to analyze your usage patterns to improve our services"
            ),
            Purpose(
                name="Personalization",
                description="Personalize your experience based on your preferences"
            ),
            Purpose(
                name="Third-party Sharing",
                description="Share your data with trusted third-party partners"
            )
        ]

        # Add purposes to database
        for purpose in purposes:
            db.session.add(purpose)
        
        try:
            db.session.commit()
            print("Successfully added test purposes to the database!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding test purposes: {e}")

if __name__ == "__main__":
    seed_data() 
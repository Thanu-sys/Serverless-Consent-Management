#!/usr/bin/env python3
"""
Test script for the Consent Management API using SQLite
This will help verify the backend works without AWS RDS connection issues
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app)

# Use SQLite for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_consent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models (same as main app)
class Purpose(db.Model):
    __tablename__ = 'purposes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

class Consent(db.Model):
    __tablename__ = 'consents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    purpose_id = db.Column(db.Integer, db.ForeignKey('purposes.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    purpose = db.relationship('Purpose', backref=db.backref('consents', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'purpose_id': self.purpose_id,
            'purpose_name': self.purpose.name if self.purpose else None,
            'status': self.status,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Routes (same as main app)
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/purposes', methods=['GET'])
def get_purposes():
    try:
        purposes = Purpose.query.all()
        return jsonify([purpose.to_dict() for purpose in purposes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent', methods=['GET'])
def get_consent():
    try:
        user_id = request.args.get('user_id')
        purpose_id = request.args.get('purpose_id')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
            
        query = Consent.query.filter_by(user_id=user_id)
        
        if purpose_id:
            query = query.filter_by(purpose_id=purpose_id)
            
        consents = query.all()
        return jsonify([consent.to_dict() for consent in consents])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent', methods=['POST'])
def update_consent():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        purpose_id = data.get('purpose_id')
        status = data.get('status')
        
        if not all([user_id, purpose_id, status is not None]):
            return jsonify({'error': 'user_id, purpose_id, and status are required'}), 400
            
        # Check if purpose exists
        purpose = Purpose.query.get(purpose_id)
        if not purpose:
            return jsonify({'error': 'Invalid purpose_id'}), 400
            
        # Update or create consent
        consent = Consent.query.filter_by(
            user_id=user_id,
            purpose_id=purpose_id
        ).first()
        
        if consent:
            consent.status = status
            consent.ip_address = request.remote_addr
        else:
            consent = Consent(
                user_id=user_id,
                purpose_id=purpose_id,
                status=status,
                ip_address=request.remote_addr
            )
            db.session.add(consent)
            
        db.session.commit()
        return jsonify(consent.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent/bulk', methods=['POST'])
def bulk_update_consent():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        consents = data.get('consents', [])
        
        if not user_id or not consents:
            return jsonify({'error': 'user_id and consents array are required'}), 400
        
        results = []
        
        for consent_data in consents:
            purpose_id = consent_data.get('purpose_id')
            status = consent_data.get('status')
            
            if purpose_id is None or status is None:
                continue
                
            # Check if purpose exists
            purpose = Purpose.query.get(purpose_id)
            if not purpose:
                continue
                
            # Update or create consent
            consent = Consent.query.filter_by(
                user_id=user_id,
                purpose_id=purpose_id
            ).first()
            
            if consent:
                consent.status = status
                consent.ip_address = request.remote_addr
            else:
                consent = Consent(
                    user_id=user_id,
                    purpose_id=purpose_id,
                    status=status,
                    ip_address=request.remote_addr
                )
                db.session.add(consent)
            
            results.append(consent.to_dict())
        
        db.session.commit()
        return jsonify({'message': 'Bulk update successful', 'consents': results})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent/stats', methods=['GET'])
def get_consent_stats():
    try:
        total_consents = Consent.query.count()
        active_consents = Consent.query.filter_by(status=True).count()
        inactive_consents = Consent.query.filter_by(status=False).count()
        
        # Get stats by purpose
        purpose_stats = db.session.query(
            Purpose.name,
            db.func.count(Consent.id).label('total'),
            db.func.sum(db.case([(Consent.status == True, 1)], else_=0)).label('active')
        ).join(Consent).group_by(Purpose.id, Purpose.name).all()
        
        stats = {
            'total_consents': total_consents,
            'active_consents': active_consents,
            'inactive_consents': inactive_consents,
            'consent_rate': (active_consents / total_consents * 100) if total_consents > 0 else 0,
            'by_purpose': [
                {
                    'purpose_name': stat.name,
                    'total': stat.total,
                    'active': stat.active,
                    'rate': (stat.active / stat.total * 100) if stat.total > 0 else 0
                }
                for stat in purpose_stats
            ]
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def seed_test_data():
    """Seed test data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if we already have purposes
        if Purpose.query.count() > 0:
            print("Database already has purposes, skipping seed data.")
            return

        # Create test purposes
        purposes = [
            Purpose(name="Marketing Communications", description="Receive marketing emails and promotional offers"),
            Purpose(name="Analytics", description="Allow us to analyze your usage patterns to improve our services"),
            Purpose(name="Personalization", description="Personalize your experience based on your preferences"),
            Purpose(name="Third-party Sharing", description="Share your data with trusted third-party partners")
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

if __name__ == '__main__':
    print("Starting Consent Management API (SQLite Test Version)")
    print("=" * 50)
    
    # Seed test data
    seed_test_data()
    
    print("Server will be available at: http://localhost:5001")
    print("API endpoints will be available at: http://localhost:5001/api")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start server on different port
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
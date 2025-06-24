from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration - use pg8000 instead of psycopg2
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '').replace('postgresql://', 'postgresql+pg8000://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
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

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/purposes', methods=['GET'])
def get_purposes():
    """Get all purposes"""
    try:
        purposes = Purpose.query.all()
        return jsonify([purpose.to_dict() for purpose in purposes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/purposes/<int:purpose_id>', methods=['GET'])
def get_purpose(purpose_id):
    """Get a specific purpose by ID"""
    try:
        purpose = Purpose.query.get_or_404(purpose_id)
        return jsonify(purpose.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent', methods=['GET'])
def get_consent():
    """Get consent records for a user"""
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

@app.route('/api/consent/<int:consent_id>', methods=['GET'])
def get_consent_by_id(consent_id):
    """Get a specific consent record by ID"""
    try:
        consent = Consent.query.get_or_404(consent_id)
        return jsonify(consent.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent', methods=['POST'])
def update_consent():
    """Update or create a consent record"""
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
    """Update multiple consent records at once"""
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

@app.route('/api/consent/<int:consent_id>', methods=['DELETE'])
def delete_consent(consent_id):
    """Delete a consent record"""
    try:
        consent = Consent.query.get_or_404(consent_id)
        db.session.delete(consent)
        db.session.commit()
        return jsonify({'message': 'Consent record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent/user/<user_id>', methods=['DELETE'])
def delete_user_consents(user_id):
    """Delete all consent records for a user"""
    try:
        consents = Consent.query.filter_by(user_id=user_id).all()
        for consent in consents:
            db.session.delete(consent)
        db.session.commit()
        return jsonify({'message': f'All consent records for user {user_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent/stats', methods=['GET'])
def get_consent_stats():
    """Get consent statistics"""
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

@app.route('/api/consent/user/<user_id>/history', methods=['GET'])
def get_user_consent_history(user_id):
    """Get consent history for a specific user"""
    try:
        consents = Consent.query.filter_by(user_id=user_id).order_by(Consent.updated_at.desc()).all()
        
        # Group by purpose and show history
        history = {}
        for consent in consents:
            purpose_name = consent.purpose.name if consent.purpose else f"Purpose {consent.purpose_id}"
            if purpose_name not in history:
                history[purpose_name] = []
            
            history[purpose_name].append({
                'status': consent.status,
                'ip_address': consent.ip_address,
                'updated_at': consent.updated_at.isoformat()
            })
        
        return jsonify({
            'user_id': user_id,
            'consent_history': history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consent/check', methods=['POST'])
def check_consent_status():
    """Check if a user has given consent for specific purposes"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        purpose_ids = data.get('purpose_ids', [])
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if not purpose_ids:
            return jsonify({'error': 'purpose_ids array is required'}), 400
        
        results = {}
        for purpose_id in purpose_ids:
            consent = Consent.query.filter_by(
                user_id=user_id,
                purpose_id=purpose_id
            ).first()
            
            purpose = Purpose.query.get(purpose_id)
            purpose_name = purpose.name if purpose else f"Purpose {purpose_id}"
            
            results[purpose_name] = {
                'has_consent': consent is not None,
                'status': consent.status if consent else None,
                'last_updated': consent.updated_at.isoformat() if consent else None
            }
        
        return jsonify({
            'user_id': user_id,
            'consent_status': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 
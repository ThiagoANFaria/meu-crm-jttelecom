from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Call(db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'inbound' or 'outbound'
    duration = db.Column(db.Integer, nullable=True)  # in seconds
    status = db.Column(db.String(20), nullable=False)  # 'completed', 'missed', 'failed', 'in_progress'
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    recording_url = db.Column(db.String(255), nullable=True)
    external_call_id = db.Column(db.String(50), unique=True, nullable=True) # ID from PABX API
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'opportunity_id': self.opportunity_id,
            'user_id': self.user_id,
            'phone_number': self.phone_number,
            'direction': self.direction,
            'duration': self.duration,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'recording_url': self.recording_url,
            'external_call_id': self.external_call_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CallLog(db.Model):
    __tablename__ = 'call_logs'
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('calls.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # 'dialing', 'ringing', 'answered', 'hangup', 'error'
    event_data = db.Column(db.JSON, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    call = db.relationship('Call', backref=db.backref('logs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'call_id': self.call_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'timestamp': self.timestamp.isoformat()
        }


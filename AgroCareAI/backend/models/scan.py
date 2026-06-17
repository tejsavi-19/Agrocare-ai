from datetime import datetime
from database import db

class Scan(db.Model):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(50), nullable=False) # "Healthy" or "Diseased"
    confidence = db.Column(db.Float, nullable=False)
    disease_type = db.Column(db.String(100), nullable=True) # Future use
    risk_level = db.Column(db.String(50), nullable=True) # "Low", "Medium", "High"
    advice = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'image_path': self.image_path,
            'prediction': self.prediction,
            'confidence': self.confidence,
            'disease_type': self.disease_type,
            'risk_level': self.risk_level,
            'advice': self.advice,
            'timestamp': self.timestamp.isoformat()
        }

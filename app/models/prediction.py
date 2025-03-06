from app import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_type = db.Column(db.String(50), nullable=False)  # corn, rice, or tomato
    image_path = db.Column(db.String(256), nullable=False)
    disease = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('predictions', lazy=True))
    feedback = db.relationship('Feedback', backref='prediction', lazy=True, uselist=False) 
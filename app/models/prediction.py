from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON  # Add this import
class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_type = db.Column(db.String(50), nullable=False)  # corn, rice, or tomato
    image_path = db.Column(db.String(256), nullable=False)
    disease = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    recommendations = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship - Use 'back_populates' to avoid conflicts
    user = db.relationship('User', back_populates='predictions')
    feedbacks = db.relationship('Feedback', back_populates='prediction', lazy=True)  # One-to-Many

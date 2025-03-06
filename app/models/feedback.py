from app import db
from datetime import datetime

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    is_accurate = db.Column(db.Boolean)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    prediction = db.relationship('Prediction', backref=db.backref('feedback', lazy=True))
    user = db.relationship('User', backref=db.backref('feedback', lazy=True)) 
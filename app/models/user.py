from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='farmer')  # 'farmer' or 'admin'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # tempo token
    reset_code = db.Column(db.String(6), nullable=True)
    reset_code_expiration = db.Column(db.DateTime, nullable=True)

    # Relationship - Changed name from 'user_predictions' to 'predictions'
    predictions = db.relationship('Prediction', back_populates='user', lazy=True)
    feedbacks = db.relationship('Feedback', back_populates='user', lazy=True)  # One-to-Many

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_reset_code(self, code, expiry_time):
        self.reset_code = code
        self.reset_code_expiration = expiry_time
    def check_reset_code(self, code, current_time):
        return self.reset_code == code and self.reset_code_expiry and current_time <= self.reset_code_expir
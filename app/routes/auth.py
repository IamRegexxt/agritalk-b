from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_mail import Message
from datetime import datetime, timedelta
import random
import string
import os
import re
from app import db, mail
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

EMAIL_REGEX = r'^\S+@\S+\.\S+$'
PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'


# 6-digit random code generator
def generate_code():
    return ''.join(random.choices(string.digits, k=6))


# ------------------------------ REGISTER ------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Validate email & password format
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email format'}), 400
    if not re.match(PASSWORD_REGEX, password):
        return jsonify({
                           'error': 'Password must be at least 8 characters long and contain at least one letter and one number'}), 400

    # Check if email exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Create new user
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# ------------------------------ LOGIN ------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email format'}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'name': user.name,
            'role': user.role
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401


# ------------------------------ FORGOT PASSWORD ------------------------------
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email', '').strip()

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    reset_code = generate_code()
    expiry_time = datetime.utcnow() + timedelta(minutes=10)  # Code expires in 10 minutes

    # Store reset code in the User model
    user.set_reset_code(reset_code, expiry_time)
    db.session.commit()

    msg = Message(
        "AgriTuklas Password Reset Code",
        sender=os.getenv('MAIL_USERNAME'),
        recipients=[email]
    )
    msg.body = f"""
    Hello {user.name},

    We received a request to reset your password for your AgriTalk account. 

    🔢 **Your Reset Code:** {reset_code}  
    (This code will expire in 10 minutes.)

    If you did not request this reset, please ignore this email. Your account remains secure.

    🌱 Best Regards,  
    **AgriTalk Support Team**
    """

    try:
        mail.send(msg)
        return jsonify({'message': 'Password reset code sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500


# ------------------------------ RESET PASSWORD ------------------------------
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email', '').strip()
    reset_code = data.get('reset_code', '').strip()
    new_password = data.get('new_password', '').strip()

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Validate reset code and expiration time
    if not user.check_reset_code(reset_code, datetime.utcnow()):
        return jsonify({'error': 'Invalid or expired reset code'}), 400

    # Update new password
    user.set_password(new_password)
    user.reset_code = None
    user.reset_code_expiry = None
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200


# ------------------------------ LOG OUT ------------------------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

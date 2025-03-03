from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.feedback import Feedback
from app.models.prediction import Prediction
from app import db

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Validate input
    if not all(k in data for k in ('prediction_id', 'accuracy_rating')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    # Validate rating range
    if not 1 <= data['accuracy_rating'] <= 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
    # Check if prediction exists and belongs to user
    prediction = Prediction.query.get(data['prediction_id'])
    if not prediction:
        return jsonify({'error': 'Prediction not found'}), 404
        
    if prediction.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    # Check if feedback already exists
    existing_feedback = Feedback.query.filter_by(
        prediction_id=data['prediction_id'],
        user_id=user_id
    ).first()
    
    if existing_feedback:
        # Update existing feedback
        existing_feedback.accuracy_rating = data['accuracy_rating']
        existing_feedback.comments = data.get('comments', '')
        db.session.commit()
        return jsonify({'message': 'Feedback updated successfully'}), 200
    
    # Create new feedback
    feedback = Feedback(
        prediction_id=data['prediction_id'],
        user_id=user_id,
        accuracy_rating=data['accuracy_rating'],
        comments=data.get('comments', '')
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({'message': 'Feedback submitted successfully'}), 201

@feedback_bp.route('/feedback/<int:prediction_id>', methods=['GET'])
@jwt_required()
def get_feedback(prediction_id):
    user_id = get_jwt_identity()
    
    # Check if prediction exists and belongs to user
    prediction = Prediction.query.get_or_404(prediction_id)
    if prediction.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    # Get feedback
    feedback = Feedback.query.filter_by(
        prediction_id=prediction_id,
        user_id=user_id
    ).first()
    
    if not feedback:
        return jsonify({'error': 'No feedback found'}), 404
        
    return jsonify({
        'id': feedback.id,
        'prediction_id': feedback.prediction_id,
        'accuracy_rating': feedback.accuracy_rating,
        'comments': feedback.comments,
        'created_at': feedback.created_at.isoformat()
    }), 200 
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.prediction import Prediction
from app.models.feedback import Feedback
from sqlalchemy import desc

admin_bp = Blueprint('admin', __name__)


def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'


@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()

    # Check if user is admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Get all users
    users = User.query.all()

    user_list = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    } for user in users]

    return jsonify(user_list), 200


@admin_bp.route('/admin/recent-predictions', methods=['GET'])
@jwt_required()
def get_recent_predictions():
    user_id = get_jwt_identity()

    # Check if user is admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Get recent predictions
    predictions = Prediction.query.order_by(
        desc(Prediction.created_at)
    ).limit(20).all()

    prediction_list = [{
        'id': pred.id,
        'user_id': pred.user_id,
        'user_email': User.query.get(pred.user_id).email,
        'disease': pred.disease,
        'confidence': pred.confidence,
        'created_at': pred.created_at.isoformat()
    } for pred in predictions]

    return jsonify(prediction_list), 200


@admin_bp.route('/admin/recent-feedback', methods=['GET'])
@jwt_required()
def get_recent_feedback():
    user_id = get_jwt_identity()

    # Check if user is admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Get recent feedback
    feedback_items = Feedback.query.order_by(
        desc(Feedback.created_at)
    ).limit(20).all()

    feedback_list = [{
        'id': fb.id,
        'user_id': fb.user_id,
        'user_email': User.query.get(fb.user_id).email,
        'prediction_id': fb.prediction_id,
        'disease': Prediction.query.get(fb.prediction_id).disease,
        'rating': fb.accuracy_rating,
        'comments': fb.comments,
        'created_at': fb.created_at.isoformat()
    } for fb in feedback_items]

    return jsonify(feedback_list), 200

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.prediction import Prediction
from app.models.feedback import Feedback
from sqlalchemy import func
from app import db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'


@analytics_bp.route('/analytics/summary', methods=['GET'])
@jwt_required()
def get_analytics_summary():
    user_id = get_jwt_identity()

    # Check if user is admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Get total counts
    total_users = User.query.count()
    total_predictions = Prediction.query.count()
    total_feedback = Feedback.query.count()

    # Get average accuracy rating
    avg_rating = db.session.query(func.avg(Feedback.accuracy_rating)).scalar() or 0

    # Get disease distribution
    disease_counts = db.session.query(
        Prediction.disease,
        func.count(Prediction.id)
    ).filter(
        Prediction.disease != 'Processing'
    ).group_by(
        Prediction.disease
    ).all()

    disease_distribution = {disease: count for disease, count in disease_counts}

    # Get recent activity (last 7 days)
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    recent_predictions = Prediction.query.filter(
        Prediction.created_at >= one_week_ago
    ).count()

    return jsonify({
        'total_users': total_users,
        'total_predictions': total_predictions,
        'total_feedback': total_feedback,
        'average_rating': float(avg_rating),
        'disease_distribution': disease_distribution,
        'recent_predictions': recent_predictions
    }), 200


@analytics_bp.route('/analytics/predictions', methods=['GET'])
@jwt_required()
def get_prediction_analytics():
    user_id = get_jwt_identity()

    # Check if user is admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Get predictions by day (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    daily_predictions = db.session.query(
        func.date(Prediction.created_at),
        func.count(Prediction.id)
    ).filter(
        Prediction.created_at >= thirty_days_ago
    ).group_by(
        func.date(Prediction.created_at)
    ).all()

    # Format for response
    predictions_by_day = {
        date.strftime('%Y-%m-%d'): count
        for date, count in daily_predictions
    }

    # Get confidence score distribution
    confidence_ranges = [
        (0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)
    ]

    confidence_distribution = {}
    for low, high in confidence_ranges:
        count = Prediction.query.filter(
            Prediction.confidence >= low,
            Prediction.confidence < high
        ).count()
        confidence_distribution[f"{int(low * 100)}-{int(high * 100)}%"] = count

    return jsonify({
        'predictions_by_day': predictions_by_day,
        'confidence_distribution': confidence_distribution
    }), 200


@analytics_bp.route('/analytics/feedback', methods=['GET'])
@jwt_required()
def get_feedback_analytics():
    user_id = get_jwt_identity()

    # Check if user is admin
    if not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    # Get rating distribution
    rating_counts = db.session.query(
        Feedback.accuracy_rating,
        func.count(Feedback.id)
    ).group_by(
        Feedback.accuracy_rating
    ).all()

    rating_distribution = {f"{rating} stars": count for rating, count in rating_counts}

    # Get average rating by disease
    avg_by_disease = db.session.query(
        Prediction.disease,
        func.avg(Feedback.accuracy_rating)
    ).join(
        Feedback, Feedback.prediction_id == Prediction.id
    ).group_by(
        Prediction.disease
    ).all()

    rating_by_disease = {
        disease: float(avg_rating)
        for disease, avg_rating in avg_by_disease
    }

    return jsonify({
        'rating_distribution': rating_distribution,
        'rating_by_disease': rating_by_disease
    }), 200

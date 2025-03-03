from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc, func

from app.models.prediction import Prediction
from app.models.feedback import Feedback
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/history', methods=['GET'])
@jwt_required()
def get_user_history():
    user_id = get_jwt_identity()

    # Get user's predictions
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(desc(Prediction.created_at)).all()

    # Get feedback for each prediction
    history = []
    for prediction in predictions:
        feedback = Feedback.query.filter_by(prediction_id=prediction.id, user_id=user_id).first()

        history.append({
            'prediction_id': prediction.id,
            'image_url': prediction.image_path,
            'disease': prediction.disease,
            'confidence': prediction.confidence,
            'created_at': prediction.created_at.isoformat(),
            'feedback': {
                'rating': feedback.accuracy_rating,
                'comments': feedback.comments
            } if feedback else None
        })

    return jsonify(history), 200

@user_bp.route('/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    user_id = get_jwt_identity()

    # Get total predictions
    total_predictions = Prediction.query.filter_by(user_id=user_id).count()

    # Get disease distribution
    disease_counts = (
        Prediction.query
        .filter_by(user_id=user_id)
        .filter(Prediction.disease != 'Processing')
        .with_entities(Prediction.disease, func.count(Prediction.id))
        .group_by(Prediction.disease)
        .all()
    )
    disease_distribution = {disease: count for disease, count in disease_counts}

    # Get feedback stats
    total_feedback = Feedback.query.filter_by(user_id=user_id).count()
    avg_rating = db.session.query(func.avg(Feedback.accuracy_rating)).filter_by(user_id=user_id).scalar() or 0

    return jsonify({
        'total_predictions': total_predictions,
        'disease_distribution': disease_distribution,
        'total_feedback': total_feedback,
        'average_rating': float(avg_rating)
    }), 200

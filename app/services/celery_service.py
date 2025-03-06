from celery import Celery
from app import create_app, db
from app.models.prediction import Prediction
from app.services.ml_service import MLService
from app.services.recommendation_service import RecommendationService

celery = Celery('tasks', broker='redis://localhost:6379/0')
flask_app = create_app()
ml_service = MLService()
recommendation_service = RecommendationService()

@celery.task
def process_image(prediction_id):
    with flask_app.app_context():
        # Get prediction record
        prediction = Prediction.query.get(prediction_id)
        if not prediction:
            return
        
        # Get ML prediction
        result = ml_service.predict(
            prediction.image_path,
            prediction.crop_type
        )
        
        if result:
            # Update prediction record
            prediction.disease = result['disease']
            prediction.confidence = result['confidence']
            
            # Get recommendations
            recommendations = recommendation_service.get_recommendations(
                prediction.crop_type,
                prediction.disease
            )
            
            # Store recommendations (you might want to add a recommendations field to your Prediction model)
            prediction.recommendations = recommendations
            
            db.session.commit() 
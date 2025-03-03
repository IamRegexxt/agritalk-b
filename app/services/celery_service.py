from celery import Celery
from app import create_app, db
from app.models.prediction import Prediction
from app.services.ml_service import MLService

celery = Celery('tasks', broker='redis://localhost:6379/0')
flask_app = create_app()
ml_service = MLService()

@celery.task
def process_image(prediction_id):
    with flask_app.app_context():
        # Get prediction record
        prediction = Prediction.query.get(prediction_id)
        if not prediction:
            return
        
        # Get ML prediction
        result = ml_service.predict(prediction.image_path)
        if result:
            # Update prediction record
            prediction.disease = result['disease']
            prediction.confidence = result['confidence']
            db.session.commit() 
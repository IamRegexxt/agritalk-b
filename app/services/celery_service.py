from app.models.prediction import Prediction
from app.services.ml_service import MLService
from app.services.recommendation_service import RecommendationService
from app import db
from app.celery_app import create_celery

# Deferred initialization pattern
ml_service = MLService()
recommendation_service = RecommendationService()


class CeleryContext:
    def __init__(self):
        self.celery = None
        self.app = None

    def init_celery(self):
        from app import create_app  # Local import to break cycle
        self.app = create_app()
        self.celery = create_celery(self.app)
        return self.celery


celery_context = CeleryContext()
celery = celery_context.init_celery()


@celery.task(bind=True)
def process_image(self, prediction_id):
    with celery_context.app.app_context():
        prediction = Prediction.query.get(prediction_id)
        if not prediction:
            return "Prediction not found"

        result = ml_service.predict(prediction.image_path, prediction.crop_type)

        if result:
            prediction.disease = result['disease']
            prediction.confidence = result['confidence']

            if hasattr(prediction, 'recommendations'):
                recommendations = recommendation_service.get_recommendations(
                    prediction.crop_type, prediction.disease
                )
                prediction.recommendations = recommendations

            db.session.commit()
            return f"Prediction {prediction_id} processed successfully"

        return f"Prediction {prediction_id} processing failed"
from flask_migrate import Migrate
from app import create_app, db
from app.models.user import User
from app.models.prediction import Prediction
from app.models.feedback import Feedback

app = create_app()
migrate = Migrate(app, db)

# Import all models to ensure they're tracked by migrations
__all__ = ['User', 'Prediction', 'Feedback']

CROP_TYPES = ['corn', 'rice', 'tomato']

DISEASE_TYPES = {
    'corn': ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy'],
    'rice': ['leaf_blast', 'bacterial_leaf_blight', 'narrow_brown_spot', 'healthy', 'brown_spot', 'leaf_scald', 'Rice Hispa',
             'Neck_Blast', 'Sheath Blight', 'Tungro'],
    'tomato': ['Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']
}
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
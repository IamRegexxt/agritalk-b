from flask_migrate import Migrate
from app import create_app, db
from app.models.user import User
from app.models.prediction import Prediction
from app.models.feedback import Feedback

app = create_app()
migrate = Migrate(app, db)

# Import all models to ensure they're tracked by migrations
__all__ = ['User', 'Prediction', 'Feedback']

if __name__ == '__main__':
    with app.app_context():
        # Import all models here to ensure they're tracked by migrations
        pass
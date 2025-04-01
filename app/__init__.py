# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail


mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    from app.celery_app import create_celery
    create_celery(app)  # Initialize Celery with the app

    from app.routes.auth import auth_bp
    from app.routes.prediction import prediction_bp
    from app.routes.feedback import feedback_bp
    from app.routes.analytics import analytics_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    from app.routes.docs import docs_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(prediction_bp, url_prefix='/api/predict')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(docs_bp, url_prefix='/api/docs')

    return app
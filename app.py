from app import create_app, db
from app.models.user import User
from app.models.prediction import Prediction
from app.models.feedback import Feedback

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Prediction': Prediction,
        'Feedback': Feedback
    }


if __name__ == '__main__':
    app.run(debug=True)

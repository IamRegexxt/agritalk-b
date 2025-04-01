from app import create_app, db
from app.models.user import User


def init_db():
    app = create_app()

    with app.app_context():
        # Create tables
        db.create_all()

        # Check if admin user exists
        admin = User.query.filter_by(email='admin@agritalk.com').first()
        if not admin:
            # Create admin user
            admin = User(email='admin@agritalk.com', role='admin')
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        print("Database initialized successfully.")


if __name__ == '__main__':
    init_db()

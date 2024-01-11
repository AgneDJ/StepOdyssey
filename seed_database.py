from model import User,  connect_to_db, db
# from party import app


def create_test_user(user_name, user_email, user_password):
    """Create test/user into database."""

    user = User(user_name='user_name', user_email='user_email',
                user_password='user_password')

    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)

    with app.app_context():
        db.create_all()
        create_test_user()

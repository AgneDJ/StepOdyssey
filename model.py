"""Models for Step Odyssey app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user data."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User user_id={self.user_id} name={self.user_name} email={self.user_email} password={self.user_password}>"


class Friends(db.Model):
    """A user data."""

    __tablename__ = "friends"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    friend_id = db.Column(db.Integer, foreignkey=True)
    status_acceptance = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<User user_id={self.user_id} name={self.user_name} email={self.user_email} password={self.user_password}>"


def connect_to_db(flask_app, db_uri="postgresql:///step_challenge", echo=True):
    """Connects to database."""
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

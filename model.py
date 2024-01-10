"""Models for Step Odyssey app."""

from datetime import datetime
from flask import Flask
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
    """A friends data."""

    __tablename__ = "friends"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    friend_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    status_acceptance = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Friend user_id={self.user_id} friend_id={self.friend_id} status={self.status_acceptance}>"


class Steps(db.Model):
    """A steps data."""

    __tablename__ = "steps"

    steps_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    daily_total = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Steps steps_id={self.steps_id} user_id={self.user_id} daily_total={self.daily_total} date={self.date}>"


class ChatBox(db.Model):
    """A chat box data."""

    __tablename__ = "chat_box"

    chat_box_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __repr__(self):
        return f"<ChatBox user1={self.user1_id} user2={self.user2_id} chatbox={self.chat_box_id}>"


class Message(db.Model):
    """A message data."""

    __tablename__ = "message"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    chat_box_id = db.Column(db.Integer, db.ForeignKey("chat_box.chat_box_id"))
    date = db.Column(db.DateTime)
    message = db.Column(db.VARCHAR(256))
    sender = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __repr__(self):
        return f"<Message message_id={self.message_id} chat_box_id={self.chat_box_id_id} date={self.date} message={self.message} sender={self.sender}>"


class Achievements(db.Model):
    """Achievements data."""

    __tablename__ = "achievements"

    achievements_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    image = db.Column(db.String)
    condition = db.Column(db.Integer)
    title = db.Column(db.String)

    def __repr__(self):
        return f"<Achievements achievements_id={self.achievements_id} image={self.image} condition={self.condition} title={self.title}>"


class Challenges(db.Model):
    """A challenge data."""

    __tablename__ = "challenges"

    challenge_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    duration = db.Column(db.Integer)
    total_to_compete = db.Column(db.Integer)

    def __repr__(self):
        return f"<Challenges challenge_id={self.challenge_id} title={self.title} duration={self.duration} total_to_compete={self.total_to_compete}>"


class UserAchievements(db.Model):
    """A user/achievements data."""

    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    achievements_id = db.Column(
        db.Integer, db.ForeignKey("achievements.achievements_id"))
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<UserAchievements id={self.id} user_id={self.user_id} achievements_id={self.achievements_id} date={self.date}>"


class UserChallenges(db.Model):
    """A user/challenges data."""

    __tablename__ = "user_challenges"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.challenge_id"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return f"<UserChallenge id={self.id}  user_id={self.user_id} challenge_id={self.challenge_id}  start_time={self.star_time} end_time={self.end_time} complete={self.complete}>"


def connect_to_db(flask_app, db_uri="postgresql:///step_challenge", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)

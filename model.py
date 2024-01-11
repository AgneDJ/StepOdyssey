"""Models for Step Odyssey app."""

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user data."""

    __tablename__ = "user_data"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)

    # friends = db.relationship('Friends', back_populates="user")
    steps = db.relationship('Steps', back_populates="user")
    user_achievements = db.relationship(
        'UserAchievements', back_populates="user")
    user_challenges = db.relationship(
        'UserChallenges', back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} name={self.user_name} email={self.user_email} password={self.user_password}>"


class Friends(db.Model):
    """A friends data."""

    __tablename__ = "friends"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    friend_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    status_acceptance = db.Column(db.Boolean)

    # user = db.relationship('User', back_populates="friends")

    def __repr__(self):
        return f"<Friend user_id={self.user_id} friend_id={self.friend_id} status={self.status_acceptance}>"


class Steps(db.Model):
    """A steps data."""

    __tablename__ = "steps"

    steps_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    daily_total = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    user = db.relationship('User', back_populates="steps")

    def __repr__(self):
        return f"<Steps steps_id={self.steps_id} user_id={self.user_id} daily_total={self.daily_total} date={self.date}>"


class ChatBox(db.Model):
    """A chat box data."""

    __tablename__ = "chat_box"

    chat_box_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))

    messages = db.relationship('Message', back_populates="chat_box")

    def __repr__(self):
        return f"<ChatBox user1={self.user1_id} user2={self.user2_id} chatbox={self.chat_box_id}>"


class Message(db.Model):
    """A message data."""

    __tablename__ = "message"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    chat_box_id = db.Column(db.Integer, db.ForeignKey("chat_box.chat_box_id"))
    date = db.Column(db.DateTime)
    message = db.Column(db.VARCHAR(256))
    sender = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))

    chat_box = db.relationship('ChatBox', back_populates="messages")

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

    user_achievements = db.relationship(
        'UserAchievements', back_populates="achievements")

    def __repr__(self):
        return f"<Achievements achievements_id={self.achievements_id} image={self.image} condition={self.condition} title={self.title}>"


class Challenges(db.Model):
    """A challenge data."""

    __tablename__ = "challenges"

    challenge_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    duration = db.Column(db.Integer)
    total_to_compete = db.Column(db.Integer)

    user_challenges = db.relationship(
        'UserChallenges', back_populates="challenges")

    def __repr__(self):
        return f"<Challenges challenge_id={self.challenge_id} title={self.title} duration={self.duration} total_to_compete={self.total_to_compete}>"


class UserAchievements(db.Model):
    """A user/achievements data."""

    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    achievements_id = db.Column(
        db.Integer, db.ForeignKey("achievements.achievements_id"))
    date = db.Column(db.DateTime)

    user = db.relationship(
        'User', back_populates="user_achievements")
    achievements = db.relationship(
        'Achievements', back_populates="user_achievements")

    def __repr__(self):
        return f"<UserAchievements id={self.id} user_id={self.user_id} achievements_id={self.achievements_id} date={self.date}>"


class UserChallenges(db.Model):
    """A user/challenges data."""

    __tablename__ = "user_challenges"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.challenge_id"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    complete = db.Column(db.Boolean)

    user = db.relationship(
        'User', back_populates="user_challenges")
    challenges = db.relationship(
        'Challenges', back_populates="user_challenges")

    def __repr__(self):
        return f"<UserChallenge id={self.id}  user_id={self.user_id} challenge_id={self.challenge_id}  start_time={self.star_time} end_time={self.end_time} complete={self.complete}>"


def example_data():
    """Create some sample data."""

    User.query.delete()

    agne = User(user_name='Agne', user_email='fizikee@gmail.com',
                user_password='Asdf1234')
    bagne = User(user_name='Bagne', user_email='fizikea@gmail.com',
                 user_password='Asdf1235')
    cagne = User(user_name='Cagne', user_email='fizikeu@gmail.com',
                 user_password='Asdf1236')
    dagne = User(user_name='Dagne', user_email='fizikei@gmail.com',
                 user_password='Asdf1236')

    db.session.add_all([agne, bagne, cagne, dagne])
    db.session.commit()


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

    with app.app_context():
        db.create_all()
        example_data()

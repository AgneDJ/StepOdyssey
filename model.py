"""Models for Step Odyssey app."""

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets


db = SQLAlchemy()


class User(db.Model):
    """A user data."""

    __tablename__ = "user_data"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String)

    # friends = db.relationship('Friends', back_populates="user")
    steps = db.relationship('Steps', back_populates="user")
    user_achievements = db.relationship(
        'UserAchievements', back_populates="user")
    user_challenges = db.relationship(
        'UserChallenges', back_populates="user")

    def __repr__(self):
        return f"<{self.user_name}>"


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

    # steps_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    daily_total = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, primary_key=True)

    user = db.relationship('User', back_populates="steps")

    def __repr__(self):
        return f"<Steps {self.user.user_name},{self.date}, {self.daily_total}>"


class ChatBox(db.Model):
    """A chat box data."""

    __tablename__ = "chat_box"

    chat_box_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))

    messages = db.relationship('Message', back_populates="chat_box")

    def __repr__(self):
        return f"<ChatBox user1={self.user1_id} user2={self.user2_id} messages={self.messages}>"


class FriendRequest(db.Model):
    """Friend request data."""
    __tablename__ = "friend_request"

    sender = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)
    receiver = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)


class Message(db.Model):
    """A message data."""

    __tablename__ = "message"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    chat_box_id = db.Column(db.Integer, db.ForeignKey("chat_box.chat_box_id"))
    date = db.Column(db.DateTime)
    message = db.Column(db.Text)
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
        return f"<{self.id}, {self.user_id}, {self.challenge_id},  {self.start_time}, {self.end_time}, {self.complete}>"


def example_data():
    """Create some sample data."""

    Achievements.query.delete()
    ChatBox.query.delete()
    Steps.query.delete()
    FriendRequest()
    Friends.query.delete()
    User.query.delete()
    db.session.commit()
    gagne = User(user_name='gAgne', user_email='fizike@gmail.com',
                 user_password='Asdf1234')
    bagne = User(user_name='Bagne', user_email='fizikea@gmail.com',
                 user_password='Asdf1235')
    cagne = User(user_name='Cagne', user_email='fizikeu@gmail.com',
                 user_password='Asdf1236')
    dagne = User(user_name='Dagne', user_email='fizikei@gmail.com',
                 user_password='Asdf1236')

    db.session.add_all([gagne, bagne, cagne, dagne])
    db.session.commit()

    friend1 = Friends(user_id=gagne.user_id,
                      friend_id=bagne.user_id, status_acceptance=True)
    friend2 = Friends(user_id=bagne.user_id,
                      friend_id=cagne.user_id, status_acceptance=True)
    friend3 = Friends(user_id=cagne.user_id,
                      friend_id=dagne.user_id, status_acceptance=True)
    friend4 = Friends(user_id=dagne.user_id,
                      friend_id=gagne.user_id, status_acceptance=True)

    db.session.add_all([friend1, friend2, friend3, friend4])
    db.session.commit()

    steps1 = Steps(user_id=gagne.user_id, daily_total=15000, date="2024-1-1"
                   )
    steps2 = Steps(user_id=bagne.user_id, daily_total=15800, date="2024-1-3"
                   )
    steps3 = Steps(user_id=cagne.user_id, daily_total=12000, date="2024-1-2"
                   )
    steps4 = Steps(user_id=dagne.user_id, daily_total=15060, date="2024-1-5"
                   )

    db.session.add_all([steps1, steps2, steps3, steps4])
    db.session.commit()

    challenge1 = Challenges(title="Hit 5k", duration=24, total_to_compete=5000)
    challenge2 = Challenges(
        title="Hit 10k", duration=24, total_to_compete=10000)
    challenge3 = Challenges(
        title="Hit 20k", duration=24, total_to_compete=20000)
    challenge4 = Challenges(
        title="Hit 30k", duration=24, total_to_compete=30000)
    challenge5 = Challenges(
        title="Hit 40k", duration=24, total_to_compete=40000)
    challenge6 = Challenges(
        title="Hit 50k", duration=24, total_to_compete=50000)
    challenge7 = Challenges(
        title="Hit 60k", duration=24, total_to_compete=60000)
    challenge8 = Challenges(
        title="Hit 70k", duration=24, total_to_compete=70000)
    challenge9 = Challenges(
        title="Hit 80k", duration=24, total_to_compete=80000)
    challenge10 = Challenges(
        title="Hit 90k", duration=24, total_to_compete=90000)
    challenge11 = Challenges(
        title="Hit 100k", duration=24, total_to_compete=100000)

    db.session.add_all([challenge1, challenge2, challenge3, challenge4, challenge5,
                       challenge6, challenge7, challenge8, challenge9, challenge10, challenge11])

    chat_box1 = ChatBox(user1_id=gagne.user_id,
                        user2_id=bagne.user_id,)
    chat_box2 = ChatBox(user1_id=bagne.user_id,
                        user2_id=cagne.user_id)
    chat_box3 = ChatBox(user1_id=cagne.user_id,
                        user2_id=dagne.user_id)
    chat_box4 = ChatBox(user1_id=dagne.user_id,
                        user2_id=gagne.user_id)

    db.session.add_all([chat_box1, chat_box2, chat_box3, chat_box4])
    db.session.commit()

    achievements1 = Achievements(
        image="/static/img/10k_achievement.jpeg", condition=10000, title="10k Nice! You are alive!!")

    achievements2 = Achievements(
        image="/static/img/10k_achievement.jpeg", condition=100000, title="100k Hooray!!")
    achievements3 = Achievements(image="/static/img/10k_achievement.jpeg",
                                 condition=200000, title="20k Where Are You Heading?!")
    achievements4 = Achievements(image="/static/img/10k_achievement.jpeg", condition=300000, title="300k Half way to Moon"
                                 )
    achievements5 = Achievements(image="/static/img/10k_achievement.jpeg", condition=400000, title="400k Now thats what I'm talking about!"
                                 )
    achievements6 = Achievements(image="/static/img/10k_achievement.jpeg", condition=500000, title="500k ..."
                                 )
    achievements7 = Achievements(image="/static/img/10k_achievement.jpeg", condition=600000, title="600k ,.,"
                                 )
    achievements8 = Achievements(image="/static/img/10k_achievement.jpeg", condition=700000, title="700k woooooow"
                                 )
    achievements9 = Achievements(
        image="/static/img/10k_achievement.jpeg", condition=800000, title="800k gosh!")

    achievements10 = Achievements(
        image="/static/img/10k_achievement.jpeg", condition=900000, title="900k you are doing it!!!!")

    achievements11 = Achievements(
        image="/static/img/10k_achievement.jpeg", condition=1000000, title="The Impossible!")

    db.session.add_all([achievements1, achievements2, achievements3, achievements4, achievements5,
                       achievements6, achievements7, achievements8, achievements9, achievements10, achievements11])
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
        # example_data()

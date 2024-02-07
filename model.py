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
    user_password = db.Column(db.String)
    user_avatar = db.Column(db.String)
    refresh_token = db.Column(db.String)

    # friends = db.relationship('Friends', back_populates="user")
    steps = db.relationship('Steps', back_populates="user")
    user_achievements = db.relationship(
        'UserAchievements', back_populates="user")
    user_challenges = db.relationship(
        'UserChallenges', back_populates="user")

    def __repr__(self):
        return f"{self.user_name}"


class UserMessage(db.Model):
    """User messages."""

    __tablename__ = "user_message"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
    message = db.Column(db.String)


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
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)
    daily_total = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, primary_key=True)

    user = db.relationship('User', back_populates="steps")

    def __repr__(self):
        return f"<Steps {self.user.user_name},{self.date}, {self.daily_total}>"


# class ChatBox(db.Model):
#     """A chat box data."""

#     __tablename__ = "chat_box"

#     chat_box_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user1_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))
#     user2_id = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))

#     messages = db.relationship('Message', back_populates="chat_box")

#     def __repr__(self):
#         return f"<ChatBox user1={self.user1_id} user2={self.user2_id} messages={self.messages}>"


class FriendRequest(db.Model):
    """Friend request data."""
    __tablename__ = "friend_request"

    sender = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)
    receiver = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)


class ChallengeRequest(db.Model):
    """Challenge request data."""
    __tablename__ = "challenge_request"

    receiver = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey(
        "user_data.user_id"), primary_key=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.challenge_id"))


# class Message(db.Model):
#     """A message data."""

#     __tablename__ = "message"

#     message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     chat_box_id = db.Column(db.Integer, db.ForeignKey("chat_box.chat_box_id"))
#     date = db.Column(db.DateTime)
#     message = db.Column(db.Text)
#     sender = db.Column(db.Integer, db.ForeignKey("user_data.user_id"))

#     chat_box = db.relationship('ChatBox', back_populates="messages")

#     def __repr__(self):
#         return f"<Message message_id={self.message_id} chat_box_id={self.chat_box_id_id} date={self.date} message={self.message} sender={self.sender}>"


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
    # ChatBox.query.delete()
    Steps.query.delete()
    FriendRequest()
    Friends.query.delete()
    User.query.delete()
    db.session.commit()

    agne = User(user_name='Agne', user_email='fizikee@gmail.com')
    peter = User(user_name='Peter', user_email='peter@gmail.com')
    carl = User(user_name='Carl', user_email='carl@gmail.com')
    alma = User(user_name='Alma', user_email='alma@gmail.com')
    rachel = User(user_name='Rachel', user_email='rachel@gmail.com')
    jennifer = User(user_name='Jennifer', user_email='jenni@gmail.com')
    sean = User(user_name='Sean', user_email='sean@gmail.com')
    zoe = User(user_name='Zoe', user_email='zoe@gmail.com')
    silvia = User(user_name='Silvia', user_email='silvi_a@gmail.com')

    db.session.add_all([agne, carl, peter, alma, rachel,
                       jennifer, sean, zoe, silvia])
    db.session.commit()

    friend1 = Friends(user_id=peter.user_id,
                      friend_id=carl.user_id, status_acceptance=True)
    friend2 = Friends(user_id=carl.user_id,
                      friend_id=peter.user_id, status_acceptance=True)
    friend3 = Friends(user_id=agne.user_id,
                      friend_id=peter.user_id, status_acceptance=True)
    friend4 = Friends(user_id=carl.user_id,
                      friend_id=agne.user_id, status_acceptance=True)
    friend5 = Friends(user_id=alma.user_id,
                      friend_id=agne.user_id, status_acceptance=True)
    friend6 = Friends(user_id=rachel.user_id,
                      friend_id=agne.user_id, status_acceptance=True)
    friend7 = Friends(user_id=jennifer.user_id,
                      friend_id=agne.user_id, status_acceptance=True)
    friend8 = Friends(user_id=sean.user_id,
                      friend_id=agne.user_id, status_acceptance=True)
    friend9 = Friends(user_id=zoe.user_id,
                      friend_id=agne.user_id, status_acceptance=True)
    friend10 = Friends(user_id=silvia.user_id,
                       friend_id=agne.user_id, status_acceptance=True)

    db.session.add_all([friend1, friend2, friend3, friend4,
                       friend5, friend6, friend7, friend8, friend9, friend10])
    db.session.commit()

    challenge1 = Challenges(
        title="Stride and Thrive: The 5,000 Step Daily Challenge", duration=24, total_to_compete=5000)
    challenge2 = Challenges(
        title="March to Wellness: The 10,000 Steps Challenge", duration=24, total_to_compete=10000)
    challenge3 = Challenges(
        title="March to Mastery: The 20,000 Steps Challenge", duration=24, total_to_compete=20000)
    challenge4 = Challenges(
        title="March to Triumph: The 30,000 Steps Challenge", duration=24, total_to_compete=30000)
    challenge5 = Challenges(
        title="March to Victory: The 40,000 Steps Challenge", duration=24, total_to_compete=40000)
    challenge6 = Challenges(
        title="March to Glory: The 50,000 Steps Challenge", duration=24, total_to_compete=50000)
    challenge7 = Challenges(
        title="March to Legend: The 60,000 Steps Challenge", duration=24, total_to_compete=60000)
    challenge8 = Challenges(
        title="March to Infinity: The 70,000 Steps Challenge", duration=24, total_to_compete=70000)
    challenge9 = Challenges(
        title="March to the Beyond: The 80,000 Steps Challenge", duration=24, total_to_compete=80000)
    challenge10 = Challenges(
        title="March to the Summit: The 90,000 Steps Challenge", duration=24, total_to_compete=90000)
    challenge11 = Challenges(
        title="March to the Apex: The 100,000 Steps Challenge", duration=24, total_to_compete=100000)
    challenge12 = Challenges(
        title="Odyssey Sprint: The 20,000 Step 2-Day Challenge", duration=48, total_to_compete=20000)
    challenge13 = Challenges(
        title="Odyssey Trek: The 30,000 Step 2-Day Marathon", duration=48, total_to_compete=30000)
    challenge14 = Challenges(
        title="Odyssey Voyage: The 40,000 Step 2-Day Quest", duration=48, total_to_compete=40000)
    challenge15 = Challenges(
        title="Odyssey Expedition: The 50,000 Step 2-Day Quest", duration=48, total_to_compete=50000)
    challenge16 = Challenges(
        title="Odyssey: The 100,000 Step 7-Day Epic", duration=168, total_to_compete=100000)

    db.session.add_all([challenge1, challenge2, challenge3, challenge4, challenge5,
                       challenge6, challenge7, challenge8, challenge9, challenge10, challenge11, challenge12, challenge13, challenge14, challenge15, challenge16])
    db.session.commit()

    user_challenge1 = UserChallenges(
        user_id=1, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge2 = UserChallenges(
        user_id=2, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge3 = UserChallenges(
        user_id=3, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge4 = UserChallenges(
        user_id=4, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge5 = UserChallenges(
        user_id=5, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge6 = UserChallenges(
        user_id=6, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge7 = UserChallenges(
        user_id=7, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge8 = UserChallenges(
        user_id=8, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)
    user_challenge9 = UserChallenges(
        user_id=9, challenge_id=1, start_time=2024-2-6, end_time=2024-2-7, complete=False)

    db.session.add_all([user_challenge1, user_challenge2, user_challenge3, user_challenge4, user_challenge5,
                       user_challenge6, user_challenge7, user_challenge8, user_challenge9, ])
    db.session.commit()

    achievements1 = Achievements(
        image="/static/img/10k_achievement.jpeg", condition=10000, title="Odyssey Conqueror: The 10,000 Step Milestone")

    achievements2 = Achievements(
        image="/static/img/100k_achievement.jpeg", condition=100000, title="Odyssey Legend: The 100,000 Step Epic Journey")
    achievements3 = Achievements(image="/static/img/200k_achievement.jpeg",
                                 condition=200000, title="Odyssey Titan: The 200,000 Step Odyssey Triumph")
    achievements4 = Achievements(image="/static/img/300k_achievement.jpeg", condition=300000, title="Odyssey Immortal: The 300,000 Step Odyssey Masterpiece"
                                 )
    achievements5 = Achievements(image="/static/img/400k_achievement.jpeg", condition=400000, title="Odyssey Sovereign: The 400,000 Step Supreme Expedition"
                                 )
    achievements6 = Achievements(image="/static/img/500k_achievement.jpeg", condition=500000, title="Odyssey Monarch: The 500,000 Step Ultimate Quest"
                                 )
    achievements7 = Achievements(image="/static/img/600k_achievement.jpeg", condition=600000, title="Odyssey Deity: The 600,000 Step Grand Odyssey"
                                 )
    achievements8 = Achievements(image="/static/img/700k_achievement.jpeg", condition=700000, title="Odyssey Cosmos: The 700,000 Step Galactic Journey"
                                 )
    achievements9 = Achievements(
        image="/static/img/800k_achievement.jpeg", condition=800000, title="Odyssey Infinite: The 800,000 Step Endless Voyage")

    achievements10 = Achievements(
        image="/static/img/900k_achievement.jpeg", condition=900000, title="Odyssey Eternal: The 900,000 Step Timeless Trek")

    achievements11 = Achievements(
        image="/static/img/1000k_achievement.jpeg", condition=1000000, title="Odyssey Mythic: The 1,000,000 Step Legendary Odyssey")

    db.session.add_all([achievements1, achievements2, achievements3, achievements4, achievements5,
                       achievements6, achievements7, achievements8, achievements9, achievements10, achievements11])
    db.session.commit()

    challenge_request1 = ChallengeRequest(
        receiver=agne.user_id, sender=peter.user_id, challenge_id=1)
    challenge_request2 = ChallengeRequest(
        receiver=agne.user_id, sender=carl.user_id, challenge_id=1)
    challenge_request3 = ChallengeRequest(
        receiver=agne.user_id, sender=alma.user_id, challenge_id=1)
    challenge_request4 = ChallengeRequest(
        receiver=agne.user_id, sender=silvia.user_id, challenge_id=1)
    challenge_request5 = ChallengeRequest(
        receiver=agne.user_id, sender=zoe.user_id, challenge_id=1)
    challenge_request6 = ChallengeRequest(
        receiver=agne.user_id, sender=jennifer.user_id, challenge_id=1)
    challenge_request7 = ChallengeRequest(
        receiver=agne.user_id, sender=sean.user_id, challenge_id=1)
    challenge_request8 = ChallengeRequest(
        receiver=agne.user_id, sender=rachel.user_id, challenge_id=1)

    db.session.add_all([challenge_request1, challenge_request2, challenge_request3, challenge_request4,
                       challenge_request5, challenge_request6, challenge_request7, challenge_request8])
    db.session.commit()

    steps1 = Steps(user_id=peter.user_id, daily_total=1930, date="2024-2-6"
                   )
    steps2 = Steps(user_id=agne.user_id, daily_total=13965, date="2024-2-6"
                   )
    steps3 = Steps(user_id=carl.user_id, daily_total=1682, date="2024-2-6"
                   )
    steps4 = Steps(user_id=alma.user_id, daily_total=10328, date="2024-2-6"
                   )
    steps5 = Steps(user_id=jennifer.user_id, daily_total=40392, date="2024-2-6"
                   )
    steps6 = Steps(user_id=silvia.user_id, daily_total=254, date="2024-2-6"
                   )
    steps7 = Steps(user_id=zoe.user_id, daily_total=200, date="2024-2-6"
                   )
    steps8 = Steps(user_id=rachel.user_id, daily_total=2, date="2024-2-6"
                   )
    steps9 = Steps(user_id=sean.user_id, daily_total=2712, date="2024-2-6"
                   )

    db.session.add_all([steps1, steps2, steps3, steps4,
                       steps5, steps6, steps7, steps8, steps9])
    db.session.commit()

    # chat_box1 = ChatBox(user1_id=gagne.user_id,
    #                     user2_id=bagne.user_id,)
    # chat_box2 = ChatBox(user1_id=bagne.user_id,
    #                     user2_id=cagne.user_id)
    # chat_box3 = ChatBox(user1_id=cagne.user_id,
    #                     user2_id=dagne.user_id)
    # chat_box4 = ChatBox(user1_id=dagne.user_id,
    #                     user2_id=gagne.user_id)

    # db.session.add_all([chat_box1, chat_box2, chat_box3, chat_box4])
    # db.session.commit()


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

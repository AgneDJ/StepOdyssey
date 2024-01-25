"""CRUD operations."""

from model import db, User, Friends, Steps, ChatBox, Challenges, Achievements, UserChallenges, UserAchievements, Message, FriendRequest, connect_to_db
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
import os
from datetime import date


def create_user(name, email, password):
    """Create and return a new user."""

    user = User(user_name=name, user_email=email,
                user_password=password, refresh_token="")

    return user


def create_steps(user_id, daily_total, date):
    return Steps(user_id=user_id, daily_total=daily_total,
                 date=date)


def get_users():
    """Return all users."""
    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.user_email == email).first()


def get_user_by_password(password):
    """Return a user by password."""

    return User.query.filter(User.password == password).first()


def get_challenges():
    """Return all challenges by title."""

    challenges = Challenges.query.all()

    return challenges


def get_challenge_by_id(challenge_id):
    challenge = Challenges.query.get(challenge_id)
    return challenge


def get_achievements():
    """Return all achievements by title."""

    achievements = Achievements.query.all()
    return achievements


def add_data_to_user_challenges(user_id, challenge_id, start_time, end_time, complete):
    """Adds challenge data to db"""
    user_challenges = UserChallenges(user_id=user_id, challenge_id=challenge_id,
                                     start_time=start_time, end_time=end_time, complete=complete)

    return user_challenges


def lifetime_steps(user_id):
    """Returns total steps."""

    user_lifetime_steps = db.session.query(
        func.sum(Steps.daily_total)).filter(Steps.user_id == user_id).first()[0]
    return user_lifetime_steps


def create_friend_req(sender, receiver):
    """Create a friend request."""
    req = FriendRequest(sender=sender, receiver=receiver)
    db.session.add(req)
    db.session.commit()
    return req


def delete_friend_req(sender, receiver):
    """Delete a friend request."""
    request = FriendRequest.query.filter(
        FriendRequest.sender == sender, FriendRequest.receiver == receiver).first()
    if len(request) > 0:
        db.session.delete(request[0])


def make_friend(sender, receiver):
    """Add friend."""
    request = FriendRequest.query.filter(
        FriendRequest.sender == sender, FriendRequest.receiver == receiver).first()
    if len(request) == 0:
        return
    create_friendship = Friends(sender, receiver, True)
    db.session.delete(request[0])


def lose_friend(sender, receiver):
    """Remove friend."""
    destroy_friendship = Friends.query.filter(
        Friends.user_id == sender, Friends.friend_id == receiver).first()[0]
    db.session.delete(destroy_friendship)

    return create_friendship


def get_friend_req(sender, receiver):
    """Get friend requests."""
    request = FriendRequest.query.filter(
        FriendRequest.sender == sender, FriendRequest.receiver == receiver).first()

    return request


def get_friend_rec(receiver):
    request = FriendRequest.query.filter(
        FriendRequest.receiver == receiver).all()

    return request

# achievements--------------------------
# def add_user_achievements(user_id, achievement_id, date, image):
#     """Adds achievements data to db"""
#     user_achievements = UserAchievements(user_id=user_id, achievement_id=achievement_id,
#                                          date=date, image=image)

#     return user_achievements


def get_leader():
    """Return most active users."""

    today = date.today()
    query = Steps.query.filter(Steps.date == today).order_by(
        Steps.daily_total.desc()).limit(10).all()

    # hmmmmmm NEED USER NAME

    return query

# if __name__ == "__main__":
#     from server import app

#     connect_to_db(app)

"""CRUD operations."""

from model import db, User, Friends, Steps, ChatBox, Challenges, Achievements, UserChallenges, UserAchievements, Message, connect_to_db
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


def get_user_achievements():
    """Return user achievements by title."""
    user_achievements = [
        user_achievements.title for user_achievements in UserAchievements.query.all()]
    return user_achievements


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

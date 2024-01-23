"""CRUD operations."""

from model import db, User, Friends, Steps, ChatBox, Challenges, Achievements, UserChallenges, UserAchievements, Message, connect_to_db
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
import os


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
    print(User.query.all())
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

    challenges = [challenges.title for challenges in Challenges.query.all()]

    return challenges


def get_achievements():
    """Return all achievements by title."""

    achievements = [
        achievements.title for achievements in Achievements.query.all()]
    return achievements


def get_user_challenges():
    """Return user challenges by title."""
    user_challenges = [
        user_challenges.title for user_challenges in UserChallenges.query.all()]
    return user_challenges


def get_user_achievements():
    """Return user achievements by title."""
    user_achievements = [
        user_achievements.title for user_achievements in UserAchievements.query.all()]
    return user_achievements


def get_leader():
    """Return most active users."""

   # leader = User.query.filter(User.user_name, count(Steps.daily_total).join(Steps.daily_total, User.user_name ==
    query = db.session.query(User.user_name, func.count(Steps.daily_total).label('daily_total')).join(
        Steps.daily_total, User.user_name == Steps.daily_total).group_by(User.user_name).order_by(func.count(Steps.daily_total).desc()).limit(10)
    return print(query)
# if __name__ == "__main__":
#     from server import app

#     connect_to_db(app)

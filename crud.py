"""CRUD operations."""

from model import db, User, Friends, Steps, Challenges, Achievements, UserChallenges, UserAchievements, FriendRequest, connect_to_db
from sqlalchemy import insert, or_, and_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
import os
from datetime import date


def create_user(name, email, token):
    """Create and return a new user."""

    user = User(user_name=name, user_email=email,
                refresh_token="", user_password="", user_avatar="")

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


def get_users_by_ids(ids):
    """Return a users by primary key."""

    return User.query.filter(User.user_id.in_(ids)).all()


def get_friends(receiver):

    friend_list = Friends.query.filter(or_(Friends.friend_id == receiver,
                                           Friends.user_id == receiver)).all()
    user_ids = []
    for friend in friend_list:
        user_ids.append(friend.friend_id)
        user_ids.append(friend.user_id)

    user_ids = set(user_ids)
    if len(user_ids) > 0:
        user_ids.remove(receiver)

    return user_ids


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


def get_user_achievements(user_id):
    """Return all user achievements by title."""

    user_achievements = UserAchievements.query.filter(
        UserAchievements.user_id == user_id).all()

    return user_achievements

# do I need a commit?


def add_data_to_user_challenges(user_id, challenge_id, start_time, end_time, complete):
    """Adds challenge data to db"""
    user_challenges = UserChallenges(user_id=user_id, challenge_id=challenge_id,
                                     start_time=start_time, end_time=end_time, complete=complete)
    db.session.add(user_challenges)
    db.session.commit()
    return user_challenges

# do I need a commit?


# def add_data_to_user_achievements(user_id, achievements_id, date):
#     """Adds achievements to personal db"""
#     user_achievements = UserAchievements(user_id=user_id, achievements_id=achievements_id,
#                                          date=date)
#     db.session.add(user_achievements)
#     db.session.commit()

#     return user_achievements


def get_achievement_img(achievement_id):
    """Gets achievements image url by achievement id"""
    achievement_image = db.session.query(
        Achievements.image).filter(achievement_id).first()

    return achievement_image


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


def create_user_achievements(achievements_id, user_id, date):
    if (UserAchievements.query.filter(UserAchievements.achievements_id == achievements_id, UserAchievements.user_id == user_id).first()):
        return
    usr_achvm = UserAchievements(
        achievements_id=achievements_id, user_id=user_id, date=date)
    db.session.add(usr_achvm)
    db.session.commit()
    return usr_achvm


def delete_friend_req(sender, receiver):
    """Delete a friend request."""
    request = FriendRequest.query.filter(
        FriendRequest.sender == sender, FriendRequest.receiver == receiver).first()
    if request:
        db.session.delete(request)
        db.session.commit()


def make_friend(sender, receiver):
    """Add friend."""
    request = FriendRequest.query.filter(
        FriendRequest.sender == sender, FriendRequest.receiver == receiver).first()
    if not request:
        return

    relation = Friends(user_id=sender,
                       friend_id=receiver, status_acceptance=True)
    print("===========================================")
    print(relation)
    db.session.add(relation)
    db.session.delete(request)
    db.session.commit()
    print("visogeeeeeero")


def lose_friend(sender, receiver):
    """Remove friend."""
    destroy_friendship = Friends.query.filter(
        or_(
            and_(Friends.friend_id == receiver, Friends.user_id == sender),
            and_(Friends.friend_id == sender, Friends.user_id == receiver)
        )).all()
    for friends in destroy_friendship:
        print(friends)
        db.session.delete(friends)
    db.session.commit()

    return destroy_friendship


def get_friend_req(sender, receiver):
    """Get friend requests."""
    request = FriendRequest.query.filter(
        FriendRequest.sender == sender, FriendRequest.receiver == receiver).first()

    return request


def is_there_friend_request(receiver):
    """Return boolean if there are any friend requests."""

    requests = get_friend_rec(receiver)
    return len(requests) > 0


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

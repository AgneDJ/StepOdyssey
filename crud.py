"""CRUD operations."""

from model import db, User, Friends, Steps, Challenges, Achievements, UserChallenges, UserAchievements, FriendRequest, ChallengeRequest, UserMessage, connect_to_db
from sqlalchemy import insert, or_, and_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
import os
from datetime import date, datetime


def create_user(name, email, token):
    """Create and return a new user."""

    user = User(user_name=name, user_email=email,
                refresh_token="", user_password="", user_avatar="")

    return user


def post_message(sender, message):
    """Adding message to db."""

    adding_message = UserMessage(user_id=sender, message=message)

    db.session.add(adding_message)
    db.session.commit()


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


def get_user_challenges(user_id):
    """Return all user_challenges."""

    now = datetime.now()
    return UserChallenges.query.filter(UserChallenges.end_time >= now, UserChallenges.user_id == user_id).all()


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


def invite_to_challenge(sender, receiver, challenge_id):
    """Invite friend to a challenge."""

    challenge_invitation = ChallengeRequest(
        sender=sender, receiver=receiver, challenge_id=challenge_id)
    db.session.merge(challenge_invitation)
    db.session.commit()


def challenge_invites(user_id):
    """Return all invites to a challenges."""

    return ChallengeRequest.query.filter(
        ChallengeRequest.receiver == user_id).all()


def delete_all_challenge_invites(receiver, challenge_id):
    """Delete all invitations for challenge"""

    challenge_invitation = ChallengeRequest.query.filter(
        ChallengeRequest.receiver == receiver, ChallengeRequest.challenge_id == challenge_id).all()
    for invite in challenge_invitation:
        db.session.delete(invite)
    db.session.commit()


def has_invites(user_id):
    """Return boolean if there are any invites."""

    invites = ChallengeRequest.query.filter(
        ChallengeRequest.receiver == user_id).first()
    return invites is not None


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


def if_joined(user_id, challenge_id):
    joined = UserChallenges.query.filter(UserChallenges.user_id == user_id,
                                         UserChallenges.challenge_id == challenge_id, UserChallenges.end_time >= datetime.now()).first()
    return joined is not None


def get_users_challenges(friends_list, challenge_id):
    user_challenges = []
    for friend in friends_list:
        user_challenge = UserChallenges.query.filter(UserChallenges.user_id == friend.user_id,
                                                     UserChallenges.challenge_id == challenge_id, UserChallenges.end_time >= datetime.now()).first()
        if user_challenge is not None:
            user_challenges.append(user_challenge)

    return user_challenges


def get_steps_by_date(user_id, date):
    steps_by_date = Steps.query.filter(
        Steps.user_id == user_id, Steps.date == datetime.date(date)).first()
    if steps_by_date is None:
        return 0
    return steps_by_date.daily_total


def get_steps_by_user_id(user_id):
    steps_by_user = Steps.query.filter(
        Steps.user_id == user_id).first()

    return steps_by_user


def get_leader():
    """Return most active users."""

    today = date.today()
    query = Steps.query.filter(Steps.date == today).order_by(
        Steps.daily_total.desc()).limit(10).all()

    # all_users = User.query.filter(Steps.date == datetime.now()).order_by(
    #     Steps.daily_total.desc()).limit(10).all()
    return query

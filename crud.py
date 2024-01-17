"""CRUD operations."""

from model import db, User, Friends, Steps, ChatBox, Challenges, Achievements, UserChallenges, UserAchievements, Message, connect_to_db
import os
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import googleapiclient.discovery


def create_user(name, email, password):
    """Create and return a new user."""

    user = User(user_name=name, user_email=email, user_password=password)

    return user


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
# google rest api


# def recor_steps():
#     OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
#     APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")

#     import requests
#     url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

#     headers = {'content-type': 'application/json',
#                'Authorization': 'Bearer %s' % OAUTH_TOKEN}
#     r = requests.get(url, headers=headers)

#     # Fitness.getRecordingClient(this, GoogleSignIn.getAccountForExtension(this, fitnessOptions))
#     #     .subscribe(DataType.TYPE_STEP_COUNT_CUMULATIVE)
#     #     .addOnSuccessListener {
#     #         Log.i(TAG,"Subscription was successful!")
#     #     }
#     #     .addOnFailureListener { e ->
#     #         Log.w(TAG, "There was a problem subscribing ", e)
#     #    }
#     print(r.status_code)
#     print(r.content)

#     # def total_daily():
#     #          url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

#     #     headers = { 'content-type': 'application/json',
#     #                 'Authorization': 'Bearer %s' % OAUTH_TOKEN }
#     # #     r = requests.get(url, headers=headers)


#     #             {
# recor_steps()

# if __name__ == "__main__":
#     from server import app

#     connect_to_db(app)

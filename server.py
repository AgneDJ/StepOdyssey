"""Server for step_odyssey app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json
import crud
from datetime import time, date, datetime, timedelta
import humanize
import datetime as dt


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY", None)
app.jinja_env.undefined = StrictUndefined

# TODO: crash i
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/")
def homepage():
    """View homepage."""
    if "user_email" in session:
        return redirect("/profile")
    return render_template("homepage.html")


@app.route('/profile')
def rendering_profile():
    """User profile."""
    if "user_email" not in session:
        return redirect("/")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
# checking if user exists
    if not user:
        del session["user_email"]
        return redirect("/")

    daily_total = crud.get_steps_by_date(
        user.user_id, datetime.now())

    now = datetime.now()
    print("     ---------THIS IS START")
    daystart = datetime(year=now.year, month=now.month,
                        day=now.day)
    daynext = datetime(year=now.year, month=now.month,
                       day=now.day+1)
    print(" -----------THIS IS END")
    print(daystart)

    friends = crud.get_friends(user.user_id)
    friends_list = crud.get_users_by_ids(friends)

    user_challenges = []
    challenges = crud.get_challenges()
    print('ppppppppppppppppppp')
    complete = "In progress"
    status_of_challenge = "None"
    for challenge in user.user_challenges:
        # get steps from day of end_time instead of daily total
        steps = crud.get_steps_by_date(user.user_id, challenge.start_time)
        end = challenge.end_time
        challenge_date = datetime(year=end.year, month=end.month,
                                  day=end.day)
        duration = now-challenge.end_time
        progress = challenge.challenges.total_to_compete-steps

        if challenge_date <= daystart and progress > 0:
            complete = "You lost..."
            status_of_challenge = "Over"

        elif challenge_date <= daystart and progress < 0:
            complete = "Hurray! You made it!"
            status_of_challenge = "Over"

        else:
            complete = "Getting there"
            status_of_challenge = "In progress"

        friends_challenges = crud.get_users_challenges(
            friends_list, challenge.challenge_id)
        friends_state = []
        for challenge in friends_challenges:
            steps = crud.get_steps_by_date(
                challenge.user_id, datetime.now())
            friends_state.append({
                'friend': challenge.user,
                'steps': steps
            })

        user_challenges.append({
            'user_challenge': challenge,
            'duration': humanize.naturaltime(duration),
            'status': status_of_challenge,
            'progress': steps,
            'complete': complete,
            'friends': friends_state,
        })
    user_challenges.reverse()

    # achievement adding process
    lifetime_steps = crud.lifetime_steps(user.user_id)
    # lifetime_steps = 1000000
    all_achievements = crud.get_achievements()
    user_achievements = crud.get_user_achievements(user.user_id)

    achievement_image = None

    if all_achievements is not None:
        for achievement in all_achievements:
            if achievement.condition <= lifetime_steps:
                crud.create_user_achievements(
                    achievement.achievements_id, user.user_id, now)
                # UserAchievements.achievements_id = achievement.achievements_id,
                # UserAchievements.user_id = user.user_id
                # UserAchievements.date = now
                achievement_image = achievement.image
                # crud.add_data_to_user_achievements(
                #     user.user_id, achievement.achievements_id, now)

    has_friend_requests = crud.is_there_friend_request(receiver=user.user_id)

    user_achievements = crud.get_user_achievements(user.user_id)
    print("------------")

    has_invites = crud.has_invites(user.user_id)

    return render_template("profile.html",
                           has_friend_requests=has_friend_requests,
                           has_invites=has_invites,
                           user=user,
                           date=datetime.date(now),
                           daily_total=daily_total,
                           user_achievements=user_achievements,
                           achievement_image=achievement_image,
                           user_challenges=user_challenges,
                           lifetime_steps=lifetime_steps,
                           friends_list=friends_list)


@app.route("/login/google")
def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.host_url + "login/oauth",
        scope=["openid", "email", "https://www.googleapis.com/auth/userinfo.profile",
               "https://www.googleapis.com/auth/fitness.activity.read"],
        access_type="offline",
        include_granted_scopes="true",
    )
    print(request_uri)
    return redirect(request_uri)


@app.route("/login/oauth")
def login_oauth():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    print("DATS DA TOUKEN:---------------------------------->")
    refresh_token = token_response.json()["refresh_token"]

    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    print("lllllllllllll")
    print(userinfo_response)
    email = userinfo_response['email']
    picture = userinfo_response['picture']

    print("hhhhhhhhhhhhhhhhhhhhhhhhhh___hhhhh")

    # user from db
    # no user - register
    # yes user - continue
    # set session
    user = crud.get_user_by_email(email)
    if not user:
        user = crud.create_user(userinfo_response['given_name'], email, "")

    session["user_email"] = user.user_email

    user.refresh_token = refresh_token
    user.user_avatar = picture
    db.session.add(user)
    db.session.commit()

    update_steps(user.user_id)

    return redirect("/profile")


def getting_access_token(refresh_token):
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Preparing and sending a request to get tokens
    token_url, headers, body = client.prepare_refresh_token_request(
        token_endpoint, refresh_token)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    return token_response.json()["access_token"]


class FitnessRequest:
    def __init__(self, start, end, bucket=3600000):
        self.data = {
            "aggregateBy": [{
                "dataTypeName": "com.google.step_count.delta",
                "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
            }],
            "bucketByTime": {"durationMillis": bucket},
            "startTimeMillis": int(start*1000),
            "endTimeMillis": int(end*1000)
        }

    def to_body(self):
        return json.dumps(self.data)


@app.route("/friends")
def friends():
    """View friends list."""
    if "user_email" not in session:
        return redirect("/")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401

    receiver = user.user_id  # it is always user
    requests = crud.get_friend_rec(
        receiver)  # gives ID of a receiver(first)

    print("---------------------------")
    print(receiver)
    senders = []
    for req in requests:
        senders.append(req.sender)

    senders = set(senders)

    user_list = crud.get_users_by_ids(senders)
    print(user_list)
    friends = crud.get_friends(receiver)
    friends_list = crud.get_users_by_ids(friends)

    has_friend_requests = crud.is_there_friend_request(receiver=user.user_id)

    return render_template("friends.html", has_friend_requests=has_friend_requests, user_list=user_list, friends_list=friends_list)


@app.route("/friends/request", methods=["POST"])
def friend_request():

    if "user_email" not in session:
        return redirect("/")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401

    friend_email = request.get_json()['friend']
    recipient = crud.get_user_by_email(friend_email)
    if not recipient:
        return "{}", 404
    sender = user.user_id
    # todo: are we already friends?
    crud.create_friend_req(sender=sender, receiver=recipient.user_id)

    return "{}"


@app.route("/friends/invite", methods=["POST"])
def friend_invite():
    if "user_email" not in session:
        return redirect("/"), 401
    user = crud.get_user_by_email(session["user_email"])
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401

    new_friend = request.get_json()["friend"]
    challenge_id = request.get_json()["challenge_id"]
    crud.invite_to_challenge(
        sender=user.user_id, receiver=new_friend, challenge_id=challenge_id)

    return "{}"


@app.route("/friends/notadding", methods=["POST"])
def delete_request():
    friend_id = request.get_json()["friend"]
    if "user_email" not in session:
        return redirect("/"), 401
    user = crud.get_user_by_email(session["user_email"])
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401

    crud.delete_friend_req(sender=friend_id, receiver=user.user_id)

    return "{}"


@app.route("/friends/accepting", methods=["POST"])
def add_friend():

    friend_id = request.get_json()["friend"]
    if "user_email" not in session:
        return redirect("/"), 401
    user = crud.get_user_by_email(session["user_email"])
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401
    print("lllllllaaaaaaabas")

    # id = request.get_json()['friend_id']
    crud.make_friend(friend_id, user.user_id)

    crud.delete_friend_req(sender=friend_id, receiver=user.user_id)
    return "{}"


@app.route("/friends/removing_friends", methods=["POST"])
def remove_friend():
    new_friend = request.get_json()["friend"]
    if "user_email" not in session:
        return redirect("/"), 401
    user = crud.get_user_by_email(session["user_email"])
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401

    crud.lose_friend(sender=new_friend, receiver=user.user_id)

    return "{}"


@app.route("/challenges")
def challenges():
    """View challenges list."""
    if "user_email" not in session:
        return redirect("/"), 401
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    if not user:
        del session["user_email"]
        return "{}", 401

    user_id = user.user_id
    user_challenges = crud.get_user_challenges(user_id)
    challenges = crud.get_challenges()
    user_challenges_by_id = {}
    for user_challenge in user_challenges:
        user_challenges_by_id[user_challenge.challenge_id] = user_challenge

    requests_for_challenge = []
    all_challenge_invites = crud.challenge_invites(user_id)
    for invite in all_challenge_invites:
        challenge = crud.get_challenge_by_id(invite.challenge_id)
        sender = crud.get_user_by_id(invite.sender)
        requests_for_challenge.append(
            {"challenge": challenge, "sender": sender})

    # get all has_invites
    # for each inv find challenge and sender
    # create dict and pass to jinja

    return render_template("challenges.html", challenges=challenges, user_challenges_by_id=user_challenges_by_id, requests_for_challenge=requests_for_challenge)


@app.route("/challenges", methods=["POST"])
def join_challenges():
    if "user_email" not in session:
        return redirect("/"), 401
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    if not user:
        del session["user_email"]
        return "{}", 401

    challenge_id = request.get_json()['id']
    print(challenge_id)
    challenge_data = crud.get_challenge_by_id(challenge_id)
    start_time = date.today()

    crud.delete_all_challenge_invites(user.user_id, challenge_id)

    # todo are we joined yet?
    is_joined = crud.if_joined(user.user_id, challenge_id)
    if is_joined:
        return "{}"

    user_challenge = crud.add_data_to_user_challenges(
        user.user_id, challenge_data.challenge_id, start_time, start_time+timedelta(hours=challenge_data.duration), False)

    db.session.add(user_challenge)
    db.session.commit()

    # add data to that table
    resp = {
        'status': 'hell yeah',
        'title': challenge_data.title,
        'start': str(start_time),
        'duration': challenge_data.duration
    }
    return json.dumps(resp)


@app.route("/leaderboard")
def leaderboard():
    """View leaderboard."""
    leaders = crud.get_leader()
    if "user_email" not in session:
        return redirect("/")
    email = session["user_email"]
    user = crud.get_user_by_email(email)

    # user_steps = crud.get_steps()
    # print(user_steps)
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401
    return render_template("leaderboard.html", leaders=leaders)


@app.route("/achievements")
def achievements():
    """View achievements."""
    achievements = crud.get_achievements()
    if "user_email" not in session:
        return redirect("/")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401
    return render_template("achievements.html", achievements=achievements)


@app.route("/sync")
def sync():
    print("iiiiiiiiiiiiiiiiiiixxxxxxx")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    # checking if user exists
    if not user:
        del session["user_email"]
        return redirect("/")
    print(update_steps(user.user_id))

    return redirect("/profile")


@app.route("/logout")
def logout():
    email = session["user_email"]
    if "user_email" in session:
        del session["user_email"]

    return redirect("/")


@app.route("/cancel", methods=["POST"])
def cancel_invite():

    challenge_id = request.get_json()["id"]
    if "user_email" not in session:
        return redirect("/"), 401
    user = crud.get_user_by_email(session["user_email"])
    # checking if user exists
    if not user:
        del session["user_email"]
        return "{}", 401

    crud.delete_all_challenge_invites(
        receiver=user.user_id, challenge_id=challenge_id)

    return "{}"


def fetch_steps(token, day):
    day = date(day.year, day.month, day.day)
    start_time = datetime.combine(
        day, datetime.min.time()).timestamp()
    end_time = datetime.combine(
        day, datetime.max.time()).timestamp()
    req = FitnessRequest(start_time, end_time)
    headers = {
        "Content-Type": "application/json;encoding=utf-8",
        "Authorization": "Bearer " + token,
    }
    print(req.to_body())
    #  Sample outputL {'bucket': [{'startTimeMillis': '1705384320000', 'endTimeMillis': '1705387920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': [{'startTimeNanos': '1705384320000000000', 'endTimeNanos': '1705386154881356800', 'dataTypeName': 'com.google.step_count.delta', 'originDataSourceId': 'derived:com.google.step_count.delta:com.google.ios.fit:appleinc.:watch:860ab664:top_level', 'value': [{'intVal': 89, 'mapVal': []}]}]}]}, {'startTimeMillis': '1705387920000', 'endTimeMillis': '1705391520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705391520000', 'endTimeMillis': '1705395120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705395120000', 'endTimeMillis': '1705398720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705398720000', 'endTimeMillis': '1705402320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705402320000', 'endTimeMillis': '1705405920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705405920000', 'endTimeMillis': '1705409520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705409520000', 'endTimeMillis': '1705413120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705413120000', 'endTimeMillis': '1705416720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705416720000', 'endTimeMillis': '1705420320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705420320000', 'endTimeMillis': '1705423920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705423920000', 'endTimeMillis': '1705427520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705427520000', 'endTimeMillis': '1705431120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705431120000', 'endTimeMillis': '1705434720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705434720000', 'endTimeMillis': '1705438320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705438320000', 'endTimeMillis': '1705441920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705441920000', 'endTimeMillis': '1705445520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705445520000', 'endTimeMillis': '1705449120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705449120000', 'endTimeMillis': '1705452720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705452720000', 'endTimeMillis': '1705456320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705456320000', 'endTimeMillis': '1705459920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705459920000', 'endTimeMillis': '1705463520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705463520000', 'endTimeMillis': '1705467120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705467120000', 'endTimeMillis': '1705470720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}]}
    return requests.post("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate", headers=headers, data=req.to_body()).json()


def update_steps(user_id):
    user = crud.get_user_by_id(user_id)
    access_token = getting_access_token(user.refresh_token)

    week = 7
    for offset in range(week):
        day = date.today()-timedelta(days=offset)
        whole_data_pack = fetch_steps(access_token, day)
        daily_total = 0
        for element in whole_data_pack['bucket']:  # bucket
            for every_el in element['dataset']:  # start;end;dataset
                for el in every_el['point']:  # data,points
                    for e in el['value']:
                        daily_total += e['intVal']
        steps = crud.create_steps(
            user_id=user.user_id, daily_total=daily_total, date=day)
        db.session.merge(steps)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")

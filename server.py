"""Server for step_odyssey app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json
import crud
from datetime import time, date, datetime

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# TODO: crash if empty
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
    # name = request.args.get('user_name')
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
    daily_total = user.steps
    date = daily_total[0]
    steps = daily_total[1]

    challenges = crud.get_challenges()
    achievements = crud.get_achievements()

    return render_template("profile.html", name=user.user_name, date=date, steps=steps, challenges=challenges, achievements=achievements)


@app.route("/profile")
def profile():
    """View user profile."""
    # name = request.args.get('user_name')
    return render_template("profile.html")


@app.route("/signup")
def show_register_user():
    return render_template("signin.html")


@app.route("/signup", methods=["POST"])
def register_user():
    """Register user."""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    print('ddddddddddd'+name)

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
        return redirect("/signup")
    else:
        user = crud.create_user(name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def logging_in():
    """Logging user in."""

    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)

    user = crud.get_user_by_email(email)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(user)
# sup
    if not user or user.user_password != password:
        flash("Email or password are incorrect, my friend.")
        return redirect("/")
    else:
        session["user_email"] = user.user_email
        flash(f"Hey there, {user.user_email}, what's up?")
    return redirect("/profile")


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
        scope=["openid", "email",
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

    user = crud.get_user_by_email(session['user_email'])
    user.refresh_token = refresh_token
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

    return render_template("friends.html")


@app.route("/challenges")
def challenges():
    """View challenges list."""
    challenges = crud.get_challenges()

    return render_template("challenges.html", challenges=challenges)


@app.route("/leaderboard")
def leaderboard():
    """View leaderboard."""

    return render_template("leaderboard.html")


@app.route("/achievements")
def achievements():
    """View achievements."""
    achievements = crud.get_achievements()
    return render_template("achievements.html", achievements=achievements)


@app.route("/sync")
def sync():
    # ar yra useris
    # ar prijungtas
    update_steps()

    return redirect("/profile")


def fetch_steps(token):
    today = date.today()
    today = date(today.year, today.month, today.day-1)
    start_time = datetime.combine(
        today, datetime.min.time()).timestamp()
    end_time = datetime.combine(
        today, datetime.max.time()).timestamp()
    # TODO:  put in fitnessrequest calculation to start day from specific day (and end)
    req = FitnessRequest(start_time, end_time)
    headers = {
        "Content-Type": "application/json;encoding=utf-8",
        "Authorization": "Bearer " + token,
    }
    print(req.to_body())
    #  Sample outputL {'bucket': [{'startTimeMillis': '1705384320000', 'endTimeMillis': '1705387920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': [{'startTimeNanos': '1705384320000000000', 'endTimeNanos': '1705386154881356800', 'dataTypeName': 'com.google.step_count.delta', 'originDataSourceId': 'derived:com.google.step_count.delta:com.google.ios.fit:appleinc.:watch:860ab664:top_level', 'value': [{'intVal': 89, 'mapVal': []}]}]}]}, {'startTimeMillis': '1705387920000', 'endTimeMillis': '1705391520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705391520000', 'endTimeMillis': '1705395120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705395120000', 'endTimeMillis': '1705398720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705398720000', 'endTimeMillis': '1705402320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705402320000', 'endTimeMillis': '1705405920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705405920000', 'endTimeMillis': '1705409520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705409520000', 'endTimeMillis': '1705413120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705413120000', 'endTimeMillis': '1705416720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705416720000', 'endTimeMillis': '1705420320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705420320000', 'endTimeMillis': '1705423920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705423920000', 'endTimeMillis': '1705427520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705427520000', 'endTimeMillis': '1705431120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705431120000', 'endTimeMillis': '1705434720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705434720000', 'endTimeMillis': '1705438320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705438320000', 'endTimeMillis': '1705441920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705441920000', 'endTimeMillis': '1705445520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705445520000', 'endTimeMillis': '1705449120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705449120000', 'endTimeMillis': '1705452720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705452720000', 'endTimeMillis': '1705456320000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705456320000', 'endTimeMillis': '1705459920000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705459920000', 'endTimeMillis': '1705463520000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705463520000', 'endTimeMillis': '1705467120000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}, {'startTimeMillis': '1705467120000', 'endTimeMillis': '1705470720000', 'dataset': [{'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:aggregated', 'point': []}]}]}
    return requests.post("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate", headers=headers, data=req.to_body()).json(), today
    # TODO: write steps to db


def update_steps(user_id):
    user = crud.get_user_by_id(user_id)
    access_token = getting_access_token(user.refresh_token)
    whole_data_pack, today = fetch_steps(access_token)
    print("------------------------------", whole_data_pack)
    daily_total = 0
    print(whole_data_pack)
    for element in whole_data_pack['bucket']:  # bucket
        for every_el in element['dataset']:  # start;end;dataset
            for el in every_el['point']:  # datasr,points
                for e in el['value']:
                    daily_total += e['intVal']
    steps = crud.create_steps(
        user_id=user.user_id, daily_total=daily_total, date=today)
    db.session.merge(steps)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")

"""Server for step_odyssey app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    # name = request.args.get('user_name')
    return render_template("homepage.html")


@app.route('/profile')
def rendering_profile():
    """User profile."""
    if "user_email" not in session:
        return redirect("/signup")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
# tghjk
    return render_template("profile.html", name=user.user_name)


@app.route("/signup")
def show_register_user():
    return render_template("signin.html")


@app.route("/signup", methods=["POST"])
def register_user():
    """Register user."""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

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


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

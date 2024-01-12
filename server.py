"""Server for step_odyssey app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud


app = Flask(__name__)


@app.route("/")
def homepage():
    """View homepage."""
    name = request.args.get('user_name')
    return render_template("homepage.html")


@app.route('/profile')
def rendering_profile():
    """Greet user."""
    name = request.args.get('user_name')
    if not name:
        return redirect("/signin")

    return render_template("profile.html", name=name)


@app.route("/signin")
def signing_up():
    """View sign up form."""

    return render_template("signin.html")


@app.route("/signin", methods=["POST"])
def register_user():
    """Create a new user."""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(name)

    if user:
        flash("The user with this name already exists. Try again.")
    else:
        user = crud.create_user(name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Great! Your account has been created! Please log in.")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

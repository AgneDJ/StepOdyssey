"""Server for step_odyssey app."""

from flask import Flask, render_template, request, flash, session, redirect
import crud


app = Flask(__name__)


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/login")
def loggin_in():
    """View login form."""

    return render_template("login.html")


if __name__ == "__main__":
    #     connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

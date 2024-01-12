import os
import json
from random import choice, randint
from datetime import datetime
import crud
import server
from model import User,  connect_to_db, db


os.system('dropdb step_challenge')
os.system('createdb step_challenge')


def connect_to_db(flask_app, db_uri="postgresql:///step_challenge", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)

    with app.app_context():
        db.create_all()
        example_data()

from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baba_wisdom.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATONS'] = False

    db.init(app)

    with app.app_contect():
        db.create_all()

    return app
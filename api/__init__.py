from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager

db = SQLAlchemy()

base_dir = os.path.dirname(os.path.abspath(__file__))
db_name = os.getenv('DB_NAME')
db_path = os.path.join(base_dir, db_name)

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Initialize Flask extensions here

    # Register blueprints here
    from api.main import bp as main_bp
    app.register_blueprint(main_bp)

    from api.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # from api.wisdom import bp as wisdom_bp
    # app.register_blueprint(wisdom_bp)

    from .models import User, Baba, Apprentice, Review, Wisdom, Category, WisdomCategories

    create_database(app)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Patter</h1>'
    
    return app


def create_database(app):
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print(f'Created database at {os.path.abspath(db_path)}!')
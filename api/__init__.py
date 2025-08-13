from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager

db = SQLAlchemy()

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
db_name = os.getenv('DB_NAME')
db_path = os.path.join(base_dir, db_name)

def create_app():

    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    )
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Initialize Flask extensions here

    # Register blueprints here
    from api.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from api.home import bp as home_bp
    app.register_blueprint(home_bp)

    from .models import User, Baba, Apprentice, Review, Wisdom, Category, WisdomCategories

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print(f'Created database at {os.path.abspath(db_path)}!')
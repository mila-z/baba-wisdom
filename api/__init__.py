"""
Initialize the Flask application and its extensions. 

This module sets up the Flask app, configures the database,
registers blueprints, and initializes login management.
"""
import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager

db = SQLAlchemy()

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.getenv('DB_NAME')
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    - Sets up Flask with templates and configuration.
    - Initializes the database (SQLAlchemy).
    - Registers all application blueprints.
    - Configures login management.

    Returns:
        Flask: the configured Flask application instance.
    """
    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    )
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from api.auth import bp as auth_bp # pylint: disable=import-outside-toplevel
    app.register_blueprint(auth_bp)

    from api.home import bp as home_bp # pylint: disable=import-outside-toplevel
    app.register_blueprint(home_bp)

    from api.wisdom import bp as wisdom_bp # pylint: disable=import-outside-toplevel
    app.register_blueprint(wisdom_bp)

    from api.search import bp as search_bp # pylint: disable=import-outside-toplevel
    app.register_blueprint(search_bp)

    from api.review import bp as review_bp # pylint: disable=import-outside-toplevel
    app.register_blueprint(review_bp)

    from api.admin import bp as admin_bp # pylint: disable=import-outside-toplevel
    app.register_blueprint(admin_bp)

    from .models import User # pylint: disable=import-outside-toplevel

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return User.query.get(int(user_id))
    return app

def create_database(app: Flask) -> None:
    """
    Create the database if it foes not already exist.

    Args:
        app (Flask): The Flask appliation instance.
    """
    if not os.path.exists(DB_PATH):
        with app.app_context():
            db.create_all()
        print(f'Created database at {os.path.abspath(DB_PATH)}!')

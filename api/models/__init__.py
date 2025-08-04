from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, Baba, Apprentice
from .review import Review
from .wisdom import Wisdom
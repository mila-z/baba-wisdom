"""
User, Baba, and Apprentice models.

Defines the User model (with roles 'admin', 'baba', 'apprentice') and its
associated profile models: Baba and Apprentice. Each model includes a
utility methid to convert instances into dictionaries.
"""
from typing import Dict
from flask_login import UserMixin
from api import db

class User(db.Model, UserMixin):
    """
    User model representing a registered user of the application.

    Attributes:
        id (int): Primary key.
        email (str): Unique email of the user.
        password (str): Hashed password.
        username (str): Unique username.
        role (str): Role of the user ('admin', 'baba', 'apprentice').
        baba (Baba): One-to-one relationship to the Baba profile.
        apprentice (Apprentice): One-to-one relationship to the Apprentice profile.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    baba = db.relationship(
        'Baba', 
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    apprentice = db.relationship(
        'Apprentice', 
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the User instance into a dictionary.

        Returns:
            dict: A dictionary containing 'id', 'email', 
            'username', 'role' and 'type' of the user.
        """
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'type': self.type
        }

class Baba(db.Model):
    """
    User model representing a user that has the role baba.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the User.
        village (str): Vilage that the baba is from.
        bio (str): Bio that contains information about the baba.
        user (User): One-to-one relationship to the user profile.
        wisdom (list[Wisdom]): One-to-many relationship to the Wisdom module.
    """
    __tablename__ = 'babas'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    village = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    user = db.relationship('User', back_populates='baba')
    wisdom = db.relationship('Wisdom', back_populates='baba', cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the Baba instance into a dictionary.

        Returns:
            dict: A dictionary containing 'id', 'user_id', 
            'village', and 'bio' of the baba.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'village': self.village,
            'bio': self.bio
        }

class Apprentice(db.Model):
    """
    User model representing a user that has the role apprentice.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the User.
        birth_date (date): Date of birth of the apprentice.
        user (User): One-to-one relationship to the user profile.
        reviews (list[Review]): One-to-many relationship to Review.
    """
    __tablename__ = 'apprentices'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    user = db.relationship('User', back_populates = 'apprentice')
    reviews = db.relationship('Review', back_populates='apprentice')

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the Apprentice instance into a dictionary.

        Returns:
            dict: A dictionary containing 'id', 'user_id', 
            and 'birth_date' of the apprentice.
        """
        return {
            'id': self.id,
            'user_id': self.iser_id,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None
        }

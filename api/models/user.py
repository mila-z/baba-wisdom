from api import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # role -> 'admin', 'baba', 'apprentice'
    role = db.Column(db.String(20), nullable=False)

    # relationship setup
    baba = db.relationship('Baba', back_populates='user', uselist=False, cascade='all, delete-orphan')
    apprentice = db.relationship('Apprentice', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'type': self.type
        }


class Baba(db.Model):
    __tablename__ = 'babas'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    village = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # relationship setup
    user = db.relationship('User', back_populates='baba')
    # each baba has many wisdom
    wisdom = db.relationship('Wisdom', back_populates='baba', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'village': self.village,
            'bio': self.bio
        }

class Apprentice(db.Model):
    __tablename__ = 'apprentices'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # relationship setup
    user = db.relationship('User', back_populates = 'apprentice')
    # each apprentice has many reviews
    reviews = db.relationship('Review', back_populates='apprentice')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.iser_id,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None
        }
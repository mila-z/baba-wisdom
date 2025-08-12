from api import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # role -> 'admin', 'baba', 'apprentice'
    role = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'type': self.type
        }


class Baba(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    village = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # foreign keys
    # each baba has many wisdom
    wisdoms = db.relationship('Wisdom', back_populates='baba')
    baba_id = db.relationship('User', back_populates='baba')

    def to_dict(self):
        data = super().to_dict()
        data['village'] = self.village
        data['bio'] = self.bio
        return data

class Apprentice(User):
    birth_date = db.Column(db.Date, nullable=True)
    
    # foreign keys
    # each apprentice has many reviews
    reviews = db.relationship('Review', back_populates='apprentice')
    apprentice_id = db.relationship('User', back_populates = 'apprentice')

    def to_dict(self):
        data = super().to_dict()
        data['birth_date'] = self.birth_date.isoformat() if self.birth_date else None
        return data
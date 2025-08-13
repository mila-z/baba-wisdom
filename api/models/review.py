from api import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True)
    num_stars = db.Column(db.Integer, nullable = False)
    text = db.Column(db.Text)

    # realtionship setup
    # each review has one apprentice-author
    apprentice_id = db.Column(db.Integer, db.ForeignKey('apprentices.id'), nullable=False)
    apprentice = db.relationship('Apprentice', back_populates='reviews')
    # each review is under one wisdom
    wisdom_id = db.Column(db.Integer, db.ForeignKey('wisdom.id'), nullable=False)
    wisdom = db.relationship('Wisdom', back_populates='reviews')

    def __init__(self, num_stars, text=None):
        if not(0 <= num_stars <= 5):
            raise ValueError("Number of stars must be between 0 and 5.")
        self.num_stars = num_stars
        self.text = text

    def to_dict(self):
        return {
            'id': self.id,
            'num_stars': self.num_stars,
            'text': self.text
        }
    

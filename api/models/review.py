"""
Review model.

Defines the Review table with relationships to Apprentice (author)
and Wisdom (the wisdom being reviewed). Includes a utility method
to convert a Review instance to a dictionary.
"""
from typing import Dict
from api import db

class Review(db.Model):
    """
    Review model representing a review under a wisdom.

    Attributes:
        id (int): Primary key.
        num_sars (int): Number of stars the author has left (necessary).
        text (str): Text the author has left in addition to the stars (optional).
        apprentice_id (str): Foreign key to the Apprentice.
        apprentice (Apprentice): One-to-many relationship to the Apprentice profile.
        wisdom_id (str): Foreign key to the Wisdom.
        wisdom (Wisdom): One-to-many relationship to the Wisdom module.
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True)
    num_stars = db.Column(db.Integer, nullable = False)
    text = db.Column(db.Text)
    apprentice_id = db.Column(db.Integer, db.ForeignKey('apprentices.id'), nullable=False)
    apprentice = db.relationship('Apprentice', back_populates='reviews')
    wisdom_id = db.Column(db.Integer, db.ForeignKey('wisdom.id'), nullable=False)
    wisdom = db.relationship('Wisdom', back_populates='reviews')

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the Review instance into a dictionary.

        Returns:
            dict: A dictionary containing 'id', 'num_stars', and 'text' of the review.
        """
        return {
            'id': self.id,
            'num_stars': self.num_stars,
            'text': self.text
        }

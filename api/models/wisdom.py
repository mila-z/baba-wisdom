"""
Wisdom and Category models.

Defines the Wisdom model representing a piece of wisdom content, the
Category model for categorization, and the WisdomCategories association
table for the many-to-many relationship between Wisdom and Category.
"""
from typing import Dict
from sqlalchemy.sql import func
from api import db

class WisdomCategories(db.Model):
    """
    Association table linking Wisdom and Category.

    Attributes:
        id (int): Primary key.
        wisdom_id (int): Foreign key to the Wisdom.
        category_id (int): Foreign key to the Category.
    """
    __tablename__ = 'wisdom_categories'
    id = db.Column(db.Integer, primary_key=True)
    wisdom_id = db.Column(db.Integer, db.ForeignKey('wisdom.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class Wisdom(db.Model):
    """
    Wisdom model representing a piece of wisdom shared by a Baba.

    Attributes:
    id (int): Primary key.
    text (str): Text of the wisdom.
    age_restriction (Optional[int]): Minimum age required to view the wisdom.
    posted (datetime): Timestamp when the wisdom was posted.
    baba_id (int): Foreign key to the Baba.
    baba (Baba): Relationship to the Baba.
    reviews (List[Review]): Reviews for this wisdom.
    categories (List[Category]): Categories associated with this wisdom.
    """
    __tablename__ = 'wisdom'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable = False)
    age_restriction = db.Column(db.Integer)
    posted = db.Column(db.DateTime(timezone=True), default=func.now())
    baba_id = db.Column(db.Integer, db.ForeignKey('babas.id'), nullable=False)
    baba = db.relationship('Baba', back_populates='wisdom')
    reviews = db.relationship('Review', back_populates='wisdom', cascade='all, delete-orphan')
    categories = db.relationship(
        'Category',
        secondary=WisdomCategories.__table__,
        back_populates='wisdom'
    )

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the Wisdom instance into a dictionary.

        Returns:
            dict: A dictionary containing 'id', 'text', 
            'age_restriction', and 'posted' of the wisdom.
        """
        return {
            'id': self.id,
            'text': self.text,
            'age_restriction': self.age_restriction,
            'posted': self.posted
        }

class Category(db.Model):
    """
    Category model for classifying wisdom.

    Attributes:
        id (int): Primary key.
        name (str): Unique name of the category.
        wisdom (List[Wisdom]): Wisdom associated with this caegory.
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    wisdom = db.relationship(
        'Wisdom',
        secondary=WisdomCategories.__table__,
        back_populates='categories'
    )

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the Category instance into a dictionary.

        Returns:
            dict: A dictionary containing 'id' and 'name' of the category.
        """
        return {
            'id': self.id,
            'name': self.name
        }

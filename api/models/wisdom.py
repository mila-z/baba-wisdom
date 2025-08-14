from api import db
from sqlalchemy.sql import func

class WisdomCategories(db.Model):
    __tablename__ = 'wisdom_categories'
    id = db.Column(db.Integer, primary_key=True)
    wisdom_id = db.Column(db.Integer, db.ForeignKey('wisdom.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class Wisdom(db.Model):
    __tablename__ = 'wisdom'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable = False)
    age_restriction = db.Column(db.Integer)
    posted = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # relationship setup
    # each wisdom has one baba-author
    baba_id = db.Column(db.Integer, db.ForeignKey('babas.id'), nullable=False)
    baba = db.relationship('Baba', back_populates='wisdom')
    # each wisdom has many reviews
    reviews = db.relationship('Review', back_populates='wisdom')
    # each wisdom has many categories
    categories = db.relationship('Category', secondary=WisdomCategories.__table__, back_populates='wisdom')

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'age_restriction': self.age_restriction,
            'posted': self.posted
        }
    
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # foreign keys
    # each category could be used in many wisdom
    wisdom = db.relationship('Wisdom', secondary=WisdomCategories.__table__, back_populates='categories')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
from . import db

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
    
    # foreign keys
    # each wisdom has one baba-author
    baba_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    baba = db.relationship('Baba', back_populates='wisdoms')
    # each wisdom has many reviews
    reviews = db.relationship('Review', back_populates='wisdom')
    # each wisdom has many categories
    categories = db.relationship('Category', secondary=WisdomCategories.__table__, back_populates='wisdom')

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'age_restriction': self.age_restriction,
            'categories': [cat.name for cat in self.categories]
        }
    
    def set_categories(self, category_names, session):
        categories = []
        for name in category_names:
            name = name.strip().lower()
            category = session.query(Category).filter_by(name=name).first()
            if not category:
                category = Category(name=name)
                session.add(category)
            categories.append(category)
        self.categories = categories
    
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
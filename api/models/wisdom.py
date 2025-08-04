from . import db

class Wisdom(db.Model):
    __tablename__ = 'wisdom'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable = False)
    category = db.Column(db.Text, nullable = False)
    age_restriction = db.Column(db.Integer)
    
    # foreign keys
    # each wisdom has one baba-author
    baba_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    baba = db.relationship('Baba', back_populates='wisdoms')
    # each wisdom has many reviews
    reviews = db.relationship('Review', back_populates='wisdom')


    def get_categories(self):
        return [c.strip() for c in self.category.split(',')] if self.category else []
    
    def set_category(self, categories):
        self.category = ','.join([c.strip() for c in categories if c.strip()])

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'categories': self.get_categories(),
            'age_restriction': self.age_restriction
        }
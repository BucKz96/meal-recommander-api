from .. import db


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    ingredients = db.Column(db.String(500))

    def __repr__(self):
        return f"<Meal {self.name}>"

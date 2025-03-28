from .database import db


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients.split(', '),
            'calories': self.calories,
            'cuisine': self.cuisine
        }


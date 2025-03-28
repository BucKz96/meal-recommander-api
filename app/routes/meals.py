from flask import Blueprint, jsonify, request
from ..models.meal import Meal
from .. import db

meals_bp = Blueprint('meals', __name__)

@meals_bp.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([{'id': meal.id, 'name': meal.name, 'description': meal.description, 'ingredients': meal.ingredients} for meal in meals])

@meals_bp.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    new_meal = Meal(name=data['name'], description=data.get('description'), ingredients=data.get('ingredients'))
    db.session.add(new_meal)
    db.session.commit()
    return jsonify({'message': 'Meal added successfully'}), 201

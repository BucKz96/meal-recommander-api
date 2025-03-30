from flask import Blueprint, jsonify, request
from meal_app.models.meal import Meal
from meal_app import db

meals_bp = Blueprint('meals', __name__)

@meals_bp.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([{'id': meal.id, 'name': meal.name, 'description': meal.description, 'ingredients': meal.ingredients} for meal in meals])


@meals_bp.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()

    if not data or 'name' not in data or 'description' not in data or 'ingredients' not in data:
        return jsonify({"error": "Missing required fields: name, description, ingredients"}), 400

    try:
        meal = Meal(name=data['name'], description=data['description'], ingredients=data['ingredients'])
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Meal created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, jsonify, request
from .models import Meal
from .database import db
import csv
import os

api = Blueprint('api', __name__)


@api.route("/")
def home():
    return "Hello, World!"


@api.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([meal.to_dict() for meal in meals])


@api.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    new_meal = Meal(
        name=data['name'],
        ingredients=data['ingredients'],
        calories=data['calories'],
        cuisine=data['cuisine']
    )
    db.session.add(new_meal)
    db.session.commit()
    return jsonify(new_meal.to_dict()), 201


@api.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    data = request.get_json()
    meal = Meal.query.get_or_404(meal_id)

    meal.name = data.get('name', meal.name)
    meal.ingredients = data.get('ingredients', meal.ingredients)
    meal.calories = data.get('calories', meal.calories)
    meal.cuisine = data.get('cuisine', meal.cuisine)

    db.session.commit()
    return jsonify(meal.to_dict())


@api.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'message': 'Meal deleted successfully'})


@api.route('/import', methods=['POST'])
def import_meals():
    file_path = os.path.join(os.getcwd(), 'data', 'meals.csv')
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                new_meal = Meal(
                    name=row['name'],
                    ingredients=', '.join(row['ingredients'].split(', ')),
                    calories=int(row['calories']),
                    cuisine=row['cuisine']
                )
                db.session.add(new_meal)
            except Exception as e:
                print(f"Error importing meal {row['name']}: {e}")
        db.session.commit()
    return jsonify({'message': 'Data imported successfully'}), 201

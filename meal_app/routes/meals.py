from flask import Blueprint, jsonify, request
from meal_app.models.meal import Meal
from meal_app import db
import os
import csv

ALLOWED_CSV_DIR = "/data"

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


@meals_bp.route('/meals/import_csv', methods=['POST'])
def import_csv():
    data = request.get_json()

    if not data or 'file_path' not in data:
        return jsonify({"error": "Missing required field: file_path"}), 400

    try:
        filename = os.path.basename(data['file_path'])
        full_path = os.path.join(ALLOWED_CSV_DIR, filename)

        if not os.path.exists(full_path):
            return jsonify({"error": f"File '{filename}' not found in {ALLOWED_CSV_DIR}"}), 404

        imported_count = 0

        with open(full_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                name = row.get("name")
                description = row.get("description", "")
                ingredients = row.get("ingredients", "")

                if not name:
                    continue

                existing = Meal.query.filter_by(name=name).first()
                if existing:
                    continue

                meal = Meal(name=name, description=description, ingredients=ingredients)
                db.session.add(meal)
                imported_count += 1

            db.session.commit()

        return jsonify({"message": f"{imported_count} meals imported successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



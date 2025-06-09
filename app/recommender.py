from .models import Meal
import csv
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "meals.csv"

def load_meals():
    meals = []
    with open(DATA_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            meal = Meal(
                name=row["name"],
                ingredients=[i.strip().lower() for i in row["ingredients"].split(",")],
                calories=int(row["calories"]),
                cuisine=row["cuisine"]
            )
            meals.append(meal)
    return meals

def recommend_meals(available_ingredients: list[str]) -> list[Meal]:
    available = [i.strip().lower() for i in available_ingredients]
    meals = load_meals()
    return [
        meal for meal in meals
        if all(ingredient in available for ingredient in meal.ingredients)
    ]

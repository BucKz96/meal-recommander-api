import pandas as pd
import ast
from .models import Meal
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "recipe.csv"

def safe_parse_ingredients(val):
    if isinstance(val, list):
        return [i.strip().lower() for i in val if isinstance(i, str)]

    try:
        # list ou dict
        parsed = ast.literal_eval(val)
        if isinstance(parsed, list):
            return [i.strip().lower() for i in parsed if isinstance(i, str)]
    except (ValueError, SyntaxError):
        pass

    # Fallback if not object Python valid
    cleaned = val.replace("\n", " ").replace("#", "").replace("^", ",")
    return [i.strip().lower() for i in cleaned.split(",") if i.strip()]



def extract_calories(val):
    try:
        data = ast.literal_eval(val)
        return int(float(data.get("amount", 0)))
    except Exception:
        return 0


def load_meals() -> list[Meal]:
    df = pd.read_csv(DATA_PATH)

    # Nettoyage & transformation
    df["ingredients"] = df["ingredients"].apply(safe_parse_ingredients)
    df["name"] = df["recipe_name"].fillna("Unnamed Recipe")
    df["cuisine"] = df["tags"].apply(lambda x: x.split(",")[0].strip() if isinstance(x, str) and "," in x else x if isinstance(x, str) else "")
    if "calories" in df.columns:
        df["calories"] = df["calories"].apply(extract_calories).fillna(0).astype(int)
    else:
        df["calories"] = 0

    ## ingredients=['all-purpose flour^salt^baking soda^baking powder^ground cinnamon^eggs^vegetable oil
    # ^white sugar^vanilla extract^grated zucchini^chopped walnuts']

    meals = [
        Meal(
            name=row["name"],
            ingredients=[i.strip().lower() for i in row["ingredients"]],
            calories=row["calories"],
            cuisine=row["cuisine"]
        )
        for _, row in df.iterrows()
    ]
    print(meals[0])
    return meals


def recommend_meals(available_ingredients: list[str]) -> list[Meal]:
    available = {i.strip().lower() for i in available_ingredients}
    meals = load_meals()

    scored_meals = []

    for meal in meals:
        matched_ingredients = available.intersection(set(meal.ingredients))
        score = len(matched_ingredients)

        if score > 0:
            scored_meals.append((score, meal))

    # Tri décroissant sur le score (meilleurs en haut)
    scored_meals.sort(key=lambda x: x[0], reverse=True)

    # Retourne juste les objets Meal triés
    return [meal for _, meal in scored_meals]


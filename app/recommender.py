import pandas as pd
from pathlib import Path
from .models import Meal
import ast

DATA_PATH = Path(__file__).parent / "data" / "recipes_clean.csv"

def parse_ingredients(val):
    if isinstance(val, list):
        return [i.strip().lower() for i in val]
    if isinstance(val, str):
        return [i.strip().lower() for i in val.split(",") if i.strip()]
    return []

def parse_nutritions(val):
    try:
        if isinstance(val, str):
            nutrition = ast.literal_eval(val)
        elif isinstance(val, dict):
            nutrition = val
        else:
            return {}

        # Nettoyage des valeurs numériques
        clean_nutrition = {}
        for k in ["calories", "protein", "fat", "carbohydrates", "sugars", "fiber"]:
            try:
                clean_nutrition[k] = round(float(nutrition.get(k, 0)), 2)
            except:
                clean_nutrition[k] = 0.0
        return clean_nutrition
    except Exception:
        return {}

def load_meals() -> list[Meal]:
    df = pd.read_csv(DATA_PATH)

    # Nom et ingrédients
    df["name"] = df["name"].fillna("Unnamed Recipe")
    df["ingredients"] = df["ingredients"].apply(parse_ingredients)

    # Nutrition (dict nettoyé)
    df["nutritions"] = df["nutritions"].apply(parse_nutritions)

    # Cuisine = premier tag s’il existe
    df["cuisine"] = df.get("tags", "").apply(
        lambda x: x.split(",")[0].strip() if isinstance(x, str) and "," in x else (x.strip() if isinstance(x, str) else "")
    )
    df["prep_time"] = df["prep_time"].astype(str).str.replace('-', ' ')

    # Colonnes additionnelles : fallback safe
    for col in ["prep_time", "diet_type", "dish_type", "seasonal", "image_url"]:
        df[col] = df.get(col, "").fillna("")

    # Construction des objets Meal
    meals = [
        Meal(
            name=row["name"],
            ingredients=row["ingredients"],
            cuisine=row["cuisine"],
            image=row["image_url"],
            prep_time=row["prep_time"],
            diet_type=row["diet_type"],
            dish_type=row["dish_type"],
            seasonal=row["seasonal"],
            nutritions=row["nutritions"]
        )
        for _, row in df.iterrows()
    ]

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

    scored_meals.sort(key=lambda x: x[0], reverse=True)
    return [meal for _, meal in scored_meals]

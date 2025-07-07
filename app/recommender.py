import pandas as pd
from pathlib import Path
from .models import Meal
import ast
import os
import requests

DATA_DIR = Path(__file__).parent / "data"
DATA_PATH = DATA_DIR / "recipes_clean.csv"
CSV_URL = "https://huggingface.co/spaces/BucKz96/csv_app/resolve/main/recipes_clean.csv"

def download_csv_if_missing():
    if not DATA_PATH.exists():
        print("\n Downloading dataset...")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            r = requests.get(CSV_URL)
            r.raise_for_status()
            DATA_PATH.write_bytes(r.content)
            print("Dataset downloaded successfully.")
        except Exception as e:
            print("Failed to download dataset:", e)

download_csv_if_missing()

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
    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print("Failed to read CSV:", e)
        return []

    # Assure toutes les colonnes requises
    required_columns = ["name", "ingredients", "nutritions", "tags", "prep_time", "diet_type", "dish_type", "seasonal", "image_url"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    df["name"] = df["name"].fillna("Unnamed Recipe")
    df["ingredients"] = df["ingredients"].apply(parse_ingredients)
    df["nutritions"] = df["nutritions"].apply(parse_nutritions)
    df["cuisine"] = df["tags"].apply(
        lambda x: x.split(",")[0].strip() if isinstance(x, str) and "," in x else (x.strip() if isinstance(x, str) else "")
    )
    df["prep_time"] = df["prep_time"].astype(str).str.replace('-', ' ')

    for col in ["prep_time", "diet_type", "dish_type", "seasonal", "image_url"]:
        df[col] = df[col].fillna("")

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
        matched_ingredients = [
            ing for ing in meal.ingredients
            if any(user_ing in ing for user_ing in available)
        ]
        score = len(matched_ingredients)
        if score > 0:
            scored_meals.append((score, meal))

    scored_meals.sort(key=lambda x: x[0], reverse=True)
    return [meal for _, meal in scored_meals]

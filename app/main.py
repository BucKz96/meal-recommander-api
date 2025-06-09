from fastapi import FastAPI, Query
from fastapi.params import Query as FastAPIQuery

from .recommender import recommend_meals

app = FastAPI()

@app.get("/meals/by-ingredients")
def get_meals_by_ingredients(
    available_ingredients: list[str] = FastAPIQuery(...)
):
    meals = recommend_meals(available_ingredients)
    return [meal.dict() for meal in meals]

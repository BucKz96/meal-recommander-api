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


@app.get("/meals/all")
def get_all_meals(cuisine: str | None = Query(None, description="Filter by type")):
    meals = load_meals()
    if cuisine:
        cuisine = cuisine.strip().lower()
        meals = [m for m in meals if m.cuisine.lower() == cuisine]
    return [meal.dict() for meal in meals]
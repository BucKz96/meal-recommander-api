from pydantic import BaseModel

class Meal(BaseModel):
    name: str
    ingredients: list[str]
    calories: int
    cuisine: str

from pydantic import BaseModel
from typing import List, Optional

class Meal(BaseModel):
    name: str
    ingredients: List[str]
    cuisine: Optional[str] = None
    image: Optional[str] = None
    prep_time: Optional[str] = None
    diet_type: Optional[str] = None
    dish_type: Optional[str] = None
    seasonal: Optional[str] = None
    nutritions: dict
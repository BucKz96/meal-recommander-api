from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_meals_by_ingredients_valid():
    params = [
        ("available_ingredients", "chicken"),
        ("available_ingredients", "rice"),
        ("available_ingredients", "tomato"),
    ]
    response = client.get("/meals/by-ingredients", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for meal in data:
        assert "name" in meal
        assert "ingredients" in meal
        assert "calories" in meal
        assert "cuisine" in meal


def test_meals_by_ingredients_empty():
    response = client.get("/meals/by-ingredients", params={"available_ingredients": []})
    assert response.status_code == 422  # car Query(...) impose un champ obligatoire

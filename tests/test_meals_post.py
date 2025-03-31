def test_add_meal_success(client):
    payload = {
        "name": "Test Meal",
        "description": "For testing",
        "ingredients": "Ingredient1, Ingredient2"
    }
    response = client.post('/meals', json=payload)
    assert response.status_code == 201


def test_add_meal_missing_data(client):
    response = client.post('/meals', json={'name': 'Pizza'})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required fields: name, description, ingredients"}

    response = client.post('/meals', json={'description': 'Tasty pizza'})
    assert response.status_code == 400

    response = client.post('/meals', json={'ingredients': 'cheese, tomato, dough'})
    assert response.status_code == 400

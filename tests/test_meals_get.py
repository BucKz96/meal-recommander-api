def test_get_meals(client):
    response = client.get('/meals')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_meal_by_id_success(client):
    response = client.get("/meals/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert "name" in data
    assert "ingredients" in data
    assert "description" in data


def test_get_meal_by_id_not_found(client):
    response = client.get("/meals/999999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data or "message" in data

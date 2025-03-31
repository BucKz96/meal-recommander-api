def test_get_meals(client):
    response = client.get('/meals')
    assert response.status_code == 200
    assert isinstance(response.json, list)

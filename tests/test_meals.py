import pytest
from meal_app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_meals(client):
    response = client.get('/meals')
    assert response.status_code == 200

def test_add_meal(client):
    response = client.post('/meals', json={'name': 'Spaghetti', 'description': 'Pasta with sauce', 'ingredients': 'pasta,tomato'})
    assert response.status_code == 201

def test_get_meal_invalid_id(client):
    response = client.get('/meals/999')
    assert response.status_code == 404

def test_add_meal_missing_data(client):
    response = client.post('/meals', json={'name': 'Pizza'})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required fields: name, description, ingredients"}

    response = client.post('/meals', json={'description': 'Tasty pizza'})
    assert response.status_code == 400

    response = client.post('/meals', json={'ingredients': 'cheese, tomato, dough'})
    assert response.status_code == 400

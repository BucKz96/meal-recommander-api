import pytest
from app import create_app, db


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

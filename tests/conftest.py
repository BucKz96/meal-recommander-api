import pytest
from meal_app import create_app, db as _db
import os


@pytest.fixture(scope='session')
def app():
    app = create_app()
    db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/test_mealdb")
    print("✅ DATABASE_URL used:", db_url)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": db_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        _db.drop_all()
        _db.create_all()

    yield app

    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

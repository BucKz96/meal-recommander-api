import pytest
from meal_app import create_app, db as _db
from flask import Flask
from sqlalchemy import text


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/test_mealdb",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        _db.drop_all()
        _db.create_all()

    yield app

    # Clean up
    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

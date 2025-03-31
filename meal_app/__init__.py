from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("meal_app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from meal_app.routes.meals import meals_bp
    app.register_blueprint(meals_bp)

    return app

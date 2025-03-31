import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://localhost:5432/mealdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

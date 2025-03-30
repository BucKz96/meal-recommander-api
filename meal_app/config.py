import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://user:password@db:5432/meals")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
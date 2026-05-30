import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL_SYNC",
        "postgresql://user:password@db:5432/fooddiary",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ML_API_URL = os.getenv("ML_API_URL", "http://fastapi:8000")

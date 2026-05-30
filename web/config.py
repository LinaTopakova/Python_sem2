import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ML_API_URL = os.getenv("ML_API_URL", "http://localhost:8000")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

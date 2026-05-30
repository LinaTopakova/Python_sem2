import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"   # тот же файл, что и для FastAPI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ML_API_URL = os.getenv("ML_API_URL", "http://fastapi:8000")
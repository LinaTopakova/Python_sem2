from fastapi import FastAPI
from infrastructure.db.database import engine
from infrastructure.db.models import Base

from api.routers.predict import router as predict_router

app = FastAPI(title="Food Diary ML API", version="1.0.0")
app.include_router(predict_router, prefix="/api/v1")


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model-info")
async def model_info() -> dict[str, object]:
    return {
        "name": "Kaludi/food-category-classification-v2.0",
        "version": "1.0",
        "feature_types": ["image_base64"],
    }

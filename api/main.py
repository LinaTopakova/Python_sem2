import base64
import logging
from io import BytesIO

from alembic import command
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI
from PIL import Image

from api.routers.predict import router as predict_router

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Food Diary ML API", version="1.0.0")
app.include_router(predict_router, prefix="/api/v1")


def _create_dummy_base64() -> str:
    """Создаёт чёрное изображение 224x224 и возвращает в base64."""
    img = Image.new("RGB", (224, 224), color=(0, 0, 0))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


DUMMY_IMAGE_BASE64 = _create_dummy_base64()


@app.on_event("startup")
async def startup() -> None:
    # Применяем миграции
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Migrations applied successfully")

    # Прогрев модели
    try:
        from infrastructure.ml.food_model import FoodClassifier

        classifier = FoodClassifier()
        classifier.predict(DUMMY_IMAGE_BASE64)
        logger.info("Model warmed up successfully")
    except Exception as e:
        logger.error(f"Model warm-up failed: {e}")


@app.get("/health")
async def health() -> dict[str, str]:
    logger.info("Health check called")
    return {"status": "ok"}


@app.get("/model-info")
async def model_info() -> dict[str, object]:
    return {
        "name": "Kaludi/food-category-classification-v2.0",
        "version": "1.0",
        "feature_types": ["image_base64"],
    }

import base64
import io
from typing import Tuple

import torch
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor


class FoodClassifier:
    def __init__(self, model_name: str = "Kaludi/food-category-classification-v2.0") -> None:
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.model = ViTForImageClassification.from_pretrained(model_name)

    def predict(self, image_base64: str) -> Tuple[str, float]:
        """Возвращает (название блюда, уверенность)."""
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        predicted_label = self.model.config.id2label[predicted_class_idx]
        confidence = torch.softmax(logits, dim=-1)[0, predicted_class_idx].item()
        return predicted_label, confidence

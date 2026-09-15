"""
Gesture classification.

TODO: once recordings/processed/ has labeled sessions, replace this with
model/training.py output (joblib.load(settings.MODEL_PATH)) without changing
the predict() interface, so orchestrator.py doesn't need to change.
"""

from config import settings


class GestureClassifier:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        self.model_path = model_path
        self.model = None  # will hold the trained model once available

    def load(self):
        """No-op for now (placeholder classifier needs no trained model)."""
        pass

    def predict(self, feature_vector: dict) -> dict:
        mav = feature_vector.get("mav", 0.0)

        if mav >= settings.MAV_ACTIVATION_THRESHOLD:
            confidence = min(1.0, mav / (settings.MAV_ACTIVATION_THRESHOLD * 2))
            return {"gesture": "contract", "confidence": round(confidence, 2)}

        return {"gesture": "rest", "confidence": 1.0}
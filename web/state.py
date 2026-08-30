import time
from config import settings

# Estado inicial: todos los servos en reposo, sin gesto detectado
current_state = {
    "timestamp": time.time(),
    "gesture": "rest",
    "servos": {channel: 0 for channel in settings.SERVO_CHANNELS},
    "emg_raw": 0,
    "confidence": 0.0,
}


def update_state(new_data: dict):
    """Merges new_data into current_state and refreshes the timestamp."""
    current_state.update(new_data)
    current_state["timestamp"] = time.time()
    return current_state


def get_state():
    return current_state
from fastapi import APIRouter
from config import settings
from web.state import get_state, update_state
from web import websocket_server

router = APIRouter(prefix="/api")


@router.get("/state")
def read_state():
    """Returns the latest known hand/arm state."""
    return get_state()


@router.get("/servos")
def list_servos():
    """Returns the list of servo channels this project controls."""
    return {"channels": settings.SERVO_CHANNELS}


@router.post("/state")
async def write_state(new_state: dict):
    """
    Manually inject a state (for testing without hardware).
    Example body:
    {
        "gesture": "pinch",
        "servos": {"elbow": 45, "gripper": 90},
        "emg_raw": 512,
        "confidence": 0.87
    }
    """
    updated = update_state(new_state)
    await websocket_server.broadcast(updated)
    return updated
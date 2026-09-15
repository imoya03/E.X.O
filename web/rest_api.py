"""
Read-only info endpoints for the website. No longer connects to the
Arduino directly - keyboard_control.py now owns that connection
exclusively, to avoid two processes fighting over the same COM port.
"""

from fastapi import APIRouter
from config import settings
from web.state import get_state

router = APIRouter(prefix="/api")


@router.get("/state")
def read_state():
    """Returns the latest known hand/arm state (informational only)."""
    return get_state()


@router.get("/servos")
def list_servos():
    """Returns the list of servo channels this project controls."""
    return {"channels": settings.SERVO_CHANNELS}
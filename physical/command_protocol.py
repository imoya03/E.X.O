"""
Defines the TEXT-based message format expected by the tested Arduino sketch
(Serial.parseInt() reading 6 comma-separated integers, no start byte, no checksum
-- this firmware has no built-in error detection).

Frame layout: "v0,v1,v2,v3,v4,v5\n"
Order matches SERVO_CHANNELS dict order exactly: root, arm_a, wrist_b, wrist_a, arm_b, gripper
"""

from config import settings


def resolve_full_angles(active_values: dict) -> dict:
    """Returns a dict with ALL servo channels resolved to a final angle."""
    resolved = {}
    for name, cfg in settings.SERVO_CHANNELS.items():
        if cfg["active"] and name in active_values:
            angle = active_values[name]
        else:
            angle = cfg["rest_angle"]
        resolved[name] = max(0, min(180, int(angle)))
    return resolved


def encode(state: dict) -> bytes:
    """Builds the plain-text comma-separated frame the Arduino expects."""
    active_values = state.get("servos", {})
    resolved = resolve_full_angles(active_values)

    values = [str(resolved[name]) for name in settings.SERVO_CHANNELS.keys()]
    frame = ",".join(values) + "\n"

    return frame.encode("ascii")
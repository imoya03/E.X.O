"""
Offline validation of physical/command_protocol.py - no Arduino needed.
Confirms resolve_full_angles() and encode() behave correctly with the
current channel set and the plain-text protocol format.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physical import command_protocol
from config import settings

print("=== Test 1: Rest state (no servos dict) ===")
resolved = command_protocol.resolve_full_angles({})
print(f"Resolved: {resolved}")
assert resolved["root"] == 90
assert resolved["arm_a1"] == 90
assert resolved["wrist_b"] == 90
assert resolved["wrist_a"] == 94  # recalibrated center
assert resolved["arm_b"] == 90
assert resolved["gripper"] == 0

frame = command_protocol.encode({})
print(f"Encoded frame: {frame}")
assert frame == b"90,90,90,94,90,0\n"
print("PASS\n")

print("=== Test 2: Active state (wrist_a=120, gripper=180) ===")
resolved = command_protocol.resolve_full_angles({"wrist_a": 120, "gripper": 180})
print(f"Resolved: {resolved}")
assert resolved["wrist_a"] == 120
assert resolved["gripper"] == 180
assert resolved["root"] == 90  # untouched channels stay at rest

frame = command_protocol.encode({"servos": {"wrist_a": 120, "gripper": 180}})
print(f"Encoded frame: {frame}")
assert frame == b"90,90,90,120,90,180\n"
print("PASS\n")

print("=== Test 3: Out-of-range values get clamped ===")
resolved = command_protocol.resolve_full_angles({"wrist_a": 999, "gripper": -50})
print(f"Resolved: {resolved}")
assert resolved["wrist_a"] == 180
assert resolved["gripper"] == 0
print("PASS\n")

print("=== Test 4: Channel order matches SERVO_CHANNELS dict order ===")
expected_order = list(settings.SERVO_CHANNELS.keys())
print(f"Expected order: {expected_order}")
assert expected_order == ["root", "arm_a1", "wrist_b", "wrist_a", "arm_b", "gripper"]
print("PASS\n")

print("All protocol tests passed.")
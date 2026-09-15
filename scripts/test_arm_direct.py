"""
Minimal direct test: bypasses FastAPI/REST entirely. Sends one fixed frame
straight to the Arduino to confirm the wiring + protocol work in isolation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from physical.servo_control import ServoController

controller = ServoController()
print("Connecting (waiting for Arduino auto-reset)...")
controller.connect()
print("Connected. Sending test position...")

controller.send_state({"servos": {"wrist_a": 45, "wrist_b": 135, "gripper": 180}})
time.sleep(2)

print("Sending rest position...")
controller.send_state({"servos": {}})  # all channels fall back to rest_angle

controller.close()
print("Done.")
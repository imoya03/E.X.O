"""
Direct hardware test: sends a few known positions to Arduino 2 via
ServoController, using the current channel names. Useful for a quick
sanity check without needing keyboard_control.py or gamepad_control.py.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from physical.servo_control import ServoController

controller = ServoController()
print("Connecting (waiting for Arduino auto-reset)...")
controller.connect()
print("Connected.\n")

print("Sending rest position (all channels at their rest_angle)...")
controller.send_state({"servos": {}})
time.sleep(2)

print("Sending test position: wrist_a=120, wrist_b=60, gripper=180...")
controller.send_state({"servos": {"wrist_a": 120, "wrist_b": 60, "gripper": 180}})
time.sleep(2)

print("Sending test position: root=45, arm_a1=135, arm_b=45...")
controller.send_state({"servos": {"root": 45, "arm_a1": 135, "arm_b": 45}})
time.sleep(2)

print("Back to rest...")
controller.send_state({"servos": {}})
time.sleep(1)

controller.close()
print("\nDone.")
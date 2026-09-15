"""
Diagnostic tool: moves ONE servo channel at a time to a distinct test
angle, while all others stay at rest (90), so you can visually confirm
which physical joint corresponds to which channel name.

Watch the arm as each channel is announced, and note which joint moves
(or if none moves at all).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from config import settings
from physical.servo_control import ServoController

TEST_ANGLE = 45  # far enough from 90 (rest) to be obviously visible
HOLD_SECONDS = 3

controller = ServoController()
print("Connecting (waiting for Arduino auto-reset)...")
controller.connect()
print("Connected.\n")

channel_names = list(settings.SERVO_CHANNELS.keys())

# Start everyone at rest
rest_state = {name: settings.SERVO_CHANNELS[name]["rest_angle"] for name in channel_names}
controller.send_state({"servos": rest_state})
time.sleep(1)

for name in channel_names:
    print(f"\n>>> Testing channel: '{name}' (pin {settings.SERVO_CHANNELS[name]['pin']}) -> moving to {TEST_ANGLE}")
    test_state = dict(rest_state)
    test_state[name] = TEST_ANGLE
    controller.send_state({"servos": test_state})

    input("    Watch the arm, then press Enter to continue to the next channel...")

    controller.send_state({"servos": rest_state})
    time.sleep(0.5)

controller.close()
print("\nDone.")
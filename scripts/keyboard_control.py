"""
Standalone manual control of the physical arm via keyboard - talks
directly to Arduino 2 over serial, no FastAPI/HTTP involved.

Controls:
  Up / Down     -> wrist_b
  Left / Right  -> wrist_a
  W / S         -> arm_a1
  A / D         -> root
  Q / E         -> arm_b
  Space         -> toggle gripper (open/closed)
  U             -> macro: Home (rest position)
  I             -> macro: Pick (reach forward, gripper open)
  O             -> macro: Wave (animated greeting)
  P             -> macro: Full open (centered, gripper open)
  Esc           -> quit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import keyboard
from physical.servo_control import ServoController

STEP = 1

state = {
    "root": 90,
    "arm_a1": 90,
    "wrist_b": 90,
    "wrist_a": 94,
    "arm_b": 90,
    "gripper": 0,
}
gripper_open = False

controller = ServoController()

MACROS = {
    "home":      {"root": 90, "arm_a1": 90, "wrist_b": 90, "wrist_a": 94, "arm_b": 90, "gripper": 0},
    "pick":      {"root": 90, "arm_a1": 60, "wrist_b": 90, "wrist_a": 94, "arm_b": 120, "gripper": 180},
    "full_open": {"root": 90, "arm_a1": 90, "wrist_b": 90, "wrist_a": 94, "arm_b": 90, "gripper": 180},
}


def clamp(value):
    return max(0, min(180, value))


def send_state():
    try:
        controller.send_state({"servos": state})
        print(f"\rroot={state['root']:>3}  arm_a1={state['arm_a1']:>3}  "
              f"arm_b={state['arm_b']:>3}  wrist_a={state['wrist_a']:>3}  "
              f"wrist_b={state['wrist_b']:>3}  "
              f"gripper={'OPEN' if gripper_open else 'CLOSED':>6}", end="")
    except Exception as e:
        print(f"\nLost connection to Arduino: {e}")


def adjust(channel, delta):
    state[channel] = clamp(state[channel] + delta)
    send_state()


def toggle_gripper():
    global gripper_open
    gripper_open = not gripper_open
    state["gripper"] = 180 if gripper_open else 0
    send_state()


def run_macro(name):
    global gripper_open
    print(f"\nRunning macro: {name}")
    preset = MACROS[name]
    state.update(preset)
    gripper_open = state["gripper"] > 90
    send_state()


def run_wave_macro():
    """Animated example macro: waves the wrist back and forth a few times."""
    print("\nRunning macro: wave")
    run_macro("home")
    time.sleep(0.5)

    for _ in range(3):
        state["wrist_a"] = 60
        send_state()
        time.sleep(0.3)
        state["wrist_a"] = 120
        send_state()
        time.sleep(0.3)

    state["wrist_a"] = 90
    send_state()


def main():
    print("Connecting to Arduino (waiting for auto-reset)...")
    controller.connect()
    print("Connected.\n")
    print("Arrows: wrist_b (up/down) / wrist_a (left/right)")
    print("W/S: arm_a1 | A/D: root | Q/E: arm_b | Space: gripper")
    print("U: Home | I: Pick | O: Wave | P: Full open | Esc: quit\n")

    keyboard.on_press_key("up", lambda _: adjust("wrist_b", STEP))
    keyboard.on_press_key("down", lambda _: adjust("wrist_b", -STEP))
    keyboard.on_press_key("right", lambda _: adjust("wrist_a", STEP))
    keyboard.on_press_key("left", lambda _: adjust("wrist_a", -STEP))

    keyboard.on_press_key("w", lambda _: adjust("arm_a1", STEP))
    keyboard.on_press_key("s", lambda _: adjust("arm_a1", -STEP))
    keyboard.on_press_key("a", lambda _: adjust("root", -STEP))
    keyboard.on_press_key("d", lambda _: adjust("root", STEP))
    keyboard.on_press_key("q", lambda _: adjust("arm_b", -STEP))
    keyboard.on_press_key("e", lambda _: adjust("arm_b", STEP))

    keyboard.on_press_key("space", lambda _: toggle_gripper())

    keyboard.on_press_key("u", lambda _: run_macro("home"))
    keyboard.on_press_key("i", lambda _: run_macro("pick"))
    keyboard.on_press_key("o", lambda _: run_wave_macro())
    keyboard.on_press_key("p", lambda _: run_macro("full_open"))

    send_state()  # send initial rest state
    keyboard.wait("esc")

    print("\nExiting.")
    controller.close()


if __name__ == "__main__":
    main()
"""
DualSense (PS5) control via Bluetooth - RATE-based control: pushing a
stick or trigger moves the corresponding servo continuously in that
direction (faster with more deflection); releasing back to center
HOLDS the current position instead of springing back to rest.

Controls:
  Left stick  -> X: root, Y: arm_a1 (rate control)
  Right stick -> X: wrist_a, Y: wrist_b (rate control)
  L2 / R2     -> arm_b (L2 decreases, R2 increases, rate control)
  Cross (X)   -> toggle gripper
  Triangle    -> macro: Home
  Circle      -> macro: Pick
  Square      -> macro: Wave
  L1          -> macro: Full open
  Down        -> macro: Wave in place
  Options     -> quit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import threading
import pygame
from physical.servo_control import ServoController

TICK_INTERVAL = 0.05        # 20Hz - both the control loop and the serial sender
DEADZONE = 0.15             # ignore small stick drift near center
RATE_DEG_PER_SEC = 90       # servo speed at full stick/trigger deflection

state = {
    "root": 90, "arm_a1": 90,
    "wrist_a": 94,  # recalibrated center - servo sits slightly crooked at 90
    "wrist_b": 90,
    "arm_b": 90, "gripper": 0,
}
gripper_open = False
state_lock = threading.Lock()
last_sent_state = None
stop_event = threading.Event()

# Raw axis values as last reported by the gamepad (idle defaults: sticks
# centered at 0, triggers unpressed at -1, matching SDL's DualSense mapping)
axis_state = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: -1.0, 5: -1.0}
axis_lock = threading.Lock()

controller = ServoController()

MACROS = {
    "home":      {"root": 90, "arm_a1": 90, "wrist_b": 90, "wrist_a": 94, "arm_b": 90, "gripper": 0},
    "pick":      {"root": 90, "arm_a1": 60, "wrist_b": 90, "wrist_a": 94, "arm_b": 120, "gripper": 180},
    "full_open": {"root": 90, "arm_a1": 90, "wrist_b": 90, "wrist_a": 94, "arm_b": 90, "gripper": 180},
}


def clamp(value):
    return max(0, min(180, value))


def apply_deadzone(value, threshold=DEADZONE):
    return 0.0 if abs(value) < threshold else value


def print_status():
    print(f"\rroot={state['root']:>5.1f}  arm_a1={state['arm_a1']:>5.1f}  "
          f"arm_b={state['arm_b']:>5.1f}  wrist_a={state['wrist_a']:>5.1f}  "
          f"wrist_b={state['wrist_b']:>5.1f}  "
          f"gripper={'OPEN' if gripper_open else 'CLOSED':>6}", end="")


def toggle_gripper():
    global gripper_open
    with state_lock:
        gripper_open = not gripper_open
        state["gripper"] = 180 if gripper_open else 0


def run_macro(name):
    global gripper_open
    print(f"\nRunning macro: {name}")
    with state_lock:
        state.update(MACROS[name])
        gripper_open = state["gripper"] > 90


def run_wave_macro():
    print("\nRunning macro: wave")
    run_macro("home")
    time.sleep(0.5)
    for _ in range(3):
        with state_lock:
            state["wrist_a"] = 60
        time.sleep(0.3)
        with state_lock:
            state["wrist_a"] = 130
        time.sleep(0.3)
    with state_lock:
        state["wrist_a"] = 94

def run_wave_in_place():
    """
    Waves the wrist WITHOUT returning home first - keeps whatever position
    the arm is currently in, oscillates wrist_a around its current value,
    then restores it back to that exact value when done.
    """
    print("\nRunning macro: wave in place")

    with state_lock:
        original_wrist_a = state["wrist_a"]

    swing = 30  # degrees to swing on each side of the current position

    for _ in range(3):
        with state_lock:
            state["wrist_a"] = clamp(original_wrist_a - swing)
        time.sleep(0.3)
        with state_lock:
            state["wrist_a"] = clamp(original_wrist_a + swing)
        time.sleep(0.3)

    with state_lock:
        state["wrist_a"] = original_wrist_a

def control_loop():
    """
    Runs at a fixed rate: reads current raw axis positions and nudges
    each servo's angle continuously while a stick/trigger is deflected.
    Releasing back to center simply stops the nudging - the servo holds
    wherever it last was (no spring-back to a rest angle).
    """
    max_step = RATE_DEG_PER_SEC * TICK_INTERVAL  # max degrees moved per tick at full deflection

    while not stop_event.is_set():
        with axis_lock:
            left_x = apply_deadzone(axis_state[0])
            left_y = apply_deadzone(axis_state[1])
            right_x = apply_deadzone(axis_state[2])
            right_y = apply_deadzone(axis_state[3])
            l2_raw = axis_state[4]
            r2_raw = axis_state[5]

        # Normalize triggers from [-1 (released), 1 (pressed)] to [0, 1]
        l2_norm = (l2_raw + 1) / 2
        r2_norm = (r2_raw + 1) / 2
        trigger_delta = apply_deadzone(r2_norm - l2_norm, threshold=0.05)

        changed = any([left_x, left_y, right_x, right_y, trigger_delta])

        if changed:
            with state_lock:
                state["root"] = clamp(state["root"] + left_x * max_step)
                state["arm_a1"] = clamp(state["arm_a1"] + left_y * max_step)
                state["wrist_a"] = clamp(state["wrist_a"] + right_x * max_step)
                state["wrist_b"] = clamp(state["wrist_b"] + right_y * max_step)
                state["arm_b"] = clamp(state["arm_b"] + trigger_delta * max_step)
            print_status()

        time.sleep(TICK_INTERVAL)


def sender_loop():
    global last_sent_state
    while not stop_event.is_set():
        with state_lock:
            current = {k: round(v) for k, v in state.items()}
        if current != last_sent_state:
            try:
                controller.send_state({"servos": current})
                last_sent_state = current
            except Exception as e:
                print(f"\nLost connection to Arduino: {e}")
        time.sleep(TICK_INTERVAL)


def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No gamepad detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Detected: {joystick.get_name()}")

    print("Connecting to Arduino (waiting for auto-reset)...")
    controller.connect()
    print("Connected.\n")
    print("Left stick: root/arm_a1 | Right stick: wrist_a/wrist_b | L2: arm_b down | R2: arm_b up")
    print("Cross: gripper | Triangle: Home | Circle: Pick | Square: Wave | L1: Full open")
    print("Options: quit\n")

    control_thread = threading.Thread(target=control_loop, daemon=True)
    sender_thread = threading.Thread(target=sender_loop, daemon=True)
    control_thread.start()
    sender_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                with axis_lock:
                    axis_state[event.axis] = event.value

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:      # Cross
                    toggle_gripper()
                elif event.button == 3:    # Triangle
                    run_macro("home")
                elif event.button == 1:    # Circle
                    run_macro("pick")
                elif event.button == 2:    # Square
                    run_wave_macro()
                elif event.button == 9:    # L1
                    run_macro("full_open")
                elif event.button == 12:    # DOWN
                    run_wave_in_place()
                elif event.button == 6:    # Options
                    running = False
                print_status()

        time.sleep(0.01)

    stop_event.set()
    control_thread.join(timeout=1)
    sender_thread.join(timeout=1)
    controller.close()
    pygame.quit()
    print("\nExiting.")


if __name__ == "__main__":
    main()
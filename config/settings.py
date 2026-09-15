"""
Central configuration for the EXO project.
Keep hardware/tunable values here instead of hardcoding them across modules.
"""

# --- Serial communication: Arduino 1 (EMG) ---
ARDUINO_EMG_PORT = "COM6"         # TODO: update with real COM port when connected
ARDUINO_EMG_BAUDRATE = 115200

# --- Serial communication: Arduino 2 (servos) ---
ARDUINO_SERVO_PORT = "COM9"       # TODO: update with real COM port when connected
ARDUINO_SERVO_BAUDRATE = 9600

# --- Signal acquisition ---
SAMPLING_RATE_HZ = 1000

# --- Filtering ---
BANDPASS_LOW_HZ = 20
BANDPASS_HIGH_HZ = 450
NOTCH_FREQ_HZ = 60
NOTCH_QUALITY_FACTOR = 30

# --- Windowing for feature extraction ---
WINDOW_SIZE_MS = 200
WINDOW_OVERLAP_MS = 50
WINDOW_SIZE_SAMPLES = int(SAMPLING_RATE_HZ * WINDOW_SIZE_MS / 1000)
WINDOW_STEP_MS = WINDOW_SIZE_MS - WINDOW_OVERLAP_MS

# --- Classification (placeholder threshold-based, until a real model is trained) ---
MAV_ACTIVATION_THRESHOLD = 0.5   # TODO: calibrate once real EMG signal is available
MODEL_PATH = "model/saved_models/gesture_classifier.pkl"
CONFIDENCE_THRESHOLD = 0.6

# --- Servo channels---
# All channels are individually controllable now that keyboard_control.py
# drives the arm directly (no EMG-vs-fixed distinction needed anymore).
SERVO_CHANNELS = {
    "root":     {"pin": 3,  "active": True, "rest_angle": 90},
    "arm_a1":   {"pin": 4,  "active": True, "rest_angle": 90},
    "wrist_b":  {"pin": 6,  "active": True, "rest_angle": 90},
    "wrist_a":  {"pin": 9,  "active": True, "rest_angle": 94},
    "arm_b":    {"pin": 10, "active": True, "rest_angle": 90},
    "gripper":  {"pin": 11, "active": True, "rest_angle": 0},
}

# --- Orchestrator ---
ENABLE_ORCHESTRATOR = False   # set False to run the web server alone, without the processing loop

# --- Web server ---
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8000
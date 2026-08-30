"""
Central configuration for the EXO project.
Keep hardware/tunable values here instead of hardcoding them across modules.
"""

# --- Serial communication ---
ARDUINO_EMG_PORT = "COM5"       # Arduino COM Port - AD8226 EMG acquisition
ARDUINO_EMG_BAUDRATE = 115200

# --- Signal acquisition ---
SAMPLING_RATE_HZ = 1000         # Target EMG sampling rate

# --- Filtering ---
BANDPASS_LOW_HZ = 20
BANDPASS_HIGH_HZ = 450
NOTCH_FREQ_HZ = 60              # Country mains frequency
NOTCH_QUALITY_FACTOR = 30

# --- Windowing for feature extraction ---
WINDOW_SIZE_MS = 200
WINDOW_OVERLAP_MS = 50

# --- Servo channels ---
SERVO_CHANNELS = ["elbow", "gripper"]

# --- Web server ---
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8000
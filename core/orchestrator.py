"""
Main orchestrator loop.

Pipeline:
1. Background thread reads EMG samples continuously into a circular buffer.
2. Async loop, every WINDOW_STEP_MS: grabs the latest window, filters it,
   extracts features, classifies the gesture.
3. Builds the resulting state dict and:
   a. Sends it to Arduino 2 (servos), if connected.
   b. Broadcasts it to WebSocket clients (digital twin / web viewer).

Designed to degrade gracefully: if either Arduino isn't connected, the
orchestrator logs a warning and keeps running instead of crashing the
whole app (so the web server stays usable during hardware bring-up).
"""

import asyncio
import threading
import time
from physical import command_protocol

from config import settings
from data.serial_acquisition import EMGSerialReader
from data.circular_buffer import CircularBuffer
from data import filters, features
from data.classifier import GestureClassifier
from physical.servo_control import ServoController
from web import websocket_server
from web.state import update_state


class Orchestrator:
    def __init__(self):
        self.reader = EMGSerialReader()
        self.buffer = CircularBuffer(max_samples=settings.SAMPLING_RATE_HZ * 2)  # 2s of history
        self.classifier = GestureClassifier()
        self.servo_controller = ServoController()

        self.emg_connected = False
        self.servo_connected = False
        self._stop_event = threading.Event()

    def _acquisition_loop(self):
        """Runs in a background thread, continuously pushing EMG samples into the buffer."""
        while not self._stop_event.is_set():
            sample = self.reader.read_sample()
            if sample is not None:
                self.buffer.push(sample)

    def _start_acquisition_thread(self):
        thread = threading.Thread(target=self._acquisition_loop, daemon=True)
        thread.start()

    async def run(self):
        # --- Connect to Arduino 1 (EMG) ---
        try:
            self.reader.connect()
            self.emg_connected = True
            self._start_acquisition_thread()
            print("[Orchestrator] EMG Arduino connected.")
        except Exception as e:
            print(f"[Orchestrator] WARNING: could not connect to EMG Arduino ({e}). "
                  f"Processing loop will idle until it's available.")

        # --- Connect to Arduino 2 (servos) ---
        try:
            self.servo_controller.connect()
            self.servo_connected = True
            print("[Orchestrator] Servo Arduino connected.")
        except Exception as e:
            print(f"[Orchestrator] WARNING: could not connect to servo Arduino ({e}). "
                  f"Computed states will still broadcast to the web, but won't drive servos.")

        self.classifier.load()

        window_step_seconds = settings.WINDOW_STEP_MS / 1000

        while True:
            await asyncio.sleep(window_step_seconds)

            if not self.emg_connected:
                continue  # nothing to process yet

            window = self.buffer.get_window(settings.WINDOW_SIZE_SAMPLES)
            if len(window) < settings.WINDOW_SIZE_SAMPLES:
                continue  # not enough samples buffered yet

            filtered = filters.apply_all_filters(window)
            feature_vector = features.extract_all(filtered)
            classification = self.classifier.predict(feature_vector)
            active_angles = self._gesture_to_servo_angles(classification["gesture"])
            full_servo_state = command_protocol.resolve_full_angles(active_angles)

            state = {
                "gesture": classification["gesture"],
                "confidence": classification["confidence"],
                "emg_raw": window[-1],
                "servos": full_servo_state,  # all 7 channels, so the web can render the whole arm
            }

            update_state(state)

            if self.servo_connected:
                try:
                    self.servo_controller.send_state(state)
                except Exception as e:
                    print(f"[Orchestrator] WARNING: lost connection to servo Arduino ({e}).")
                    self.servo_connected = False

            await websocket_server.broadcast(state)

    @staticmethod
    def _gesture_to_servo_angles(gesture: str) -> dict:
        """
        Maps a classified gesture to target angles for the EMG-active servos.
        TODO: refine once real gestures/classes are defined with a trained model.
        """
        if gesture == "contract":
            return {"elbow": 45, "gripper_left": 90}
        return {"elbow": 90, "gripper_left": 0}
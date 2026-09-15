import serial
import time
from config import settings
from physical import command_protocol


class ServoController:
    def __init__(self, port: str = settings.ARDUINO_SERVO_PORT,
                 baudrate: int = settings.ARDUINO_SERVO_BAUDRATE):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
        time.sleep(2)  # let the Arduino finish its auto-reset before sending data

    def send_state(self, state: dict):
        frame = command_protocol.encode(state)
        self.connection.write(frame)

    def close(self):
        if self.connection:
            self.connection.close()
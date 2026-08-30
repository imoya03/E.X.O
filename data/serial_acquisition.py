import serial
from config import settings

START_BYTE = 0xAA


class EMGSerialReader:
    def __init__(self, port: str = settings.ARDUINO_EMG_PORT,
                 baudrate: int = settings.ARDUINO_EMG_BAUDRATE):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudrate, timeout=1)

    def read_sample(self):
        """Reads one EMG sample (0-1023). Returns None if frame is invalid/timeout."""
        byte = self.connection.read(1)
        if not byte or byte[0] != START_BYTE:
            return None

        payload = self.connection.read(3)
        if len(payload) < 3:
            return None

        high_byte, low_byte, checksum = payload[0], payload[1], payload[2]

        if (high_byte ^ low_byte) != checksum:
            return None  # frame corrupto, se descarta

        return (high_byte << 8) | low_byte

    def close(self):
        if self.connection:
            self.connection.close()
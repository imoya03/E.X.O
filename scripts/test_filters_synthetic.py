import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from data.serial_acquisition import EMGSerialReader
from config import settings

WINDOW_SECONDS = 5
buffer_size = settings.SAMPLING_RATE_HZ * WINDOW_SECONDS
data_buffer = deque([0] * buffer_size, maxlen=buffer_size)

reader = EMGSerialReader()
reader.connect()

fig, ax = plt.subplots()
line, = ax.plot(data_buffer)
ax.set_ylim(0, 1023)
ax.set_title("Raw EMG Signal (AD8226)")
ax.set_xlabel("Samples")
ax.set_ylabel("ADC value (0-1023)")


def update(frame):
    for _ in range(10):
        value = reader.read_sample()
        if value is not None:
            data_buffer.append(value)
    line.set_ydata(data_buffer)
    return line,


ani = animation.FuncAnimation(fig, update, interval=30, blit=True)

try:
    plt.show()
finally:
    reader.close()
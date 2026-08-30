from collections import deque


class CircularBuffer:
    """
    Fixed-size buffer for real-time EMG samples.
    The acquisition thread pushes samples continuously; the processing
    loop pulls fixed-size windows without blocking either side.
    """

    def __init__(self, max_samples: int):
        self.max_samples = max_samples
        self._data = deque(maxlen=max_samples)

    def push(self, sample):
        self._data.append(sample)

    def get_window(self, n_samples: int):
        """Returns the last n_samples as a list. If not enough samples yet, returns what's available."""
        if n_samples >= len(self._data):
            return list(self._data)
        return list(self._data)[-n_samples:]

    def is_full(self):
        return len(self._data) == self.max_samples

    def __len__(self):
        return len(self._data)
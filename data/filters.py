import numpy as np
from scipy import signal
from config import settings


def bandpass_filter(data, fs: int = settings.SAMPLING_RATE_HZ,
                     low: float = settings.BANDPASS_LOW_HZ,
                     high: float = settings.BANDPASS_HIGH_HZ,
                     order: int = 4):
    """Applies a zero-phase Butterworth bandpass filter to a full signal array."""
    nyquist = fs / 2
    low_norm = low / nyquist
    high_norm = high / nyquist

    sos = signal.butter(order, [low_norm, high_norm], btype="band", output="sos")
    filtered = signal.sosfiltfilt(sos, data)
    return filtered


def notch_filter(data, fs: int = settings.SAMPLING_RATE_HZ,
                  freq: float = settings.NOTCH_FREQ_HZ,
                  quality_factor: float = settings.NOTCH_QUALITY_FACTOR):
    """Applies a zero-phase notch filter at the mains frequency (60Hz)."""
    nyquist = fs / 2
    freq_norm = freq / nyquist

    b, a = signal.iirnotch(freq_norm, quality_factor)
    filtered = signal.filtfilt(b, a, data)
    return filtered


def apply_all_filters(data):
    """Convenience function: bandpass + notch in sequence."""
    data = bandpass_filter(data)
    data = notch_filter(data)
    return data
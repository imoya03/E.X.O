"""
Classic EMG feature extraction, computed per analysis window.

Features:
- RMS  (Root Mean Square)         -> signal energy
- MAV  (Mean Absolute Value)      -> signal amplitude
- ZC   (Zero Crossings)           -> frequency-related activity
- WL   (Waveform Length)          -> signal complexity
"""

import numpy as np


def rms(window: np.ndarray) -> float:
    """Root Mean Square - reflects signal energy/effort level."""
    window = np.asarray(window, dtype=float)
    return float(np.sqrt(np.mean(window ** 2)))


def mav(window: np.ndarray) -> float:
    """Mean Absolute Value - reflects signal amplitude."""
    window = np.asarray(window, dtype=float)
    return float(np.mean(np.abs(window)))


def zero_crossings(window: np.ndarray, threshold: float = 0.0) -> int:
    """
    Counts how many times the signal crosses zero (or a small threshold
    to avoid counting noise-driven crossings near zero).
    """
    window = np.asarray(window, dtype=float)
    signs = np.sign(window)
    signs[signs == 0] = 1  # avoid zero breaking the sign comparison

    crossings = 0
    for i in range(len(window) - 1):
        if signs[i] != signs[i + 1] and abs(window[i] - window[i + 1]) > threshold:
            crossings += 1

    return crossings


def waveform_length(window: np.ndarray) -> float:
    """Cumulative length of the waveform - reflects signal complexity."""
    window = np.asarray(window, dtype=float)
    return float(np.sum(np.abs(np.diff(window))))


def extract_all(window: np.ndarray) -> dict:
    """Returns all four features for a given window, ready for the classifier."""
    return {
        "rms": rms(window),
        "mav": mav(window),
        "zc": zero_crossings(window),
        "wl": waveform_length(window),
    }
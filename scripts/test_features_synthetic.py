import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from data.filters import apply_all_filters
from data.features import extract_all
from config import settings

fs = settings.SAMPLING_RATE_HZ

np.random.seed(1)
rest_window = np.random.normal(0, 0.2, int(fs * 0.2))  # 200ms, baja amplitud

contraction_window = np.random.normal(0, 2.0, int(fs * 0.2))  # 200ms, alta amplitud

rest_filtered = apply_all_filters(rest_window)
contraction_filtered = apply_all_filters(contraction_window)

rest_features = extract_all(rest_filtered)
contraction_features = extract_all(contraction_filtered)

print("=== REST window features ===")
for name, value in rest_features.items():
    print(f"{name.upper():>4}: {value:.4f}")

print("\n=== CONTRACTION window features ===")
for name, value in contraction_features.items():
    print(f"{name.upper():>4}: {value:.4f}")

print("\n=== Ratio (contraction / rest) ===")
for name in rest_features:
    ratio = contraction_features[name] / (rest_features[name] + 1e-9)
    print(f"{name.upper():>4}: {ratio:.2f}x")
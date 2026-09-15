import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from data.serial_acquisition import EMGSerialReader

reader = EMGSerialReader()
reader.connect()

print("Diagnosing for 5 seconds...")
valid = 0
invalid = 0
start = time.time()

while time.time() - start < 5:
    result = reader.read_sample()
    if result is not None:
        valid += 1
    else:
        invalid += 1

reader.close()

total = valid + invalid
print(f"\nValid frames:   {valid}")
print(f"Invalid frames: {invalid}")
print(f"Total attempts: {total}")
print(f"Valid rate: {(valid/total*100):.1f}%" if total > 0 else "No data received at all.")
"""
Diagnostic tool: prints every button/axis/hat event from a connected
gamepad in real time, so we can identify which index corresponds to
which physical control on the controller before wiring up the real
gamepad_control.py mapping.

Press buttons, move sticks, and pull triggers one at a time - watch
the printed indices.
"""

import pygame
import sys

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No gamepad detected. Make sure it's paired/connected, then try again.")
    sys.exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Detected: {joystick.get_name()}")
print(f"Axes: {joystick.get_numaxes()} | Buttons: {joystick.get_numbuttons()} | Hats: {joystick.get_numhats()}")
print("\nPress buttons / move sticks / pull triggers - watching for events (Ctrl+C to quit)...\n")

clock = pygame.time.Clock()

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"BUTTON DOWN -> index {event.button}")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"BUTTON UP   -> index {event.button}")
            elif event.type == pygame.JOYAXISMOTION:
                # Only print meaningful movement to avoid spamming with noise near 0
                if abs(event.value) > 0.15:
                    print(f"AXIS MOTION -> index {event.axis}, value {event.value:.2f}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"HAT (D-pad) -> index {event.hat}, value {event.value}")

        clock.tick(60)
except KeyboardInterrupt:
    print("\nExiting.")
    pygame.quit()
"""Simulated radar: runs the same visualization as radar_serial.py without any
hardware connected, for testing and demonstration.

    python radar_sim.py            # a servo-like sweep over a simulated room
    python radar_sim.py --random   # random measurements at random angles
"""

from __future__ import annotations

import argparse
import math
import random
import sys

import matplotlib.pyplot as plt

from radar import MAX_ANGLE, RadarDisplay

STEP_DELAY = 0.02  # seconds per degree, the same as the Arduino sketch
RANDOM_DELAY = 0.05  # seconds per measurement in --random mode

# The simulated room, in cm, and the objects in it: (first angle, last angle, distance).
ROOM_DEPTH = 120
ROOM_HALF_WIDTH = 90
OBJECTS = [(35, 50, 60), (95, 105, 75), (130, 150, 45)]


def room_distance(angle: int) -> float:
    """Distance an ideal sensor would measure at this angle in the simulated
    room, in cm.

    The sensor stands against one wall of a 120 x 180 cm room, facing into
    it: 0° points along the wall to one side, 90° straight ahead, 180° along
    the wall to the other side. A few objects stand in the room.
    """
    for first, last, distance in OBJECTS:
        if first <= angle <= last:
            return distance

    # Ray from the sensor: x is "ahead", y is "along the wall".
    radians = math.radians(angle)
    ahead, along = math.sin(radians), math.cos(radians)

    hits = []
    if ahead > 1e-9:
        hits.append(ROOM_DEPTH / ahead)  # far wall
    if abs(along) > 1e-9:
        hits.append(ROOM_HALF_WIDTH / abs(along))  # side walls
    return min(hits)


def measure(angle: int) -> float:
    """Simulates one sensor reading: the room distance plus a little noise.
    The HC-SR04 is accurate to a few centimetres and cannot measure below 2 cm."""
    distance = room_distance(angle)
    return max(2, distance + random.uniform(-3, 3))


def sweep_angles():
    """Yields angles in the same order as the Arduino: 0 to 180, then back, forever."""
    while True:
        yield from range(0, MAX_ANGLE + 1)
        yield from range(MAX_ANGLE, -1, -1)


def run_sweep(radar: RadarDisplay) -> None:
    for angle in sweep_angles():
        if not radar.is_open():
            return
        radar.update(angle, measure(angle))
        # Redraw every few degrees; drawing every single step is slower than the sweep.
        if angle % 3 == 0:
            radar.redraw()
        plt.pause(STEP_DELAY)


def run_random(radar: RadarDisplay) -> None:
    while radar.is_open():
        radar.update(random.randint(0, MAX_ANGLE), random.randint(10, 150))
        radar.redraw()
        plt.pause(RANDOM_DELAY)


def main() -> int:
    parser = argparse.ArgumentParser(description="Radar visualization with simulated data.")
    parser.add_argument("--random", action="store_true",
                        help="plot random measurements at random angles instead of a sweep")
    args = parser.parse_args()

    print("Simulating radar data. Close the window or press Ctrl+C to stop.")
    radar = RadarDisplay()
    try:
        if args.random:
            run_random(radar)
        else:
            run_sweep(radar)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())

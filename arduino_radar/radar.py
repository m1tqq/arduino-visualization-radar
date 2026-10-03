"""Shared parts of the radar: parsing measurements and drawing the radar plot.

Used by both radar_serial.py (live data from the Arduino) and radar_sim.py
(simulated data), so both show exactly the same visualization.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

MAX_RANGE = 200  # cm, the outer edge of the plot
MAX_ANGLE = 180  # degrees, the servo sweeps from 0 to MAX_ANGLE


def parse_measurement(line: str) -> tuple[int, float] | None:
    """Parses one "angle,distance" line sent by the Arduino.

    Returns (angle, distance) or None if the line is malformed or the angle is
    outside 0-180. Serial data can arrive partially (e.g. right after the port
    is opened), so invalid lines are expected and simply skipped.
    """
    parts = line.strip().split(",")
    if len(parts) != 2:
        return None

    try:
        angle = int(parts[0])
        distance = float(parts[1])
    except ValueError:
        return None

    if not 0 <= angle <= MAX_ANGLE or distance < 0:
        return None
    return angle, distance


class RadarDisplay:
    """A live polar plot holding the latest distance measured at each angle.

    0° points up and angles grow clockwise, matching the servo's sweep.
    """

    def __init__(self) -> None:
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="polar")
        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        self.ax.set_rlim(0, MAX_RANGE)

        self.angles = np.arange(0, MAX_ANGLE + 1)
        self.distances = np.full(MAX_ANGLE + 1, np.nan)
        (self.line,) = self.ax.plot([], [], lw=2)

    def update(self, angle: int, distance: float) -> None:
        """Stores a measurement. A distance of 0 means "no echo" and leaves a gap."""
        self.distances[angle] = distance if distance > 0 else np.nan

    def redraw(self) -> None:
        self.line.set_data(np.deg2rad(self.angles), self.distances)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def is_open(self) -> bool:
        """False once the user has closed the plot window."""
        return plt.fignum_exists(self.fig.number)

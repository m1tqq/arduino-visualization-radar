import serial
import time
import numpy as np
import matplotlib.pyplot as plt

PORT = "/dev/tty.usbmodem1201"
BAUD = 9600
MAX_RANGE = 200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_rlim(0, MAX_RANGE)

angles = np.arange(0, 181)
distances = np.full(181, np.nan)
line_plot, = ax.plot([], [], lw=2)

def redraw():
    line_plot.set_data(np.deg2rad(angles), distances)
    fig.canvas.draw()
    fig.canvas.flush_events()

try:
    last_draw = time.time()
    while True:
        raw = ser.readline().decode("utf-8", errors="ignore").strip()
        if not raw:
            continue

        parts = raw.split(",")
        if len(parts) != 2:
            continue

        try:
            angle = int(parts[0])
            dist = float(parts[1])
        except ValueError:
            continue

        if 0 <= angle <= 180:
            distances[angle] = dist

        if time.time() - last_draw > 0.05:
            redraw()
            last_draw = time.time()

except KeyboardInterrupt:
    ser.close()

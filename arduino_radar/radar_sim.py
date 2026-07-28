import numpy as np
import matplotlib.pyplot as plt
import random

MAX_RANGE = 200  # max dist na grafiku

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection="polar")

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_rlim(0, MAX_RANGE)

angles = np.arange(0, 181)
distances = np.full(181, np.nan)

line, = ax.plot([], [], lw=2)

while True:
    angle = random.randint(0, 180)
    distance = random.randint(10, 150)

    distances[angle] = distance

    line.set_data(np.deg2rad(angles), distances)
    plt.pause(0.05)
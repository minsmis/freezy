# Import the module
import motion

import numpy as np
import matplotlib.pyplot as plt

# Designate path for DLC (DeepLabCut) coordinates.
# path = 'PATH/OF/DLC/RESULT.csv'
path = './sample_dlc_data.csv'

# Read DLC coordinates
""" This step should be applied flexibly to adequate for your own dataset."""
dlc = motion.extract(path)
x_nose, y_nose = list(map(float, dlc['nose'][1:])), list(map(float, dlc['nose.1'][1:]))

# Make 'route' with coordinates
route = np.array([x_nose, y_nose])

# Smooth route
smoothed_route = motion.smooth_route(route, window_size=15)

# Compute speed
""" Be sure to use the adequate 'fps' and 'pixel_per_cm' for your device. """
speed = motion.compute_speed(smoothed_route, fps=30, pixel_per_cm=30)

# Display example plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
ax1.plot(route[0, 100:200], route[1, 100:200], '-o', label='Original')
ax1.plot(smoothed_route[0, 100:200], smoothed_route[1, 100:200], '-o', label='Smoothed')
ax1.set_title('Example route')
ax1.set_xlabel('X position')
ax1.set_ylabel('Y position')
ax1.legend()
ax2.plot(speed[100:200])
ax2.set_title('Example speed')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Speed (cm/s)')
plt.show()

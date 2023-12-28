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

# Compute speed
""" Be sure to use the adequate 'fps' and 'pixel_for_cm' for your device. """
speed = motion.compute_speed(route, fps=30, pixel_for_cm=30)

# Display example plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
ax1.scatter(route[0, 0:100], route[1, 0:100])
ax1.plot(route[0, 0:100], route[1, 0:100], 'b')
ax1.set_title('Example route')
ax1.set_xlabel('X position')
ax1.set_ylabel('Y position')
ax2.plot(speed[0:100])
ax2.set_title('Example speed')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Speed (cm/s)')
plt.show()

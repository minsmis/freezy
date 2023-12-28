# Import the module
import motion

import numpy as np
import matplotlib.pyplot as plt

# Designate path for DLC (DeepLabCut) coordinates.
# path = 'PATH/OF/DLC/RESULT.csv'
path = '/Users/minseokkim/IdeaProjects/freezy/examples/sample_dlc_data.csv'

# Read DLC coordinates
""" This step should be applied flexibly to adequate for your own dataset."""
dlc = motion.extract(path)
x_nose, y_nose = list(map(float, dlc['nose'][1:])), list(map(float, dlc['nose.1'][1:]))

# Make 'route' with coordinates
route = np.array([x_nose, y_nose])

# Compute speed
""" Be sure to use the adequate 'fps' and 'pixel_for_cm' for your device. """
speed = motion.compute_speed(route, fps=30, pixel_for_cm=30)

# Display speed plot
plt.plot(speed)
plt.title('Result: examples_motion.py')
plt.xlabel('Time (s)')
plt.ylabel('Speed (cm/s)')
plt.show()

# Import the module
import freezy

import numpy as np
import matplotlib.pyplot as plt

# Designate path for DLC (DeepLabCut) coordinates.
# path = 'PATH/OF/DLC/RESULT.csv'
path = './sample_dlc_data.csv'

# Read DLC coordinates
""" This step should be applied flexibly to adequate for your own dataset."""
dlc = freezy.extract(path)
x_nose, y_nose = list(map(float, dlc['nose'][1:])), list(map(float, dlc['nose.1'][1:]))

# Make 'route' with coordinates
route = np.array([x_nose, y_nose])

# Smooth route
smoothed_route = freezy.smooth_route(route, window_size=15)

# Compute speed
""" Be sure to use the adequate 'fps' and 'pixel_per_cm' for your device. """
speed = freezy.compute_speed(smoothed_route, fps=30, pixel_per_cm=30)

# Calculate freezing threshold
""" This threshold is a average speed during the baseline. Care should be taken when applying this value 
because real freezing threshold can be lower then averaged speed. """
freezing_threshold = freezy.compute_freezing_threshold(speed, baseline_duration=120)

# Detect freezing
""" The parameter, freezing_threshold can be assigned manually or average speed during baseline 
computed by 'freezy.compute_freezing_threshold' function. Here, the example assigned manually. """
freeze_or_not = freezy.detect_freezing(speed, freezing_threshold=0.3)

# Calculate freezing ratio for the protocol
""" Baseline (120 s) -> {Tone (30 s) -> ITI (30 s)} for 5 times. """
protocol = [120, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
freezing_ratio = freezy.compute_freezing_ratio(freeze_or_not, protocol)

# Display result
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8))
fig.subplots_adjust(hspace=0.5)
ax1.plot(speed)
ax1.set_title('Example speed')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Speed (cm/s)')
x = [0, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390]
ax2.plot(x, freezing_ratio, '-o')
ax2.set_title('Example freezing ratio')
xtick_labels = ['Baseline', 'T1', 'ITI1', 'T2', 'ITI2', 'T3', 'ITI3', 'T4', 'ITI4', 'T5', 'PL']
ax2.set_xticks(x, xtick_labels)
ax2.set_xlabel('Sessions')
ax2.set_ylim([0, 100])
ax2.set_ylabel('Freezing (%)')
plt.show()

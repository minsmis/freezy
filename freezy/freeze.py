import numpy as np


def compute_speed_distribution(speed):
    # Parameter
    # speed [ndarr, 1D]: Result of 'compute speed'.
    # Return
    # speed_distribution [ndarr, 1D]: Sorted speed. Highest to lowest speed.

    # Sort
    speed_distribution = np.sort(speed, kind='mergesort')[::-1]  # Highest to lowest

    return speed_distribution


def estimate_freezing_threshold(speed_distribution, detection_threshold=0.05):
    # Parameter
    # speed_distribution [ndarr, 1D]: Return of compute_speed_distribution.
    # detection_threshold [float, 0 <= detection_threshold <= 1]: Detection threshold to find freezing threshold from the top.
    # Return
    # freezing_threshold [float]: Estimated freezing threshold.

    # Reset variables
    freezing_threshold = 0

    # Find threshold
    max_speed = np.max(speed_distribution)
    min_speed = np.min(speed_distribution)
    speed_range = max_speed - min_speed
    freezing_threshold = speed_range * detection_threshold

    return freezing_threshold


def detect_freezing(speed, freezing_threshold):
    # Parameter
    # speed [ndarr, 1D]: Result of 'compute_speed'.
    # freezing_threshold [int or float]: A threshold to detect as freeze.
    # Return
    # freeze_or_not [ndarr, 1D (Same length with speed)]: Freezing or not. 0: Not freezing; 1: Freezing.

    # Make freeze_or_not array
    freeze_or_not = np.zeros((len(speed),))

    # Detect freezing
    for idx, spd in enumerate(speed):
        if spd <= freezing_threshold:
            freeze_or_not[idx] = 1
    return freeze_or_not


def compute_freezing_ratio(freeze_or_not, protocol):
    # Parameter
    # freeze_or_not [ndarr, 1D]: Result of 'detect_freezing'.
    # protocol [list or ndarr, 1D, in second]: Duration of each session in the protocol.
    # Return
    # freezing_ratio [ndarr, 1D (Same length with protocol)]: The ratio of freezing during the sessions.

    # Variables
    previous_ptc = 0

    # Declare output
    freezing_ratio = []

    # Compute freezing ratio
    for ptc in protocol:
        temp_session = freeze_or_not[previous_ptc:previous_ptc + ptc]
        freezing_time = np.sum(temp_session)
        freezing_ratio.append(100 * (freezing_time / ptc))
        previous_ptc += ptc  # Update previous protocol duration
    return np.array(freezing_ratio)

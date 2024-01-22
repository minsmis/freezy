import numpy as np


def compute_freezing_threshold(speed, baseline_duration):
    # Parameter
    # speed [ndarr, 1D]: Result of 'compute_speed'.
    # baseline_duration [int or list or ndarr, 1 or 2 elements, in second]: Duration of baseline.
    # Return
    # threshold [int or float, in second]: An average speed to use as freezing threshold.

    # Define baseline
    baseline = []
    if np.size(baseline_duration) == 1:
        if isinstance(baseline_duration, list or np.ndarray):
            # This is for the baseline duration is given as like this form, [120].
            baseline_duration = baseline_duration[0]
        baseline = speed[0:baseline_duration]
    if np.size(baseline_duration) == 2:
        baseline = speed[int(baseline_duration[0]):int(baseline_duration[-1])]
    if np.size(baseline_duration) > 2:
        raise Exception("Check baseline duration, Over the expected length 1~2.")

    # Compute average speed during baseline
    threshold = np.average(baseline)
    return threshold


def compute_speed_distribution(speed):
    # Parameter
    # speed [ndarr, 1D]: Result of 'compute speed'.
    # Return
    # speed_distribution [ndarr, 1D]: Sorted speed. Highest to lowest speed.

    # Sort
    speed_distribution = np.sort(speed, kind='mergesort')[::-1]  # Highest to lowest

    return speed_distribution


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

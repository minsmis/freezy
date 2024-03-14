import numpy as np


def euclidean_distance(pos1, pos2):
    # Parameters
    # pos1, pos2 [ndarr, 2 elements [x, y]]: The position of the mouse body part on the Euclidean plane.

    # Define variable
    x1, y1 = pos1
    x2, y2 = pos2

    # Calculate Euclidean distance
    euc_distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return euc_distance


def binning_distance(distance, fps):
    # Parameter
    # distance [ndarr, 1D]: Result of 'euclidean_distance'.
    # fps [int or float]: Frame per second of video.

    # Binning for 1 sec length
    bin_step = np.arange(fps, len(distance), step=fps)
    binned_distance = np.array_split(distance, bin_step)
    return binned_distance


def speed_per_pixel(binned_distance, fps, pixel_per_cm):
    # Parameter
    # binned_distance [ndarr, 1D]: Result of 'binning_distance'.
    # fps [int or float]: Frame per second of video.
    # pixel_per_cm [int or float]: Pixels for 1 cm.

    # Output
    speed_per_bin = []

    # Compute speed per bin by pixels
    for distance_bin in binned_distance:
        if len(distance_bin) <= fps:
            sum_distance = np.sum(distance_bin)
            speed = (sum_distance / pixel_per_cm)
            speed_per_bin.append(speed)
        if len(distance_bin) > fps:
            raise Exception("The size of bin is exceeded fps. Check the 'binned_distance'.")
    return np.array(speed_per_bin)


def compute_speed(route, fps=30, pixel_per_cm=30):
    # Parameters
    # route [list or ndarr, 2D, [x, y]]: Route of movement.
    # fps [int or float, Default=30 fps]: Frame per second of video.
    # pixel_per_cm [int, Default=30 pixels]: Pixels for 1 cm.

    # Define position
    x, y = route
    pos1 = np.array([x[:-1], y[:-1]])
    pos2 = np.array([x[1:], y[1:]])

    # Compute distance
    distance = euclidean_distance(pos1, pos2)

    # Binning distance
    binned_distance = binning_distance(distance, int(fps))

    # Compute speed
    speed_per_bin = speed_per_pixel(binned_distance, int(fps), pixel_per_cm)

    return speed_per_bin

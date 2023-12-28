import numpy as np
from math import factorial


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """

    window_size = np.abs(np.int64(window_size))
    order = np.abs(np.int64(order))

    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2

    # precompute coefficients
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


def smooth_route(route, window_size=15, order=4):
    # Parameters
    # route [ndarr, 2D, (x, y)]: Route of movement.

    # Define variables
    route_x, route_y = route

    # Smoothing y
    route_y_hat = savitzky_golay(route_y, window_size, order)

    # Reorganize route
    smoothed_route = np.stack((route_x, route_y_hat))

    return smoothed_route


def euclidean_distance(pos1, pos2):
    # Parameters
    # pos1, pos2 [ndarr, 2 elements [x, y]]: The position of the mouse body part on the Euclidean plane.

    # Define variable
    x1, y1 = pos1
    x2, y2 = pos2

    # Calculate Euclidean distance
    E_distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return E_distance


def binning_distance(distance, fps):
    # Parameter
    # distance [ndarr, 1D]: Result of 'euclidean_distance'.
    # fps [int or float]: Frame per second of video.

    # Binning for 1 sec length
    bin_step = np.arange(fps, len(distance), step=fps)
    binned_distance = np.array_split(distance, bin_step)
    return binned_distance


def speed_per_pixel(binned_distance, fps, pixel_for_cm):
    # Parameter
    # binned_distance [ndarr, 1D]: Result of 'binning_distance'.
    # fps [int or float]: Frame per second of video.
    # pixel_for_cm [int or float]: Pixels for 1 cm.

    # Output
    speed_per_bin = []

    # Compute speed per bin by pixels
    for distance_bin in binned_distance:
        if len(distance_bin) == fps:
            sum_distance = np.sum(distance_bin)
            speed = ((sum_distance / pixel_for_cm) / fps)
            speed_per_bin.append(speed)
        if len(distance_bin) < fps:
            sum_distance = np.sum(distance_bin)
            speed = ((sum_distance / pixel_for_cm) / len(distance_bin))
            speed_per_bin.append(speed)
        if len(distance_bin) > fps:
            raise Exception("The size of bin is exceeded fps. Check the 'binned_distance'.")
    return np.array(speed_per_bin)


def compute_speed(route, fps=30, pixel_for_cm=30):
    # Parameters
    # route [list or ndarr, 2D, [x, y]]: Route of movement.
    # fps [int or float, Default=30 fps]: Frame per second of video.
    # pixel_for_cm [int, Default=30 pixels]: Pixels for 1 cm.

    # Define position
    x, y = route
    pos1 = np.array([x[:-1], y[:-1]])
    pos2 = np.array([x[1:], y[1:]])

    # Compute distance
    distance = euclidean_distance(pos1, pos2)

    # Binning distance
    binned_distance = binning_distance(distance, int(fps))

    # Compute speed
    speed_per_bin = speed_per_pixel(binned_distance, int(fps), pixel_for_cm)

    return speed_per_bin

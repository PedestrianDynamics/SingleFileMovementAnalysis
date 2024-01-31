"""
©Rudina Subaih
"""
import math

import numpy as np
from scipy.ndimage.interpolation import shift


def transformation_coord(x, y, length, r):
    """
    transform coordinates to straight periodic trajectories (Ziemer2016)
    :param length: float. length of the oval corridor (circumference) in meter
    :param r: flowt. Radius
    :param x: float. a-coordinate
    :param y: float. y-coordinate
    :return: float, float. x and y-coordinate
    """
    x_trans = None
    y_trans = None

    if x < 0:
        arccos_val = (r - y) / math.sqrt((x ** 2) + ((y - r) ** 2))
        x_trans = (2 * length) + (r * math.pi) + (r * np.arccos(-arccos_val))
        y_trans = math.sqrt((x ** 2) + ((y - r) ** 2)) - r
    elif 0 <= x <= length:
        y_trans = math.sqrt(((y - r) ** 2)) - r
        if y < r:
            x_trans = x
        elif y >= r:
            x_trans = (2 * length) + (r * math.pi) - x
    elif x > length:
        arccos_val = (r - y) / math.sqrt(((x - length) ** 2) + ((y - r) ** 2))
        x_trans = length + (r * np.arccos(arccos_val))
        y_trans = math.sqrt(((x - length) ** 2) + ((y - r) ** 2)) - r

    return x_trans, y_trans


def read_trajectory_data(path):
    """
    Read the trajectory data from text file
    :param path: path to the trajectory text file
    :return: numpy array contains the trajectory data
    """
    data = np.loadtxt(path, usecols=(0, 1, 2, 3, 4), comments="#")
    return data


def individual_velocity_top_view(data, frame_data, delta_t, frame_current, frame_start, frame_end, fps, c):
    """
    to calculate the individual velocity for top view experiments (value + direction) of pedestrians
    :param data: ndarray. Trajectory dataset
    :param frame_data: the data of a specific frame
    :param delta_t: short time constant (to smooth the traj. in order to avoid fluctuations of ped. stepping)
    :param frame_current: ped_id of the current camera frame
    :param frame_start: ped_id of the starting camera frame
    :param frame_end: ped_id of the ending camera frame
    :param fps: camera frame per second
    :param c: circumference of the oval corridor
    :return: numpy array contain the velocity values
    """
    # 1. Get the data of the frame previous delta frame and the frame after delta frame
    data_frame_prev = data[data[:, 1] == (frame_current - int(delta_t * fps) / 2)]
    data_frame_next = data[data[:, 1] == (frame_current + int(delta_t * fps) / 2)]

    if data_frame_prev.size == 0:  # in case delta_t frames prev. < time start the video
        data_frame_prev = data[data[:, 1] == frame_start]  # take the first data frame (frame_start)
    if data_frame_next.size == 0:  # in case delta_t frames prev. > time end the video
        data_frame_next = data[data[:, 1] == frame_end]  # take the last data frame (frame_end)

    # 2. Order the rows of the data frame prev and next by the value of x-axis ascending (orders of ped. walking)
    # TODO: some pedestrians' information in the previous and next frame is missing (data extraction error). ERROR:
    #  in velocity calculation
    data_frame_prev = data_frame_prev[data_frame_prev[:, 2].argsort()]
    data_frame_next = data_frame_next[data_frame_next[:, 2].argsort()]

    # Some of the pedestrians are missing (trajectories not detected on specific time frames). So, it is better
    # to iterate over one by one
    velocity = np.zeros((len(frame_data[:, 0])))
    indx = 0
    ped_ids = frame_data[:, 0]
    for ped_id in ped_ids:
        ped_data_frame = data_frame_next[data_frame_next[:, 0] == ped_id]
        if ped_data_frame.size != 0:
            try:
                velocity[indx] = (data_frame_next[data_frame_next[:, 0] == ped_id][0][2] -
                                  data_frame_prev[data_frame_prev[:, 0] == ped_id][0][2]) / delta_t
                indx += 1
            except:
                # TODO: some pedestrians' information in the previous and next frame is missing (data extraction
                #  error). ERROR: in velocity calculation. For now I will do it like this
                velocity[indx] = 100
                indx += 1
        else:
            # TODO: indx += 1 ?!
            continue

    # 4. If the last ped. in the prev. frame enter the second iteration of the straight setup in the next frame
    if data_frame_prev[0, 0] == data_frame_next[-1, 0]:
        displacement = (data_frame_prev[0, 2] - 0) + (c - data_frame_next[-1, 2])
        velocity_first = displacement / delta_t
        if data_frame_prev[0, 0] == frame_data[0, 0]:
            velocity[0] = velocity_first
        else:
            velocity[-1] = velocity_first
    elif data_frame_prev[-1, 0] == data_frame_next[0, 0]:  # if the first ped. in the prev. frame walk in the opposite
        # side and become the last ped. in the second iteration in the next frame
        displacement = (c - data_frame_prev[-1, 2]) + (data_frame_next[0, 2] - 0)
        velocity_last = displacement / delta_t
        if data_frame_prev[0, 0] == frame_data[0, 0]:
            velocity[-1] = velocity_last
        else:
            velocity[0] = velocity_last

    return velocity


def individual_velocity_side_view(data, frame_data, delta_t, frame_current, fps):
    """
    to calculate the individual velocity for side view experiments (value + direction) of pedestrians
    :param data: ndarray. Trajectory dataset
    :param frame_data: the data of a specific frame
    :param delta_t: short time constant (to smooth the traj. in order to avoid fluctuations of ped. stepping)
    :param frame_current: ped_id of the current camera frame
    :param fps: camera frame per second
    :return: numpy array contain the velocity values
    """
    # order the pedestrians inside the current data frame by the position (0 to 3.14)
    frame_data = frame_data[frame_data[:, 2].argsort()]
    # initialize
    velocity = np.zeros((len(frame_data[:, 0])))
    indx = 0
    ped_ids = frame_data[:, 0]

    # 1. Get the data of the frame previous delta frame and the frame after delta frame
    data_frame_prev = data[data[:, 1] == (frame_current - int(delta_t * fps) / 2)]
    data_frame_next = data[data[:, 1] == (frame_current + int(delta_t * fps) / 2)]

    # 2. iterate over ped. inside the current frame one by one to calculate the velocity
    for ped_id in ped_ids:
        ped_data_prev = data_frame_prev[data_frame_prev[:, 0] == ped_id]
        ped_data_next = data_frame_next[data_frame_next[:, 0] == ped_id]

        # in case no prev. or next frame, take the value of x of minimum frame and maximum frame of pedestrian
        # respectively
        ped_data = data[data[:, 0] == ped_id]
        ped_data_min = min(ped_data[:, 2])
        ped_data_max = max(ped_data[:, 2])

        if (ped_data_prev.size != 0) and (ped_data_next.size != 0):  # there is frame previous and next
            velocity[indx] = (data_frame_next[data_frame_next[:, 0] == ped_id][0][2] -
                              data_frame_prev[data_frame_prev[:, 0] == ped_id][0][2]) / delta_t
            indx += 1
        elif (ped_data_prev.size != 0) and (ped_data_next.size == 0):  # there is frame previous
            velocity[indx] = (frame_data[frame_data[:, 0] == ped_id][0][2] -
                              data_frame_prev[data_frame_prev[:, 0] == ped_id][0][2]) / delta_t
            indx += 1
        elif (ped_data_prev.size == 0) and (ped_data_next.size != 0):  # there is frame next
            velocity[indx] = (data_frame_next[data_frame_next[:, 0] == ped_id][0][2] -
                              frame_data[frame_data[:, 0] == ped_id][0][2]) / delta_t
            indx += 1
        elif (ped_data_prev.size == 0) and (ped_data_next.size != 0):  # there is no frame previous and next
            velocity[indx] = (ped_data_max - ped_data_min) / delta_t
            indx += 1
        else:
            indx += 1
            continue

    return velocity


def individual_headway_side_view(frame_data):
    """
    Calculate the headway (distance in front) between two successive pedestrians
    :param frame_data: ndarray. Data of pedestrians inside the frame
    :return: numpy array. Headway
    """
    # initialize headway array with NaN values
    headway = np.full((1, len(frame_data)), np.NAN)[0]

    # 1. sort the pedestrians inside the current data frame by the position (0 to 3.14)
    frame_data = frame_data[frame_data[:, 2].argsort()]

    if len(frame_data) == 0:
        print("INFO:\tThe number of the pedestrians is small = 0")
    elif len(frame_data) == 1:
        print("INFO:\tThe number of the pedestrians is small = 1")
    else:
        # Calculate the Headway between the pedestrians
        shifted_frame_data = shift(frame_data[:, 2], -1, cval=np.NaN)
        headway = shifted_frame_data - frame_data[:, 2]

    return headway


def reorder_arr(arr, col):
    """
    reorder the ndarray values of ans array based on col. value
    :param col: ndnumpy array
    :param arr: numpy array to order
    :return: ordered ndnumpy array
    """
    # 1. We need to find the indices of the values in the second column of "arr" that we'd need to match the order of
    # "col"
    column = arr[:, 0].tolist()
    order = [column.index(item) for item in col]

    return arr[order, :]


def voronoi_rho_top_view(headway):
    """
    to calculate the voronoi rho of pedestrians in single-file movement experiments
    :param headway: ndarray. Headway
    :return: ndarray. rho
    """
    # initialize
    rho = np.zeros((len(headway)))

    denominator = headway + rotate_array(headway.tolist(), len(headway), 1)
    rho = 2 / denominator

    return rho


def voronoi_rho_side_view(headway):
    """
    to calculate the voronoi rho of pedestrians in single-file movement experiments
    :param headway: ndarray. Headway
    :return: ndarray. rho
    """
    # initialize
    rho = np.zeros((len(headway)))

    # the headway of the follower (shift the headway value to right)
    shifted_headway = shift(headway, 1, cval=np.NaN, order=0)
    # and the add the headway + headway_follower
    # print(headway)
    # print(shifted_headway)
    denominator = headway + shifted_headway
    # print(denominator)
    rho = 2 / denominator
    return rho


def rotate_array(arr, n, d):
    """
    rotate a numpy array (the last element will be the first)
    :param arr: list to rotate
    :param n: length of the arr
    :param d: number of steps to rotate
    :return:
    """
    temp = []
    i = 0
    while i < d:
        temp.append(arr[i])
        i = i + 1
    i = 0
    while d < n:
        arr[i] = arr[d]
        i = i + 1
        d = d + 1
    arr[:] = arr[: i] + temp
    return arr

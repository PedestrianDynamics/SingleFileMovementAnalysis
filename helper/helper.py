"""
©Rudina Subaih
"""
import math

import numpy as np
from scipy.ndimage.interpolation import shift
import numpy.typing as npt

import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'helper'))+'/')
from experiments import EXPERIMENTS


def transformation_coord(data: npt.NDArray[np.float64], length: float, r: float) -> npt.NDArray[np.float64]:
    """
    transform coordinates to straight periodic trajectories (Ziemer2016)
    :param data_transformation_additional: numpy array.
    :param length: float. length of the oval corridor (circumference) in meter
    :param r: flowt. Radius
    :return: float, float. x and y-coordinate
    """
    data_new = np.empty((len(data), 2))

    for i, row in enumerate(data):
        x_trans = None
        y_trans = None

        x=row[0]
        y=row[1]

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
        
        data_new[i] = [x_trans, y_trans]

    return data_new

def individual_velocity_top_view(data: npt.NDArray[np.float64], frame_data: npt.NDArray[np.float64], delta_t: float, frame_current: int, frame_start: int, frame_end: int, fps: int, c: float, flag_disp) -> npt.NDArray[np.float64]:

    if flag_disp == 'x':
        return individual_velocity_top_view_x(data, frame_data, delta_t, frame_current, frame_start, frame_end, fps, c)
    elif flag_disp == 'y':
        return individual_velocity_top_view_y(data, frame_data, delta_t, frame_current, frame_start, frame_end, fps, c)
    elif flag_disp == 'r':
        return individual_velocity_top_view_r(data, frame_data, delta_t, frame_current, frame_start, frame_end, fps, c)
    else:
        raise ValueError('The target should be x, y, or r')

def individual_velocity_top_view_x(data: npt.NDArray[np.float64], frame_data: npt.NDArray[np.float64], delta_t: float, frame_current: int, frame_start: int, frame_end: int, fps: int, c: float) -> npt.NDArray[np.float64]:
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
    velocity = np.zeros((len(frame_data[:, 0])))

    # 1. Get the data of the frame previous delta frame and the frame after delta frame
    data_frame_prev = data[data[:, 1] == (frame_current - int(delta_t * fps / 2))]
    data_frame_next = data[data[:, 1] == (frame_current + int(delta_t * fps / 2))]

    if data_frame_prev.size == 0:  # in case delta_t frames prev. < time start the video
        # data_frame_prev = data[data[:, 1] == frame_start]  # take the first data frame (frame_start)
        velocity[:] = np.NaN
        return velocity
    if data_frame_next.size == 0:  # in case delta_t frames prev. > time end the video
        # data_frame_next = data[data[:, 1] == frame_end]  # take the last data frame (frame_end)
        velocity[:] = np.NaN
        return velocity

    # 2. Order the rows of the data frame prev and next by the value of x-axis ascending (orders of ped. walking)
    # TODO: some pedestrians' information in the previous and next frame is missing (data extraction error). ERROR:
    #  in velocity calculation
    data_frame_prev_x = data_frame_prev[:, 2]
    data_frame_next_x = data_frame_next[:, 2]
    data_frame_prev = data_frame_prev[data_frame_prev_x.argsort()]
    data_frame_next = data_frame_next[data_frame_next_x.argsort()]

    # Some of the pedestrians are missing (trajectories not detected on specific time frames). So, it is better
    # to iterate over one by one
    indx = 0
    ped_ids = frame_data[:, 0]
    for ped_id in ped_ids:
        x1 = data_frame_next[data_frame_next[:, 0] == ped_id][0][2]
        x2 = data_frame_prev[data_frame_prev[:, 0] == ped_id][0][2]

        ped_data_frame = data_frame_next[data_frame_next[:, 0] == ped_id]
        
        if x1 > x2 and np.abs(x1-x2) < 1:
            if ped_data_frame.size != 0:
                try:
                    velocity[indx] = (x1 - x2) / delta_t
                    # if velocity[indx] > 37:
                    #     print('here',x1, x2, y1, y2, frame_current,delta_t,ped_id,data_frame_next.shape,data_frame_prev.shape)
                    # if velocity[indx] > 37:
                        # print(x1, x2, y1, y2, frame_current,delta_t,ped_id,data_frame_next.shape,data_frame_prev.shape)
                    indx += 1
                except:
                    # TODO: some pedestrians' information in the previous and next frame is missing (data extraction
                    #  error). ERROR: in velocity calculation. For now I will do it like this
                    velocity[indx] = np.NAN
                    indx += 1
            # if ped_id == 27 and frame_current == 3392:
            #     print(x1, x2, y1, y2, frame_current,delta_t,ped_id,data_frame_next.shape,data_frame_prev.shape)
        else:
            # when the pedestrina finish the round and start new
            velocity[indx] = np.NAN
            indx += 1

    return velocity

def individual_velocity_top_view_r(data: npt.NDArray[np.float64], frame_data: npt.NDArray[np.float64], delta_t: float, frame_current: int, frame_start: int, frame_end: int, fps: int, c: float) -> npt.NDArray[np.float64]:
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
    velocity = np.zeros((len(frame_data[:, 0])))

    # 1. Get the data of the frame previous delta frame and the frame after delta frame
    data_frame_prev = data[data[:, 1] == (frame_current - int(delta_t * fps / 2))]
    data_frame_next = data[data[:, 1] == (frame_current + int(delta_t * fps / 2))]

    if data_frame_prev.size == 0:  # in case delta_t frames prev. < time start the video
        # data_frame_prev = data[data[:, 1] == frame_start]  # take the first data frame (frame_start)
        velocity[:] = np.NaN
        return velocity
    if data_frame_next.size == 0:  # in case delta_t frames prev. > time end the video
        # data_frame_next = data[data[:, 1] == frame_end]  # take the last data frame (frame_end)
        velocity[:] = np.NaN
        return velocity

    # 2. Order the rows of the data frame prev and next by the value of x-axis ascending (orders of ped. walking)
    # TODO: some pedestrians' information in the previous and next frame is missing (data extraction error). ERROR:
    #  in velocity calculation
    data_frame_prev_r = np.sqrt(data_frame_prev[:, 2] ** 2 + data_frame_prev[:, 3] ** 2)
    data_frame_next_r = np.sqrt(data_frame_next[:, 2] ** 2 + data_frame_next[:, 3] ** 2)
    data_frame_prev = data_frame_prev[data_frame_prev_r.argsort()]
    data_frame_next = data_frame_next[data_frame_next_r.argsort()]

    # Some of the pedestrians are missing (trajectories not detected on specific time frames). So, it is better
    # to iterate over one by one
    indx = 0
    ped_ids = frame_data[:, 0]
    for ped_id in ped_ids:
        x1 = data_frame_next[data_frame_next[:, 0] == ped_id][0][2]
        x2 = data_frame_prev[data_frame_prev[:, 0] == ped_id][0][2]
        y1 = data_frame_next[data_frame_next[:, 0] == ped_id][0][3]
        y2 = data_frame_prev[data_frame_prev[:, 0] == ped_id][0][3]

        ped_data_frame = data_frame_next[data_frame_next[:, 0] == ped_id]
        
        if x1 > x2 and np.abs(x1-x2) < 1:
            if ped_data_frame.size != 0:
                try:
                    velocity[indx] = (np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)) / delta_t
                    # if velocity[indx] > 37:
                    #     print('here',x1, x2, y1, y2, frame_current,delta_t,ped_id,data_frame_next.shape,data_frame_prev.shape)
                    # if velocity[indx] > 37:
                        # print(x1, x2, y1, y2, frame_current,delta_t,ped_id,data_frame_next.shape,data_frame_prev.shape)
                    indx += 1
                except:
                    # TODO: some pedestrians' information in the previous and next frame is missing (data extraction
                    #  error). ERROR: in velocity calculation. For now I will do it like this
                    velocity[indx] = np.NAN
                    indx += 1
            # if ped_id == 27 and frame_current == 3392:
            #     print(x1, x2, y1, y2, frame_current,delta_t,ped_id,data_frame_next.shape,data_frame_prev.shape)
        else:
            # when the pedestrina finish the round and start new
            velocity[indx] = np.NAN
            indx += 1

    # 4. If the last ped. in the prev. frame enter the second iteration of the straight setup in the next frame
    
    ###IGNORE THIS PART
    # if data_frame_prev[0, 0] == data_frame_next[-1, 0]:
    #     if data_frame_prev[0, 0] == frame_data[0, 0]:
    #         velocity[0] = np.NaN
    #     else:
    #         velocity[-1] = np.NaN
    # elif data_frame_prev[-1, 0] == data_frame_next[0, 0]:  # if the first ped. in the prev. frame walk in the opposite
    #     # side and become the last ped. in the second iteration in the next frame
    #     if data_frame_prev[0, 0] == frame_data[0, 0]:
    #         velocity[-1] = np.NaN
    #     else:
    #         velocity[0] = np.NaN
    # if frame_current == 3392 or frame_current == 3393 or frame_current == 3394:
    #     print(velocity[27],np.nanmax(velocity))
    #print(frame_current,velocity[~np.isnan(velocity)].max())
    return velocity

def individual_velocity_side_view(data: npt.NDArray[np.float64], frame_data: npt.NDArray[np.float64], delta_t: float, frame_current: int, fps: int) -> npt.NDArray[np.float64]:
    """
    to calculate the individual velocity for side view experiments (value + direction) of pedestrians
    :param data: ndarray. Trajectory dataset
    :param frame_data: the data of a specific frame
    :param delta_t: short time constant (to smooth the traj. in order to avoid fluctuations of ped. stepping)
    :param frame_current: ID of the current camera frame
    :param fps: camera frame per second
    :return: numpy array contain the velocity values
    """
    # order the pedestrians inside the current data frame by the position (0 to 3.14)
    #frame_data = frame_data[frame_data[:, 2].argsort()]
    # initialize
    velocity = np.zeros((len(frame_data[:, 0])))
    indx = 0
    ped_ids = frame_data[:, 0]

    # 1. Get the data of the frame previous delta frame and the frame after delta frame
    data_frame_prev = data[data[:, 1] == (frame_current - int(delta_t * fps / 2) )]
    data_frame_next = data[data[:, 1] == (frame_current + int(delta_t * fps / 2) )]
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
        elif (ped_data_prev.size != 0) and (ped_data_next.size == 0):  # there is frame previous
            velocity[indx] = (frame_data[frame_data[:, 0] == ped_id][0][2] -
                              data_frame_prev[data_frame_prev[:, 0] == ped_id][0][2]) / delta_t
        elif (ped_data_prev.size == 0) and (ped_data_next.size != 0):  # there is frame next
            velocity[indx] = (data_frame_next[data_frame_next[:, 0] == ped_id][0][2] -
                              frame_data[frame_data[:, 0] == ped_id][0][2]) / delta_t
        elif (ped_data_prev.size == 0) and (ped_data_next.size != 0):  # there is no frame previous and next
            velocity[indx] = (ped_data_max - ped_data_min) / delta_t
        indx += 1
        
    return velocity

def individual_headway_side_view(frame_data: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """
    Calculate the headway (distance in front) between two successive pedestrians
    :param frame_data: ndarray. Data of pedestrians inside the frame
    :param c: float. circumference of the oval corridor
    :return: numpy array. Headway
    """
    # initialize headway array with NaN values
    headway = np.full((1, len(frame_data)), np.NAN)[0]

    # 1. sort the pedestrians inside the current data frame by the position (0 to Max)
    frame_data = frame_data[frame_data[:, 2].argsort()]

    if len(frame_data) != 0 or len(frame_data) != 1:
        # Calculate the Headway between the pedestrians
        shifted_frame_data = shift(frame_data[:, 2], -1, cval=np.NaN)
        headway = shifted_frame_data - frame_data[:, 2]
    # Other cases where we can not calculate the headway::
    # len(frame_data) == 0, the number of the pedestrians is small = 0
    # len(frame_data) == 1, the number of the pedestrians is small = 1


    return headway

def reorder_arr(arr: npt.NDArray[np.float64], col: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
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

def voronoi_rho_top_view(headway: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
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


def voronoi_rho_side_view(headway: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]: 
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

def rotate_array(arr: npt.NDArray[np.float64], n: int, d: int) -> npt.NDArray[np.float64]:
    """
    rotate a numpy array (the last element will be the first)
    :param arr: list to rotate
    :param n: length of the arr
    :param d: number of steps to rotate
    :return: rotated list
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

def process_data(arr: npt.NDArray[np.float64], experiment_name: str) -> npt.NDArray[np.float64]:
    """
    apply the additional transformation which is specific for each experiment
    :param arr: trajectory data
    :param experiment_name: experiment name
    :return: processed trajectory data
    """
    e = EXPERIMENTS[experiment_name]

    # transformation for x and y values (unique for each experiment)
    x = arr[:, e.x_rotate].copy()
    y = arr[:, e.y_rotate].copy()

    arr[:, 0] = (e.ref_x * x / e.unit) + e.shift_x

    # if e.y_rotate:
    arr[:, 1] = ((e.ref_y * y) / e.unit) + e.shift_y

    return arr

def calculate_speed_density_headway(data: npt.NDArray[np.float64], fps: int, c: float, camera_capture: int, delta_t: float, flag_disp = 'x') -> npt.NDArray[np.float64]:
    """
    calculate the speed and density of pedestrians in the experiment
    :param data: numpy array. Trajectory data
    :param fps: int. camera frame per second
    :param c: float. circumference of the oval corridor
    :param camera_capture: int. 0 => top_view, 1 => side_view (default=0)
    :param delta_t: float. short time constant (to smooth the traj. in order to avoid fluctuations of ped. stepping)
    :param experiment_name: str. experiment name
    :return: numpy array. speed and density of pedestrians
    """
    # 1. For each frame, I need to calculate the speed, rho, and distances of pedestrians inside frame
    frames = np.sort(np.unique(data[:, 1]))
    frame_start = frames[0]
    frame_end = frames[-1]

    new_arr = np.empty((1, 8))

    for fr in frames:
        # Pedestrians inside the frame
        frame_data = data[data[:, 1] == fr]
        # A. Sort the row data by the position of pedestrians to know the order of the pedestrians in the
        # oval corridor (straight trajectories format)
        frame_data = frame_data[frame_data[:, 2].argsort()]

        # B. Calculate pedestrian velocity
        if camera_capture == 0:
            velocity = individual_velocity_top_view(data, frame_data, delta_t, fr, frame_start,
                                                    frame_end, fps, c, flag_disp)
            # C. Calculate pedestrians' headway
            # Calculate the headway by taking the difference between each row x value and the previous
            headway = np.diff(frame_data[:, 2])
            # ... for the last pedestrian, we calculate it as
            headway_last = (c - frame_data[-1, 2]) + (frame_data[0, 2])
            headway = np.append(headway, headway_last)
            # D. Calculate pedestrians' rho
            rho = voronoi_rho_top_view(headway)
        else:
            velocity = individual_velocity_side_view(data, frame_data, delta_t, fr, fps)
            # C. Calculate pedestrians' headway
            headway = individual_headway_side_view(frame_data)
            # D. Calculate pedestrians' rho
            rho = voronoi_rho_side_view(headway)

        # reshape the velocity, headway, rho
        velocity = np.reshape(velocity, (velocity.size, 1))
        headway = np.reshape(headway, (headway.size, 1))
        rho = np.reshape(rho, (rho.size, 1))

        # id, fr, x, y, z, velocity, headway, rho
        frame_data = np.append(frame_data, velocity, axis=1)
        frame_data = np.append(frame_data, headway, axis=1)
        frame_data = np.append(frame_data, rho, axis=1)

        new_arr = np.concatenate((new_arr, frame_data))

    result = new_arr[1:]
    # drop all nan-value rows
    result = result[~np.isnan(result).any(axis=1)]
    return result

def extract_steady_state(data: npt.NDArray[np.float64], st: float, en: float) -> npt.NDArray[np.float64]:
    """ 
    extract the steady-state data from the dataset  
    :param data: numpy array.
    :param st: float. start value
    :param en: float. end value
    :return: numpy array.
    """
    rho_v = data[data[:, 1] > st]
    rho_v = rho_v[rho_v[:, 1] < en]

    return rho_v


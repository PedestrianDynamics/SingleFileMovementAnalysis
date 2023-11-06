"""
©Rudina Subaih
Making additional transformations for each experiment based on the coordinate system defined while extracting the
trajectories
PLUS:
Unify the format of the raw trajectory file of the experiment as:
# id frame x y z
because each experiment has different format and type of the trajectory files (exported from different trajectory
extraction software)
"""
import argparse
import os

import numpy as np
import numpy.typing as npt
from experiments import EXPERIMENTS
import pandas as pd
import sqlite3
import pedpy


def get_parser_args():
    """
    Required arguments from the user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="transform the trajectories (x, y)")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path to the directory containing the trajectory files"
    )
    parser.add_argument(
        "-n",
        "--fileName",
        help="Enter the names of the trajectory files",
        nargs="+"
    )
    parser.add_argument(
        "-expn",
        "--expName",
        help="Enter the experiment name: " + " , ".join(EXPERIMENTS.keys()),
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


def file_formate(data, experiment_name):
    """
    make the format of the trajectory file
    #id  frame   x   y   z
    OR
    #id  time   x   y   z
    :param file_name: name of the trajectory file
    :return:
    """
    e = EXPERIMENTS[experiment_name]

    if e.id_col_index is None:
        raise ValueError('ERROR: you have to add pedestrian ID to the trajectory file.')

    if e.x_col_index is None:
        raise ValueError('ERROR: you have to add x-coordinate to the trajectory file.')

    if e.y_col_index is None:
        raise ValueError('ERROR: you have to add y-coordinate to the trajectory file.')

    # Specify the column indices by which you want to sort the rows
    column_indices = (e.id_col_index, e.x_col_index)

    # Get the indices that would sort the first column
    sorted_indices = np.lexsort((data[:, column_indices[1]], data[:, column_indices[0]]))

    # Sort the matrix based on the specified columns
    data = data[sorted_indices]

    if e.fr_col_index is None:
        # iterate over pedestrians and give them frame
        pedIDs = set(data[:, e.id_col_index])
        frames = np.array([])
        for id in pedIDs:
            ped_data = data[data[:, e.id_col_index] == id]
            frames = np.append(frames, np.arange(ped_data.shape[0]))  # values from 0 to the length of ped. traj.
    else:
        frames = data[:, e.fr_col_index]

    if e.z_col_index is None:
        z = np.zeros(data.shape[0])  # values equal 0
    else:
        z = frames = data[:, e.z_col_index]

    # Create a 2D NumPy matrix by stacking the 1D arrays vertically
    data = np.column_stack((data[:, e.id_col_index], frames, data[:, e.x_col_index], data[:, e.y_col_index], z))

    # sort based od id and fr because the previous data appears not sorted
    data = data[np.lexsort((data[:, 1], data[:, 0]))]

    return data


def process_data(arr: npt.NDArray[np.float64], experiment_name: str):
    """
    apply the additional transformation which is specific for each experiment
    :param arr: trajectory data
    :param experiment_name: experiment name
    :return:
    """

    e = EXPERIMENTS[experiment_name]

    if (e.Min is not None) and (e.Max is not None):  # data inside measurement area (unique for each experiment)
        arr = arr[((arr[:, 2] / e.unit) >= e.Min) & ((arr[:, 2] / e.unit) <= e.Max)]

    # transformation for x and y values (unique for each experiment)
    x = arr[:, e.x_rotate].copy()
    y = arr[:, e.y_rotate].copy()

    arr[:, 2] = (e.ref_x * x / e.unit) + e.shift_x

    if e.y_rotate:
        arr[:, 3] = ((e.ref_y * y) / e.unit) + e.shift_y

    return arr


def read_sqlite_file(path, file):
    """

    :param trajectory_file:
    :return: obj: TrajectoryData
    obj: WalkableArea
    """
    trajectory_file = "%s/%s" % (path, file)
    con = sqlite3.connect(trajectory_file)
    data = pd.read_sql_query(
        "select frame, id, pos_x as x, pos_y as y, ori_x as ox, ori_y as oy from trajectory_data",
        con,
    )
    # table in the SQLite database. The data is read into a Pandas DataFrame named data.
    return data


if __name__ == "__main__":
    arg = get_parser_args()
    path = arg.path
    exp_name = arg.expName
    files = arg.fileName
    path_output = arg.pathOutput

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]  # extension of the data file
        # format of the file
        if file_type == ".sqlite":
            data = read_sqlite_file(path, file)
            data = data.to_numpy()  # fr, pedID, x, y, ori_x, ori_y
        else:
            e = EXPERIMENTS[exp_name]
            data = np.loadtxt("%s/%s" % (path, file), skiprows=1, delimiter=e.delimiter)

        data = file_formate(data, exp_name)

        # setup coordination system transformation
        data = process_data(data, exp_name)

        header = "#id\tfr\tx\ty\tz"
        np.savetxt(
            "%s/%s_transformation_additional.txt" % (path_output, file_name),
            data,
            delimiter="\t",
            header=header,
            comments="",
            newline="\r\n",
            fmt="%d\t%d\t%.4f\t%.4f\t%.4f"
        )

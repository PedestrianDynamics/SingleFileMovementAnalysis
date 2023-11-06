"""
©Rudina Subaih
Unify the raw trajectory file format to a unifird format"""
import argparse
import os

import numpy as np
import numpy.typing as npt
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
        "-deli",
        "--delimiter",
        help="Enter the delimiter of the trajectory file",
    )
    parser.add_argument(
        "-idIdx",
        "--idColIndex",
        type=int,
        help="Enter the id_col_index of the trajectory file",
    )
    parser.add_argument(
        "-frIdx",
        "--frColIndex",
        type=int,
        help="Enter the fr_col_index of the trajectory file",
    )
    parser.add_argument(
        "-xIdx",
        "--xColIndex",
        type=int,
        help="Enter the x_col_index of the trajectory file",
    )
    parser.add_argument(
        "-yIdx",
        "--yColIndex",
        default=None,
        type=int,
        help="Enter the y_col_index of the trajectory file",
    )
    parser.add_argument(
        "-zIdx",
        "--zColIndex",
        type=int,
        help="Enter the z_col_index of the trajectory file",
    )
    parser.add_argument(
        "-addiIdx",
        "--addiColIndex",
        default=None,
        type=int,
        help="Enter the additional_col_index of the trajectory file",
        nargs="+"
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


def file_formate(data, id_col_index, fr_col_index, x_col_index,
                 y_col_index, z_col_index, additional_col_index):
    """
    make the format of the trajectory file
    #id  frame   x   y   z
    OR
    #id  time   x   y   z
    :param file_name: name of the trajectory file
    :return:
    """
    if id_col_index is None:
        raise ValueError('ERROR: you have to add pedestrian ID to the trajectory file.')

    if x_col_index is None:
        raise ValueError('ERROR: you have to add x-coordinate to the trajectory file.')

    if y_col_index is None:
        raise ValueError('ERROR: you have to add y-coordinate to the trajectory file.')

    # Specify the column indices by which you want to sort the rows
    column_indices = (id_col_index, x_col_index)

    # Get the indices that would sort the first column
    sorted_indices = np.lexsort((data[:, column_indices[1]], data[:, column_indices[0]]))

    # Sort the matrix based on the specified columns
    data = data[sorted_indices]

    if fr_col_index is None:
        # iterate over pedestrians and give them frame
        pedIDs = set(data[:, id_col_index])
        frames = np.array([])
        for id in pedIDs:
            ped_data = data[data[:, id_col_index] == id]
            frames = np.append(frames, np.arange(ped_data.shape[0]))  # values from 0 to the length of ped. traj.
    else:
        frames = data[:, fr_col_index]

    if z_col_index is None:
        z = np.zeros(data.shape[0])  # values equal 0
    else:
        z = frames = data[:, z_col_index]

    # Create a 2D NumPy matrix by stacking the 1D arrays vertically
    data = np.column_stack((data[:, id_col_index], frames, data[:, x_col_index], data[:, y_col_index], z))

    # sort based od id and fr because the previous data appears not aus_mix_sorted
    data = data[np.lexsort((data[:, 1], data[:, 0]))]

    return data


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
    files = arg.fileName
    path_output = arg.pathOutput
    delimiter = arg.delimiter
    id_col_index = arg.idColIndex
    fr_col_index = arg.frColIndex
    x_col_index = arg.xColIndex
    y_col_index = arg.yColIndex
    z_col_index = arg.zColIndex
    additional_col_index = arg.addiColIndex

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]  # extension of the data file
        # format of the file
        if file_type == ".sqlite":
            data = read_sqlite_file(path, file)
            data = data.to_numpy()  # fr, pedID, x, y, ori_x, ori_y
        else:
            data = np.loadtxt("%s/%s" % (path, file), skiprows=1, delimiter=delimiter)

        data = file_formate(data,
                            id_col_index,
                            fr_col_index,
                            x_col_index,
                            y_col_index,
                            z_col_index,
                            additional_col_index)

        header = "#id\tfr\tx\ty\tz"
        np.savetxt(
            "%s/%s_traj_file_format.txt" % (path_output, file_name),
            data,
            delimiter="\t",
            header=header,
            comments="",
            newline="\r\n",
            fmt="%d\t%d\t%.4f\t%.4f\t%.4f"
        )

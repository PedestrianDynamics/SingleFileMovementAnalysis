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
from typing import List

import numpy as np
import numpy.typing as npt
from experiments import EXPERIMENTS
import pandas as pd
import sqlite3


def get_parser_args() -> argparse.Namespace:
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
        "-expk",
        "--expKey",
        help="Enter the 'experiment key': " + " , ".join(EXPERIMENTS.keys()),
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


def process_data(arr: npt.NDArray[np.float64], experiment_name: str) -> npt.NDArray[np.float64]:
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


def read_sqlite_file(path: str, file: str) -> pd.DataFrame:
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
    arg: argparse.Namespace = get_parser_args()
    path: str = arg.path
    exp_key: str = arg.expKey
    files: List[str] = arg.fileName
    path_output: str = arg.pathOutput

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]  # extension of the data file
        # format of the file
        if file_type == ".sqlite":
            data = read_sqlite_file(path, file)
            data = data.to_numpy()  # fr, pedID, x, y, ori_x, ori_y
        else:
            e = EXPERIMENTS[exp_key]
            data = np.loadtxt("%s/%s" % (path, file), skiprows=1, delimiter=e.delimiter)

        # setup coordination system transformation
        data = process_data(data, exp_key)

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

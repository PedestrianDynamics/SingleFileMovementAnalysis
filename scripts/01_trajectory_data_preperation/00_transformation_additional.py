"""
©Rudina Subaih
Making additional transformations for each experiment based on the coordinate system defined while extracting the
trajectories
"""
import argparse
import os

import numpy as np
import numpy.typing as npt
from lib.experiments import EXPERIMENTS


def get_parser_args():
    """
    Required arguments from the user to input

    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="transform the trajectories (x, y)")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path to the directory contains the trajectory files",
    )
    parser.add_argument(
        "-n", "--filename", help="Enter the trajectory file names", nargs="+"
    )
    parser.add_argument(
        "-expn",
        "--expName",
        help="Enter the experiment name: " + ", ".join(EXPERIMENTS.keys()),
    )
    return parser.parse_args()


def process_data(arr: npt.NDArray[np.float64], experiment_name: str):
    """
    apply the additional transformation which is specific for each experiment

    :param arr: ndarray. Trajectory data
    :param experiment_name: string. Experiments name
    :return:
    """

    e = EXPERIMENTS[experiment_name]

    # todo: can we dispense with this if?
    if experiment_name == "motivation_without_germany_Lukowski":
        arr = np.append(arr, [[0] for _ in range(len(arr[:, 0]))], axis=1)

    if e.Min and e.Max:
        arr = arr[(arr[:, 2] >= e.Min) & (arr[:, 2] <= e.Max)]

    arr[:, 2] = arr[:, e.x_index] / e.unit + e.shift_x
    if e.y_index:
        arr[:, 3] = e.inv_y * arr[:, e.y_index] / e.unit + e.shift_y

    return arr


if __name__ == "__main__":
    arg = get_parser_args()
    path = arg.path
    exp_name = arg.expName
    files = arg.filename

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]

        try:
            data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4))
        except:
            data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3))

        print(EXPERIMENTS[exp_name])
        data = process_data(data, exp_name)

        header = "#id\tfr\tx\ty\tz"
        np.savetxt(
            "./%s_transformation_additional.txt" % file_name,
            data,
            delimiter="\t",
            header=header,
            comments="",
            newline="\r\n",
            fmt="%d\t%d\t%.4f\t%.4f\t%.4f",
        )

"""
©Rudina Subaih
Making additional transformations for each experiment based on the coordinate system defined while extracting the
trajectories
"""
import argparse
import os

import numpy as np
import numpy.typing as npt
from experiments import EXPERIMENTS


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
        default="",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


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
    x = arr[:, e.x_index].copy()
    y = arr[:, e.y_index].copy()

    arr[:, 2] = (e.inv_x * x / e.unit) + e.shift_x

    if e.y_index:
        arr[:, 3] = ((e.inv_y * y) / e.unit) + e.shift_y

    return arr


if __name__ == "__main__":
    arg = get_parser_args()
    path = arg.path
    exp_name = arg.expName
    files = arg.fileName
    path_output = arg.pathOutput

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]

        # Some trajectory files miss the z column (i. e. motivation_germany_lukowski experiment)
        try:
            data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4))
        except:
            data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3))
            data = np.append(data, [[0] for _ in range(len(data[:, 0]))], axis=1)

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

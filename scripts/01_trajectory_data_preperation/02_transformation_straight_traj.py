"""
©Rudina Subaih
transforming the oval corridor trajectories to straight trajectories using the same formulas in Ziemer2016 with
some modifications
"""
import numpy as np
import os
from typing import List

sys.path.append(os.path.abspath(os.path.join('..', 'helper'))+'/')
from experiments import EXPERIMENTS

import time
import argparse


def get_parser_args() -> argparse.Namespace:
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="transform 00_raw trajectories to straight trajectories (Ziemer2016)")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path to the directory containing the trajectory files (transformed additional)"
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
        help="Enter the experiment key: " + " , ".join(EXPERIMENTS.keys()),
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


def transformation_coord(x, y, length, r):
    """
    transform coordinates to straight periodic trajectories (Ziemer2016)
    :param length: float. length of the oval corridor (circumference) in meter
    :param r: flowt. Radius
    :param x: float. x-coordinate
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

if __name__ == "__main__":
    arg: argparse.Namespace = get_parser_args()
    path: str = arg.path
    files: List[str] = arg.fileName
    exp_key: str = arg.expKey
    path_output: str = arg.pathOutput

    fig_name = os.path.basename(os.path.splitext(path)[0])

    e = EXPERIMENTS[exp_key]
    length = e.length
    r = e.radius

    # record start time
    start = time.time()

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]  # extension of the data file

        data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4, 5, 6))
        data_new = np.empty((len(data), 7))

        for i, row in enumerate(data):
            x_trans, y_trans = transformation_coord(row[2], row[3], length, r)
            data_new[i] = [row[0], row[1], x_trans, y_trans, row[4], row[5], row[6]]

        header = "#id\tfr\tx\ty\tz\tgender\ttime"
        np.savetxt("%s/%s_straight_traj.txt" % (path_output, file_name),
                   data_new,
                   delimiter="\t",
                   header=header,
                   comments="",
                   newline="\r\n",
                   fmt="%d\t%d\t%.4f\t%.4f\t%.4f\t%d\t%.4f")

    # record end time
    end = time.time()
    # print the difference between start
    # and end time in milli. secs
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")

"""
©Rudina Subaih
transforming the oval corridor trajectories to straight trajectories using the same formulas in Ziemer2016 with
some modifications
"""
import numpy as np
import os
from helper import transformation_coord
from experiments import EXPERIMENTS
import time
import argparse


def get_parser_args():
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
        "-expn",
        "--expName",
        help="Enter the experiment name: " + " , ".join(EXPERIMENTS.keys()),
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    parser.add_argument(
        "-n",
        "--fileName",
        help="Enter the names of the trajectory files",
        nargs="+"
    )
    return parser.parse_args()


if __name__ == "__main__":
    arg = get_parser_args()
    path = arg.path
    files = arg.fileName
    fig_name = os.path.basename(os.path.splitext(path)[0])
    exp_name = arg.expName
    path_output = arg.pathOutput

    e = EXPERIMENTS[exp_name]
    length = e.length
    r = e.radius

    # record start time
    start = time.time()

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]  # extension of the data file

        data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4))
        data_new = np.empty((len(data), 5))

        for i, row in enumerate(data):
            x_trans, y_trans = transformation_coord(row[2], row[3], length, r)
            data_new[i] = [row[0], row[1], x_trans, y_trans, row[4]]

        header = "#id\tfr\tx\ty\tz"
        np.savetxt("%s/%s_straight_traj.txt" % (path_output, file_name),
                   data_new,
                   delimiter="\t",
                   header=header,
                   comments="",
                   newline="\r\n",
                   fmt="%d\t%d\t%.4f\t%.4f\t%.4f")

    # record end time
    end = time.time()
    # print the difference between start
    # and end time in milli. secs
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")

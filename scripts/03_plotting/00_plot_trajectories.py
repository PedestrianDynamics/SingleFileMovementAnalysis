"""
©Rudina Subaih
Visualise the "raw trajectories" spatially (x-y) (oval trajectories)
Visualise the "straight trajectories" spatially (x-y)
"""
import os
import sys
import argparse

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.abspath(os.path.join('..', 'helper'))+'/')
from experiments import EXPERIMENTS

import sqlite3


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="Plot the trajectories of pedestrians x-y")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path of the directory contains the trajectory files"
    )
    parser.add_argument(
        "-n",
        "--fileName",
        help="Enter the names of the trajectory files",
        nargs="+"
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Enter a title for the figure",
        nargs="+"
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


if __name__ == "__main__":
    arg = get_parser_args()
    path = arg.path
    files = arg.fileName
    titles = arg.title
    path_output = arg.pathOutput
    fig_name = os.path.basename(os.path.splitext(path)[0])

    for file, title in zip(files, titles):
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]  # extension of the data file

        fig = plt.figure(figsize=(7, 6))

        data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4))
        plt.plot(data[:, 2], data[:, 3], "bo", markersize=0.3)

        # plt.xlim(1, 12)
        # plt.ylim(-2, 6)
        #
        # plt.vlines(2.3, -2, 2, colors="r", linestyles="dashed")
        # plt.vlines(7.48363,  -2, 2, colors="r", linestyles="dashed")
        # plt.vlines(9.78363,  -2, 2, colors="r", linestyles="dashed")

        plt.xlim(0, 14.97)
        plt.ylim(-2, 2)

        plt.vlines(2.3, -2, 2, colors="r", linestyles="dashed")
        plt.vlines(7.48363, -2, 2, colors="r", linestyles="dashed")
        plt.vlines(9.78363, -2, 2, colors="r", linestyles="dashed")

        plt.xlabel(r"$\rm x~[m]$")
        plt.ylabel(r"$\rm y~[m]$")
        plt.title(title)

        plt.savefig("%s/%s.pdf" % (path_output, file_name))
        plt.savefig("%s/%s.png" % (path_output, file_name))
        plt.close()

"""
©Rudina Subaih
Visualise the straight trajectories spatially (x-y)
"""
import os
import argparse

import matplotlib.pyplot as plt
from numpy import *


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description='Plot the trajectories of pedestrians x-y (straight transformed '
                                                 'trajectories)')
    parser.add_argument("-p", "--path", default="./", help='Enter the path of the trajectory file')
    parser.add_argument("-t", "--title", help='Enter the title for the figure')
    return parser.parse_args()


if __name__ == '__main__':
    arg = get_parser_args()
    path = arg.path
    title = arg.title
    fig_name = os.path.basename(os.path.splitext(path)[0])

    fig = plt.figure(figsize=(7, 6))

    data = loadtxt(path, usecols=(0, 1, 2, 3, 4))
    data = data[data[:, 0] == 1]

    plt.plot(data[:, 2], data[:, 3], "bo", markersize=0.3)
    plt.vlines(2.5, -1, 1, colors="r", linestyles="dashed")
    plt.vlines(8.3, -1, 1, colors="r", linestyles="dashed")
    plt.vlines(10.8, -1, 1, colors="r", linestyles="dashed")

    # plt.xlim(0, 26.8496)
    plt.ylim(-1, 1)
    plt.title(title)
    plt.xlabel(r"$\rm x~[m]$")
    plt.ylabel(r"$\rm y~[m]$")
    plt.savefig("./%s.pdf" % fig_name)
    plt.savefig("./%s.png" % fig_name)
    plt.close()

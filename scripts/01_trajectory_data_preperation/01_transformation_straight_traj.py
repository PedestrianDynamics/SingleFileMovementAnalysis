"""
©Rudina Subaih
transforming the oval corridor trajectories to straight trajectories using the same formulas in Ziemer2016 with
some modifications
"""
import numpy as np
import os
from helper import transformation_coord
import time
import argparse


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description='transform 00_raw trajectories to straight trajectories (Ziemer2016)')
    parser.add_argument("-p", "--path", help='Enter the path of the trajectory file')
    parser.add_argument("-l", "--length", type=float, default=2.5, help='Enter the length (meter) of the straight part '
                                                                        'of the oval set-up (default=2.5)')
    parser.add_argument("-r", "--radius", type=float, default=1.85, help='Enter the radius (meter) of the corner in '
                                                                         'oval set-up (measured from the center of '
                                                                         'the corner circle to the middle of the '
                                                                         'corridor)(default=1.85)')
    return parser.parse_args()


if __name__ == '__main__':
    arg = get_parser_args()
    path = arg.path
    fig_name = os.path.basename(os.path.splitext(path)[0])
    length = arg.length
    r = arg.radius

    # record start time
    start = time.time()

    data = np.loadtxt(path, usecols=(0, 1, 2, 3, 4))
    data_new = np.empty((0, 5), int)

    for row in data:
        x_trans, y_trans = transformation_coord(row[2], row[3], length, r)
        data_new = np.append(data_new, np.array([[row[0], row[1], x_trans, y_trans, row[4]]]), axis=0)

    header = "#id\tfr\tx\ty\tz"
    np.savetxt("./%s_straight_traj.txt" % fig_name, data_new, delimiter='\t', header=header, comments='',
               newline='\r\n', fmt='%d\t%d\t%.4f\t%.4f\t%.4f')

    # record end time
    end = time.time()
    # print the difference between start
    # and end time in milli. secs
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")
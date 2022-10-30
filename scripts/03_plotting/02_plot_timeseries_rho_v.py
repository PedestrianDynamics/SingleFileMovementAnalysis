"""
©Rudina Subaih
Plot the states of pedestrians' velocity and density change over time (steady-state, transit state)
"""
import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description='Plot the change of velocity and density over time to find the steady '
                                                 'state')
    parser.add_argument("-p", "--pathfile", default="./", help='Enter the path of the vel_h_rho file (default="./")')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_parser_args()
    path = args.pathfile

    fig_name = os.path.basename(os.path.splitext(path)[0])
    data = pd.read_csv(path, comment="#", sep="\t", names=["ID", "FR", "x", "y", "z", "vel", "headway", "density"])

    fig = plt.figure(figsize=(6, 6))

    plt.plot(data.FR, data.density, 'r-', label="Density")
    plt.plot(data.FR, data.vel, 'b-', label="Velocity")

    plt.axvline(x=600, linestyle="--")
    plt.axvline(x=1600, linestyle="--")
    plt.legend()

    print("Minimum frame: ", data.FR.min())
    print("Maximum frame: ", data.FR.max())
    plt.xlabel(r" $\rm Time[Frame]$")
    plt.savefig("./%s_timeseries_rho_vel.pdf" % fig_name)
    plt.close()

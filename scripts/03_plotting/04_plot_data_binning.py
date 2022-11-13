"""
©Rudina Subaih
"""
import matplotlib.pyplot as plt
import numpy as np
import argparse


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="Plot the data binning for scatter data (headway-velocity) and "
                                                 "(rho-velocity)")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path of rho_vel_h data files",
        nargs="+"
    )
    parser.add_argument(
        "-lb",
        "--label",
        help="Enter the labels` texts of the data (plot legend)",
        nargs="+"
    )
    parser.add_argument(
        "-f",
        "--figName",
        help="Enter the name of figure file to save"
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Enter a title for the figure"
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


def binning_data(x_values, y_values, lb, ax):
    """
    binning the data and plot the errorbar plots
    :param x_values: x-axis values (independent variable values)
    :param y_values: y-axis values (dependent variable values)
    :param lb: texts. Label of plot
    :param ax: subplot name
    :return:
    """
    sort_x = x_values.copy()
    sort_x.sort()

    min_x = sort_x[0]
    max_x = sort_x[-1]
    ranges = np.arange(min_x, max_x, 0.2)

    y_mean = []
    x_mean = []

    y_std = []
    x_std = []

    r = len(ranges) - 1
    for group in range(r):
        v = y_values[(x_values >= ranges[group]) & (x_values <= ranges[group + 1])]
        rho = x_values[(x_values >= ranges[group]) & (x_values <= ranges[group + 1])]

        if (len(v) >= 0) and (len(rho) >= 0):
            y_mean.append(np.mean(v))
            y_std.append(np.std(v))
            x_mean.append(np.mean(rho))
            x_std.append(np.std(rho))

    ax.errorbar(x_mean, y_mean, xerr=x_std, yerr=y_std, label=lb,
                markerfacecolor="None")


if __name__ == "__main__":
    arg = get_parser_args()
    path_source = arg.path
    fig_name = arg.figName
    label = arg.label
    title = arg.title
    path_output = arg.pathOutput

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    for path_file, l in zip(path_source, label):
        print(path_file)
        data = np.loadtxt(path_file)
        binning_data(data[:, 7], data[:, 5], l, ax1)
        binning_data(data[:, 6], data[:, 5], l, ax2)

    # 1. rho-velocity figure
    ax1.set_xlabel(r"$\rm \rho(x_{i})~[m^{-1}]$")
    ax1.set_ylabel(r"$\rm v_{i}(t)~[m/s]$")
    ax1.legend()
    ax1.set_title(title)
    # ax1.set_xlim(0, 7)
    # ax1.set_ylim(-0.5, 2)

    fig1.savefig("%s/%s_binning_h_vel.png" % (path_output, fig_name))
    fig1.savefig("%s/%s_binning_h_vel.pdf" % (path_output, fig_name))
    plt.close(fig1)

    # 2. Headway-velocity figure
    ax2.set_xlabel(r"$\rm h(x_{i})~[m]$")
    ax2.set_ylabel(r"$\rm v_{i}(t)~[m/s]$")
    ax2.legend()
    ax2.set_title(title)
    # ax2.set_xlim(0, 5.5)
    # ax2.set_ylim(-0.5, 2)

    fig2.savefig("%s/%s_binning_rho_vel.png" % (path_output, fig_name))
    fig2.savefig("%s/%s_binning_rho_vel.pdf" % (path_output, fig_name))
    plt.close(fig2)

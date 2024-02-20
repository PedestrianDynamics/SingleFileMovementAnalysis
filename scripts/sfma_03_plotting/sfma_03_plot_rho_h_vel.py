"""
©Rudina Subaih
Plot the individual fundamental diagram (FD, rho-velocity relation) and the headway-velocity relation of pedestrians
    - for different experiments (make sure that for each experiment, the data of all runs are in the same 01_FD_germany_seyfried2005_all.txt file)
    - for the same experiment, different runs (provide the data of each run using a separate 01_FD_germany_seyfried2005_all.txt file)
"""
import argparse

import matplotlib.pyplot as plt
import pandas as pd


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="Plot FD (rho-vel) and headway-velocity relation")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path of vel_h_rho files (steady-state) directory"
    )
    parser.add_argument(
        "-n",
        "--fileName",
        help="Enter the files names of vel_h_rho files (steady-state)",
        nargs="+"
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Enter the title for the figure"
    )
    parser.add_argument(
        "-f",
        "--figName",
        help="Enter the name of figure file to save"
    )
    parser.add_argument(
        "-lb",
        "--label",
        help="Enter the labels` texts of the data (plot legend)",
        nargs="+"
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


def main():
    args = get_parser_args()
    path = args.path
    files = args.fileName
    title = args.title
    fig_name = args.figName
    labels = args.label
    path_output = args.pathOutput

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    for file, label, in zip(files, labels):
        data = pd.read_csv("%s/%s" % (path, file), sep='\t', comment='#',
                           names=["id", "fr", "x", "y", "z", "vel", "headway", "rho"])

        print("Plotting: %s%s" % (path, file))
        ax1.scatter(data["headway"], data["vel"], label=label, alpha=0.5)
        ax2.scatter(data["rho"], data["vel"], label=label, alpha=0.5)

    # ax1.set_xlim(-0.5, 2.5)
    # ax1.set_ylim(-0.6, 0.8)
    ax1.set_xlabel(r"$\rm h(x_{i})~[m]$")
    ax1.set_ylabel(r"$\rm v_{i}(t)~[m/s]$")
    ax1.legend()
    ax1.set_title(title)
    fig1.savefig("%s/%s_h_vel.png" % (path_output, fig_name))
    fig1.savefig("%s/%s_h_vel.pdf" % (path_output, fig_name))
    plt.close(fig1)

    # ax2.set_xlim(-0.5, 2.5)
    # ax2.set_ylim(-0.6, 0.8)
    ax2.set_xlabel(r"$\rm \rho(x_{i})~[m^{-1}]$")
    ax2.set_ylabel(r"$\rm v_{i}(t)~[m/s]$")
    ax2.legend()
    ax2.set_title(title)
    fig2.savefig("%s/%s_rho_vel.png" % (path_output, fig_name))
    fig2.savefig("%s/%s_rho_vel.pdf" % (path_output, fig_name))
    plt.close(fig2)


if __name__ == "__main__":
    main()
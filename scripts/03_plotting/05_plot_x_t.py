"""
©Rudina Subaih
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
    parser = argparse.ArgumentParser(description="Plot the x-t diagram (trajectories)")
    parser.add_argument(
        "-p",
        "--path",
        default="./",
        help="Enter the path of trajectory file (straight periodic trajectories)"
    )
    parser.add_argument(
        "-f",
        "--fps",
        default="25",
        type=int,
        help="Enter the frame rate of the videos"
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Enter the title of the figure"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_parser_args()
    path_file = args.path
    title = args.title
    fps = args.fps
    file_name = os.path.splitext(path_file)[0]

    fig = plt.figure(figsize=(6, 6))

    data = pd.read_csv(path_file, comment="#", sep="\t", names=["id", "fr", "x", "y", "z"])

    print("Start frame id:%s" % (data["fr"].max()))
    print("End frame ID:%s" % (data["fr"]).min())

    for ped_id in set(data["id"]):
        # Take only the trajectory for one person
        p_data = data.loc[data["id"] == ped_id]
        plt.scatter(p_data["x"], p_data["fr"] / fps, s=0.1, edgecolors="black", facecolors="black", marker=".")

    # plt.xlim(0, 16.62)
    # plt.ylim(0, 70)
    plt.title(title)
    plt.xlabel(r"Space [$\rm m$]")
    plt.ylabel(r"Time [$\rm sec.$]")
    plt.savefig(file_name + "_x_t.pdf")
    plt.savefig(file_name + "_x_t.png")
    plt.close()

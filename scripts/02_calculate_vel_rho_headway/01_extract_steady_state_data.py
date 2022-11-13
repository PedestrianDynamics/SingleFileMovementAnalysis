"""
©Rudina Subaih
to save only the steady-state data
"""
import argparse

import numpy as np


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="Extract steady-state data and save it inside a file")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path of rho_v files directory"
    )
    parser.add_argument(
        "-n",
        "--fileName",
        help="Enter the files names of rho_v files",
        nargs="+"
    )
    parser.add_argument(
        "-st",
        "--start",
        type=float,
        help="Enter the start frame of the steady state",
        nargs="+"
    )
    parser.add_argument(
        "-en",
        "--end",
        type=float,
        help="Enter the end frame of the steady state",
        nargs="+"
    )
    parser.add_argument(
        "-po",
        "--pathOutput",
        default="",
        help="Enter the path to save the output"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_parser_args()
    path = args.path  # The path of the rho_v directory
    files = args.fileName  # Names of the rho_v files
    starts = args.start  # start frame of the steady state for each file
    ends = args.end  # End frame of the steady state for each file
    path_output = args.pathOutput

    for file, st, en in zip(files, starts, ends):
        n = ["id", "fr", "x", "y", "z", "velocity", "headway", "rho"]
        header = "#id\tfr\tx\ty\tz\tvelocity\theadway\trho"
        fmt = "%d\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f"

        data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4, 5, 6, 7))

        rho_v = data[data[:, 1] > st]
        rho_v = rho_v[rho_v[:, 1] < en]

        np.savetxt(
            "%s/%s_steadystate.txt" % (path_output, file),
            rho_v,
            delimiter="\t",
            header=header,
            comments="",
            newline="\r\n",
            fmt=fmt
        )

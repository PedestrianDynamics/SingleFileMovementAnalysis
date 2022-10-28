"""
©Rudina Subaih
to save only the steady state data
"""
import argparse

import pandas as pd
from numpy import *


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description='Extraxt steady state data and save it inside a file')
    parser.add_argument("-p", "--path", help='Enter the path of rho_v files directory')
    parser.add_argument("-n", "--filename", help='Enter the files names of rho_v files', nargs="+")
    parser.add_argument("-st", "--start", type=float, help="Enter the start frame of the steady state", nargs='+')
    parser.add_argument("-en", "--end", type=float, help="Enter the end frame of the steady state", nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_parser_args()
    path = args.path  # The path of the rho_v directory
    files = args.filename  # Names of the rho_v files
    starts = args.start  # start frame of the steady state for each file
    ends = args.end  # End frame of the steady state for each file

    for file, st, en in zip(files, starts, ends):
        n = ["id", "fr", "x", "y", "z", "velocity", "headway", "rho"]
        header = "#id\tfr\tx\ty\tz\tvelocity\theadway\trho"
        fmt = '%d\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f'

        data = pd.read_csv("%s/%s" % (path, file), comment="#", sep="\t", names=n)

        rho_v = data.loc[data['fr'] > st]
        rho_v = rho_v.loc[rho_v['fr'] < en]

        spath = "%s/%s_steadystate.txt" % (path, file)
        savetxt(spath, rho_v, delimiter='\t', header=header, comments='', newline='\r\n', fmt=fmt)

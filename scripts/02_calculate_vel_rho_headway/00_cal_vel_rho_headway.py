"""
©Rudina Subaih
"""
import argparse
import glob
import os
import sys

import numpy as np
from helper import read_trajectory_data, individual_velocity_top_view, voronoi_rho_top_view, \
    individual_velocity_side_view, individual_headway_side_view, voronoi_rho_side_view
from experiments import EXPERIMENTS


def get_parser_args():
    """
    Arguments required from user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description="Calculate the movement quantities velocity, rho, and headway")
    parser.add_argument(
        "-p",
        "--path",
        help="Enter the path of directory that contain trajectory (straight transformed trajectory) files"
    )
    parser.add_argument(
        "-delta",
        "--deltaTime",
        type=float,
        default=0.4,
        help="Enter the time constant to calculate the velocity (default=0.4)")
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
    return parser.parse_args()


if __name__ == "__main__":
    args = get_parser_args()
    path = args.path
    delta_t = args.deltaTime
    exp_name = args.expName
    path_output = args.pathOutput
    sys.path.append(path)

    e = EXPERIMENTS[exp_name]
    fps = e.fps
    c = e.circumference
    camera_capture = e.camera_capture

    files = glob.glob("%s/*.txt" % path)

    for p_file in files:
        if len(p_file):
            file_name = os.path.splitext(p_file)[0]
            path = "%s/%s_vel_h_rho.txt" % (path_output, file_name)

            print("Info:\tCalculating: %s" % p_file)
            data = read_trajectory_data(p_file)

            # 1. For each frame, I need to calculate the speed, rho, and distances of pedestrians inside frame
            frames = np.sort(np.unique(data[:, 1]))
            frame_start = frames[0]
            frame_end = frames[-1]

            new_arr = np.empty((1, 8))

            for fr in frames:
                # Pedestrians inside the frame
                frame_data = data[data[:, 1] == fr]
                # A. Sort the row data by the position of pedestrians to know the order of the pedestrians in the
                # oval corridor (straight trajectories format)
                frame_data = frame_data[frame_data[:, 2].argsort()]

                # B. Calculate pedestrian velocity
                # TODO: calculation of clockwise experiment velocity?
                if camera_capture == 0:
                    velocity = individual_velocity_top_view(data, frame_data, delta_t, fr, frame_start,
                                                            frame_end, fps, c)
                    # C. Calculate pedestrians' headway
                    # Calculate the headway by taking the difference between each row x value and the previous
                    headway = np.diff(frame_data[:, 2])
                    # ... for the last pedestrian, we calculate it as
                    headway_last = (c - frame_data[-1, 2]) + (frame_data[0, 2])
                    headway = np.append(headway, headway_last)
                    # D. Calculate pedestrians' rho
                    rho = voronoi_rho_top_view(headway)
                else:
                    velocity = individual_velocity_side_view(data, frame_data, delta_t, fr, fps)
                    # C. Calculate pedestrians' headway
                    headway = individual_headway_side_view(frame_data)
                    # D. Calculate pedestrians' rho
                    rho = voronoi_rho_side_view(headway)

                # reshape the velocity, headway, rho
                velocity = np.reshape(velocity, (velocity.size, 1))
                headway = np.reshape(headway, (headway.size, 1))
                rho = np.reshape(rho, (rho.size, 1))

                # id, fr, x, y, z, velocity, headway, rho
                frame_data = np.append(frame_data, velocity, axis=1)
                frame_data = np.append(frame_data, headway, axis=1)
                frame_data = np.append(frame_data, rho, axis=1)

                new_arr = np.concatenate((new_arr, frame_data))

        else:
            print("Warning:\tPlease enter the full path of the source file.")
            sys.exit()

        result = new_arr[1:]
        # drop all nan-value rows
        result = result[~np.isnan(result).any(axis=1)]

        header = "#id\tfr\tx\ty\tz\tvelocity\theadway\trho"
        np.savetxt(path, result, fmt="%d\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f", delimiter="\t", header=header,
                   comments="", newline="\r\n")

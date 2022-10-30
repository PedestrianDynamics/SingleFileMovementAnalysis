"""
©Rudina Subaih
Making additional transformations for each experiment based on the coordinate system defined while extracting the
trajectories
"""
import argparse
import os

import numpy as np


def get_parser_args():
    """
    Required arguments from the user to input
    :return: parser of arguments
    """
    parser = argparse.ArgumentParser(description='transform the trajectories (x, y)')
    parser.add_argument("-p", "--path", help='Enter the path to the directory contains the trajectory files')
    parser.add_argument("-n", "--filename", help='Enter the trajectory file names', nargs="+")
    parser.add_argument("-expn", "--expName", help='Enter the experiment name: '
                                                   'BaSiGo_germany_Ziemer \n'
                                                   'schoolWDGMainCircle_germany_Wang \n'
                                                   'schoolGymBayMainCircle_germany_Wang \n'
                                                   'age_china_cao \n'
                                                   'gender_palestine_Subaih \n'
                                                   'caserne_germany_Seyfried \n'
                                                   'motivation_germany_lukowski')
    return parser.parse_args()


Experiment = {
    'BaSiGo_germany_Ziemer': "Description: \n"
                             "- Experiment: BaSiGo_germany_Ziemer \n"
                             "- Link: https://ped.fz-juelich.de/da/doku.php?id=basigosinglefile \n"
                             "- Transformation: rotate 90 degree, horizontal translation right, "
                             "vertical translation up",
    'schoolWDGMainCircle_germany_Wang': "Description: \n"
                                        "- Experiment: schoolWDGMainCircle_germany_Wang \n"
                                        "- Link: https://ped.fz-juelich.de/da/doku.php?id=start#single"
                                        "-file_motion_of_pupils \n "
                                        "- Transformation: reflection over y-axis, horizontal translation right 1.85, "
                                        "vertical translation up "
                                        "1.25",
    'schoolGymBayMainCircle_germany_Wang': "Description: \n"
                                           "- Experiment: schoolGymBayMainCircle_germany_Wang \n"
                                           "- Link: https://ped.fz-juelich.de/da/doku.php?id=start#single"
                                           "-file_motion_of_pupils \n "
                                           "- Transformation: rotate 90 degree, horizontal translation right "
                                           "1.85, vertical translation up 1.25"
                                           "1.25",
    'age_china_cao': "Description: \n"
                     "- Experiment: age_china_cao \n"
                     "- Link: https://ped.fz-juelich.de/db/lib/exe/detail.php?id=start&media=img"
                     ":ring_mixed_09_30_2382.jpg "
                     "\n- Transformation: (x, y, z) cm -> m, horizontal translation right 2.5, vertical "
                     "translation up 2.5",
    'gender_palestine_Subaih': "Description: \n"
                               "- Experiment: gender_palestine_Subaih \n"
                               "- Link: https://ped.fz-juelich.de/da/doku.php?id=gender_single_file \n"
                               "- Transformation: take only the data starting from 0 x-axis coordinate until 3.14",
    'caserne_germany_Seyfried': "Description: \n"
                                "- Experiment: caserne_germany_Seyfried \n"
                                "- Link: https://ped.fz-juelich.de/da/doku.php?id=corridor2 \n"
                                "- Transformation: measurement area data, horizontal translation right 2, take only "
                                "the data "
                                "starting from 0 until the length of the measurement area = 4m",
    'motivation_germany_lukowski': "Description: \n"
                                           "- Experiment: motivation_without_germany_lukowski \n"
                                           "- Transformation: add z-axis value = 0, (x, y, z) cm -> m, take only the "
                                        "data starting from 0 until the length of the measurement area = 2m",
    # 'schoolGymBayAncillaryCircle_germany_Wang': "Description: \n"
    #                                     "- Experiment: schoolGymBayAncillaryCircle_germany_Wang \n"
    #                                     "- Link: https://ped.fz-juelich.de/da/doku.php?id=start#single"
    #                                             "-file_motion_of_pupils \n "
    #                                     "- Transformation: (x, y, z) cm -> m, rotate 90 degree, horizontal translation"
    #                                             " right 1.85, vertical translation up 1.25"
}


def process_data(arr, experiment_name):
    """
    apply the additional transformation which is specific for each experiment
    :param arr: ndarray. Trajectory data
    :param experiment_name: string. Experiments name
    :return:
    """
    if experiment_name == "BaSiGo_germany_Ziemer":
        arr[:, 2], arr[:, 3] = arr[:, 3] + 1, -arr[:, 2] + 3
    elif experiment_name == "schoolWDGMainCircle_germany_Wang":
        arr[:, 2], arr[:, 3] = arr[:, 2] + 1.25, -arr[:, 3] + 1.85
    elif experiment_name == "schoolGymBayMainCircle_germany_Wang":
        arr[:, 2], arr[:, 3] = arr[:, 3] + 1.25, -arr[:, 2] + 1.85
    elif experiment_name == "age_china_cao":
        arr[:, 2], arr[:, 3], arr[:, 4] = (arr[:, 2] / 100) + 2.5, (arr[:, 3] / 100) + 2.5, arr[:, 4] / 100
    elif experiment_name == "gender_palestine_Subaih":
        arr = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4))
        # take only the data starting from 0 until the length pf the measurement area
        arr = arr[(arr[:, 2] >= 0) & (arr[:, 2] <= 3.14)]
    elif experiment_name == "caserne_germany_Seyfried":
        arr = arr[(arr[:, 2] >= -2) & (arr[:, 2] <= 2)]
        arr[:, 2] = arr[:, 2] + 2
    elif experiment_name == "motivation_germany_lukowski":
        arr = np.append(arr, [[0] for _ in range(len(arr[:, 0]))], axis=1)
        arr[:, 2], arr[:, 3], arr[:, 4] = (arr[:, 2] / 100), arr[:, 3] / 100, arr[:, 4] / 100
        arr = arr[(arr[:, 2] >= 0) & (arr[:, 2] < 2)]
    # elif experiment_name == "schoolGymBayAncillaryCircle_germany_Wang":
    #     arr[:, 2], arr[:, 3], arr[:, 4] = (arr[:, 2] / 100), arr[:, 3] / 100, arr[:, 4] / 100
    #     arr[:, 2], arr[:, 3] = arr[:, 3] + 1.25, -arr[:, 2] + 1.85
    return arr


if __name__ == '__main__':
    arg = get_parser_args()
    path = arg.path
    exp_name = arg.expName
    files = arg.filename

    for file in files:
        print("Transforming: %s/%s" % (path, file))
        file_name = os.path.splitext(file)[0]

        try:
            data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3, 4))
        except:
            data = np.loadtxt("%s/%s" % (path, file), usecols=(0, 1, 2, 3))

        print(Experiment[exp_name])
        data = process_data(data, exp_name)

        header = "#id\tfr\tx\ty\tz"
        np.savetxt("./%s_transformation_additional.txt" % file_name, data, delimiter='\t', header=header, comments='',
                   newline='\r\n', fmt='%d\t%d\t%.4f\t%.4f\t%.4f')

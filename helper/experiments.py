from dataclasses import dataclass
from typing import Optional


@dataclass
class ExperimentData:
    """
    Definition of experimental data:
    - link_data: link to the trajectory data file (open source). None => not open source.
    - shift_x: translations vertically.
    - shift_y: translations horizontally.
    - Unit: 100 if data are in cm. Otherwise 1.
    - ref_x: scalar to reflect x-axis. -1 to reflect.
    - ref_y: scalar to reflect y-axis. -1 to reflect.
    - x_rotate: index of the array. Rotation 90 degree (to make the x->y and the y ->x).
    - y_rotate: index of the array. Rotation 90 degree (to make the x->y and the y ->x).
    - id_col_index: index of the column contains ped. ID values. None=the traj. file don't contain the value.
    - fr_col_index: index of the column contains frame ID values. None=the traj. file don't contain the value.
    - x_col_index: index of the column contains x value.
    - y_col_index: index of the column contains y value.
    - z_col_index: index of the column contains z value. None=the traj. file don't contain the value.
    - additional_col_index: index of the column want to delete. None=>nothing to delete, you can add list of indexes.
    - Min: min boundary of the straight area (measurement area) (if applicable).
    - Max: max boundary of the straight area (measurement area) (if applicable).
    - fps: camera capture frame per second.
    - length: length of the straight part in the oval set-up.
    - radius: radius of the oval set-up.
    - circumference: circumference of the oval set-up.
    - camera_capture: 0 => top_view, 1 => side_view (default=0).
    - temporal: 0=> fps, 1 => time (sec.).
    - delimiter: related how the trajectories stored in the traj. file. " " OR ,
    - header: related how the trajectories stored in the traj. file. None=>no header, 0=>commented header, 1=> header is
    the first row without comments sign #
    """

    link_data: Optional[str] = "empty"
    shift_x: float = 0
    shift_y: float = 0
    unit: int = 1
    ref_x: int = 1
    ref_y: int = 1
    x_rotate: Optional[int] = 2
    y_rotate: Optional[int] = 3
    id_col_index: int = 0
    fr_col_index: int = 1
    x_col_index: int = 2
    y_col_index: int = 3
    z_col_index: int = 4
    additional_col_index: Optional[list] = None
    Min: Optional[float] = None
    Max: Optional[float] = None
    fps: int = 25
    length: float = 0
    radius: Optional[float] = 0
    circumference: Optional[float] = 0
    camera_capture: int = 0
    temporal: int = 0
    delimiter: str = " "
    header: int = 0


EXPERIMENTS = {
    "BaSiGo_germany_Ziemer": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2013.7",
        shift_x=1,
        shift_y=3,
        ref_y=-1,
        x_rotate=3,
        y_rotate=2,
        fps=16,
        length=4,
        radius=3,
        circumference=26.84,
        camera_capture=0
    ),
    "schoolWDGMainCircle_germany_Wang": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2014.2",
        shift_x=1.25,
        shift_y=1.85,
        ref_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "schoolGymBayMainCircle_germany_Wang": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2014.2",
        shift_x=1.25,
        shift_y=1.85,
        delimiter='\t',
        x_rotate=2,
        y_rotate=3,
        unit=1,
        ref_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "schoolGymBayAncillaryCircle_germany_Wang": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2014.2",
        unit=100,
        shift_x=1.25,
        shift_y=1.85,
        x_rotate=3,
        y_rotate=2,
        ref_x=-1,  # because this experiment is clockwise
        ref_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "schoolWDGAncillaryCircle_germany_Wang": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2014.2",
        unit=100,
        shift_x=1.25,
        shift_y=1.85,
        x_rotate=2,
        y_rotate=3,
        ref_x=-1,  # because this experiment is clockwise
        ref_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "age_china_Cao": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2017.1",
        shift_x=2.5,
        shift_y=2.5,
        unit=100,
        fps=25,
        length=5,
        radius=2.5,
        circumference=25.70,
        camera_capture=0
    ),
    "gender_palestine_Subaih": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2018.5",
        shift_x=0,
        shift_y=0,
        y_rotate=None,
        unit=1,
        ref_y=1,
        Min=0,
        Max=3.14,
        fps=25,
        length=3.14,
        camera_capture=1
    ),
    "caserne_germany_Seyfried": ExperimentData(
        link_data="https://doi.org/10.34735/ped.2006.1",
        shift_x=2,
        shift_y=0,
        y_rotate=None,
        unit=100,
        ref_y=1,
        Min=-2.0,
        Max=2.0,
        fps=25,
        length=4,
        camera_capture=1
    ),
    "motivation_germany_lukowski": ExperimentData(
        link_data="empty",
        y_rotate=None,
        unit=100,
        ref_y=1,
        Min=0,
        Max=2,
        fps=25,
        length=2,
        camera_capture=1
    ),
    "genderCroMa_setupRight_germany_paetzke": ExperimentData(
        link_data="empty",
        delimiter='\t',
        shift_x=-1.7,
        shift_y=4.6,
        ref_y=-1,
        x_rotate=1,
        y_rotate=0,
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=14.97,
        camera_capture=0
    ),
    "genderCroMa_setupLeft_germany_paetzke": ExperimentData(
        link_data="empty",
        delimiter='\t',
        shift_x=-1.7,
        shift_y=-1.3,
        ref_y=-1,
        x_rotate=1,
        y_rotate=0,
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=14.97,
        camera_capture=0
    ),
    "music_china_zeng2019": ExperimentData(
        link_data="empty",
        unit=100,
        shift_x=2.3,
        shift_y=1.9,
        x_rotate=2,
        y_rotate=3,
        fps=25,
        length=4.995975,
        radius=1.9,
        circumference=21.93,
        camera_capture=0
    ),
    "elderly_china_ren": ExperimentData(
        link_data="empty",
        shift_x=2.5,
        shift_y=2.5,
        ref_x=-1,  # because this experiment is clockwise
        x_rotate=2,
        y_rotate=3,
        fps=25,
        length=5,
        radius=2.5,
        circumference=25.7,
        camera_capture=0
    ),
    "heightConstrains_china_ma": ExperimentData(
        link_data="empty",
        fps=25,
        length=4,
        radius=2.4,
        circumference=28.08,
        camera_capture=0,
        temporal=1
    ),
    "simulation_pathfinder_4fps": ExperimentData(
        link_data="empty",
        shift_y=0.4,
        x_rotate=2,
        y_rotate=3,
        fps=4,
        length=2.3,
        radius=1.65,
        circumference=14.97,
        camera_capture=0,
        id_col_index=1,
        fr_col_index=None,
        x_col_index=2,
        y_col_index=3,
        z_col_index=None,
        additional_col_index=[0],
        delimiter=",",
        header=1
    ),
    "simulation_pathfinder_25fps": ExperimentData(
        link_data="empty",
        shift_y=0.4,
        x_rotate=2,
        y_rotate=3,
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=14.97,
        camera_capture=0,
        id_col_index=1,
        fr_col_index=None,
        x_col_index=2,
        y_col_index=3,
        z_col_index=None,
        additional_col_index=[0],
        delimiter=",",
        header=1
    ),
    "sim_jupedsim": ExperimentData(
        link_data="empty",
        unit=1,
        id_col_index=1,
        fr_col_index=0,
        x_col_index=2,
        y_col_index=3,
        z_col_index=None,
        additional_col_index=[4, 5],
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=14.97,
    ),
    "australia_left_MC": ExperimentData(
        link_data="empty",
        unit=1,
        fps=25,
        delimiter='\t',
        ref_x=-1,
        ref_y=-1,
        x_rotate=1,
        y_rotate=0,
        shift_x=3,
        shift_y=1.8,
        length=2.3,
        radius=1.65,
        circumference=14.97,
    ),
    "australia_right_MC": ExperimentData(
        link_data="empty",
        unit=1,
        fps=25,
        delimiter='\t',
        ref_x=-1,
        ref_y=-1,
        x_rotate=3,
        y_rotate=2,
        shift_x=3,
        shift_y=8,
        length=2.3,
        radius=1.65,
        circumference=14.97,
    ),
    "japan_MC": ExperimentData(
        link_data="empty",
        unit=1,
        fps=25,
        delimiter='\t',
        ref_x=-1,
        shift_x=1.3,
        shift_y=1.5,
        length=2.3,
        radius=1.65,
        circumference=14.97,
    ),
    "china_1_MC": ExperimentData(
        link_data="empty",
        unit=1,
        fps=25,
        ref_x=-1,
        ref_y=-1,
        x_rotate=3,
        y_rotate=2,
        delimiter='\t',
        shift_x=1.3,
        shift_y=1.5,
        length=2.3,
        radius=1.65,
        circumference=14.97,
    ),
    "china_2_MC": ExperimentData(
        link_data="empty",
        unit=1,
        fps=25,
        ref_x=-1,
        # ref_y=-1,
        x_rotate=3,
        y_rotate=2,
        delimiter='\t',
        shift_x=1.3,
        shift_y=1.5,
        length=2.3,
        radius=1.65,
        circumference=14.97,
    )
}

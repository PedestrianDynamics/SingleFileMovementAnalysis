from dataclasses import dataclass
from typing import Optional


@dataclass
class ExperimentData:
    """
    Definition of experimental data

    - link: to the data
    - shift_x and shift_y: for translations vertically and horizontally.
    - Unit: 100 if data are in cm. Otherwise 1.
    - inv_x and inv_y: scalar to reflect x-axis, and y-axis, respectively.
    - x_index and y_index: are indices of the array. Rotation 90 degree (to make the x->y and the y ->x)
    - Min and Max are boundary of the straight area (measurement area) (if applicable).
    """

    link: str
    shift_x: float = 0
    shift_y: float = 0
    unit: int = 1
    inv_x: int = 1  # -1 to reflect
    inv_y: int = 1  # -1 to reflect
    x_index: int = 2
    y_index: Optional[int] = 3
    Min: Optional[float] = None
    Max: Optional[float] = None
    fps: int = 25
    length: float = 0  # length of the straight part in the oval set-up
    radius: Optional[float] = 0
    circumference: Optional[float] = 0
    camera_capture: int = 0  # 0 => top_view, 1 => side_view (default=0)


EXPERIMENTS = {
    "BaSiGo_germany_Ziemer": ExperimentData(
        link="https://doi.org/10.34735/ped.2013.7",
        shift_x=1,
        shift_y=3,
        inv_y=-1,
        x_index=3,
        y_index=2,
        fps=16,
        length=4,
        radius=3,
        circumference=26.84,
        camera_capture=0
    ),
    "schoolWDGMainCircle_germany_Wang": ExperimentData(
        link="https://doi.org/10.34735/ped.2014.2",
        shift_x=1.25,
        shift_y=1.85,
        inv_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "schoolGymBayMainCircle_germany_Wang": ExperimentData(
        link="https://doi.org/10.34735/ped.2014.2",
        shift_x=1.25,
        shift_y=1.85,
        x_index=2,
        y_index=3,
        unit=1,
        inv_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "schoolGymBayAncillaryCircle_germany_Wang": ExperimentData(
        link="https://doi.org/10.34735/ped.2014.2",
        unit=100,
        shift_x=1.25,
        shift_y=1.85,
        x_index=3,
        y_index=2,
        inv_x=-1,  # because this experiment is clockwise
        inv_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "schoolWDGAncillaryCircle_germany_Wang": ExperimentData(
        link="https://doi.org/10.34735/ped.2014.2",
        unit=100,
        shift_x=1.25,
        shift_y=1.85,
        x_index=2,
        y_index=3,
        inv_x=-1,  # because this experiment is clockwise
        inv_y=-1,
        fps=25,
        length=2.5,
        radius=1.85,
        circumference=16.62,
        camera_capture=0
    ),
    "age_china_Cao": ExperimentData(
        link="https://doi.org/10.34735/ped.2017.1",
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
        link="https://doi.org/10.34735/ped.2018.5",
        shift_x=0,
        shift_y=0,
        y_index=None,
        unit=1,
        inv_y=1,
        Min=0,
        Max=3.14,
        fps=25,
        length=3.14,
        camera_capture=1
    ),
    "caserne_germany_Seyfried": ExperimentData(
        link="https://doi.org/10.34735/ped.2006.1",
        shift_x=2,
        shift_y=0,
        y_index=None,
        unit=1,
        inv_y=1,
        Min=-2.0,
        Max=2.0,
        fps=25,
        length=4,
        camera_capture=1
    ),
    "motivation_germany_lukowski": ExperimentData(
        link="empty",
        y_index=None,
        unit=100,
        inv_y=1,
        Min=0,
        Max=2,
        fps=25,
        length=2,
        camera_capture=1
    ),
    "genderCroMa_setupRight_germany_paetzke": ExperimentData(
        link="empty",
        shift_x=-1.7,
        shift_y=4.6,
        inv_y=-1,
        x_index=3,
        y_index=2,
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=14.97,
        camera_capture=0
    ),
    "genderCroMa_setupLeft_germany_paetzke": ExperimentData(
        link="empty",
        shift_x=-1.7,
        shift_y=-1.3,
        inv_y=-1,
        x_index=3,
        y_index=2,
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=14.97,
        camera_capture=0
    ),
    "music_china_zeng2019": ExperimentData(
        link="empty",
        unit=100,
        shift_x=2.3,
        shift_y=1.9,
        x_index=2,
        y_index=3,
        fps=25,
        length=4.995975,
        radius=1.9,
        circumference=21.93,
        camera_capture=0
    ),
    "elderly_china_ren": ExperimentData(
        link="empty",
        shift_x=2.5,
        shift_y=2.5,
        inv_x=-1,  # because this experiment is clockwise
        x_index=2,
        y_index=3,
        fps=25,
        length=5,
        radius=2.5,
        circumference=25.7,
        camera_capture=0
    ),
}

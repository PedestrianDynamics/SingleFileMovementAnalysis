from dataclasses import dataclass
from typing import Optional


@dataclass
class ExperimentData:
    """
    Definition of experimental data

    - link: to the data
    - shift_x and shift_y: for translations vertically and horizontally
    - Unit: 100 if data are in cm. Otherwise 1
    - inv_y: scalar to reflect y-axis.
    - x_index and y_index are indices of the array
    - Min and Max are boundary of the straight area (measurement area)
    """

    link: str
    shift_x: float = 0
    shift_y: float = 0
    unit: float = 1
    inv_x: int = 1
    inv_y: int = 1
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
        x_index=3,
        y_index=2,
        unit=1,
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
    "genderCroMa_germany_paetzke": ExperimentData(
        link="empty",
        shift_x=4.15,
        shift_y=-1.5,
        inv_x=-1,
        inv_y=1,
        x_index=3,
        y_index=2,
        fps=25,
        length=2.3,
        radius=1.65,
        circumference=16.62,
        camera_capture=0
    ),
}

from dataclasses import dataclass
from typing import Optional


@dataclass
class experiment_data:
    """
    Definition of experimental data

    link: to the data
    For translations with shift_x anf shift_y
    Unit: 100 if data are in cm. Otherwise 1
    inv_y: scalar to reflect y-axis.
    x_index and y_index are indeces of the array
    Min and Max are boundary of the straight area
    """

    link: str
    shift_x: float = 0
    shift_y: float = 0
    unit: float = 1
    inv_y: int = 1
    x_index: int = 2
    y_index: Optional[int] = 3
    Min: Optional[float] = None
    Max: Optional[float] = None


EXPERIMENTS = {
    "BaSiGo_germany_Ziemer": experiment_data(
        link="https://doi.org/10.34735/ped.2013.7",
        shift_x=1,
        shift_y=3,
        inv_y=-1,
        x_index=3,
        y_index=2,
    ),
    "schoolWDGMainCircle_germany_Wang": experiment_data(
        link="https://doi.org/10.34735/ped.2014.2",
        shift_x=1.25,
        shift_y=1.85,
        inv_y=-1,
    ),
    "schoolGymBayMainCircle_germany_Wang": experiment_data(
        link="https://doi.org/10.34735/ped.2014.2",
        shift_x=1.25,
        shift_y=1.85,
        x_index=3,
        y_index=2,
        unit=1,
        inv_y=-1,
    ),
    "age_china_Cao": experiment_data(
        link="https://doi.org/10.34735/ped.2017.1",
        shift_x=2.5,
        shift_y=2.5,
        unit=100,
    ),
    "gender_palestine_Subaih": experiment_data(
        link="https://doi.org/10.34735/ped.2018.5",
        shift_x=0,
        shift_y=0,
        y_index=None,
        unit=1,
        inv_y=1,
        Min=0,
        Max=3.14,
    ),
    "caserne_germany_Seyfried": experiment_data(
        link="https://doi.org/10.34735/ped.2006.1",
        shift_x=0,
        shift_y=2,
        y_index=None,
        unit=100,
        inv_y=1,
        Min=-2.0,
        Max=2.0,
    ),
    "motivation_without_germany_Lukowski": experiment_data(
        link="empty",
        shift_x=1,
        shift_y=0,
        y_index=None,
        unit=100,
        inv_y=1,
    ),
}

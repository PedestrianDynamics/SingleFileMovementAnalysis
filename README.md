# SingleFileMovementAnalysis

## Introduction
This repository contains scripts and [Jupyter notebooks](/notebooks) to analyze single-file movement experiments recorded by a top-view (straight, oval), or side-view camera.

**Example of top-view experiments**: [Gender Composition in Single-File Experiments](https://doi.org/10.34735/ped.2021.5). The analysis code of the experiment using  [Jupyter notebook](/notebooks/top_view_experiments.ipynb)

<p align="center">   
   <img src="notebooks/demo_data/croma_oval.png">
</p>

**Example of side-view experiments**: [Influence of gender in single-file movement](https://doi.org/10.34735/ped.2018.5). The analysis code of the experiment using [Jupyter notebook](/notebooks/side_view_experiments.ipynb)
   
<p align="center">
    <img src="notebooks/demo_data/gender_subaih2020.png" alt="Alternative text"/>
</p>

## Requirements

Download and install the requirements with

```bash
pip3 install -r requirements.txt
```

## Description of scripts

| Script | Description |
| --- | --- |
|[00_traj_file_format.py](scripts/01_trajectory_data_preperation/00_traj_file_format.py)| (optional) Trajectory data files have several format. This script extract some data from the raw file and unify the format of the data file for the later calculations.|
|[01_transformation_additional.py](scripts/01_trajectory_data_preperation/01_transformation_additional.py) | (optional) Trajectory data require some transformation (rotation , transition, etc). |
|[02_transformation_straight_traj.py](scripts/01_trajectory_data_preperation/02_transformation_straight_traj.py) | Transform oval to straight trajectory data according to [Ziemer et al.](https://doi.org/10.48550/arXiv.1602.03053) |
|[00_cal_vel_rho_headway.py](scripts/02_calculate_vel_rho_headway/00_cal_vel_rho_headway.py)|Calculate the individual velocity, headway, and 1D Voronoi density as [Subaih e al.](https://doi.org/10.1109/ACCESS.2020.2973917)|
|[01_extract_steady_state_data.py](scripts/02_calculate_vel_rho_headway/01_extract_steady_state_data.py)|Extract and to save only the steady state data|
|[00_plot_trajectories.py](scripts/03_plotting/00_plot_trajectories.py)|Plot the raw trajectory data or Plot the straight trajectory data after|
|[02_plot_timeseries_rho_v.py](scripts/03_plotting/02_plot_timeseries_rho_v.py)|Plot timeseries of density and velocity.|
|[03_plot_rho_h_vel.py](scripts/03_plotting/03_plot_rho_h_vel.py)|Plot fundamental diagram (FD, rho-vel), and headway-velocity|
|[04_plot_data_binning.py](scripts/03_plotting/04_plot_data_binning.py)|Plot bining data (rho-velocity) (headway-velocity)|
|[05_plot_x_t.py](scripts/03_plotting/05_plot_x_t.py)|Plot the spacial-temporal (x-t) relation|

## Example of the analysis results

- Determining the steady state [02_plot_timeseries_rho_v.py](scripts/03_plotting/02_plot_timeseries_rho_v.py)

![timeseries_rho_vel](https://user-images.githubusercontent.com/4458692/197458149-0b1a230c-38df-4303-b6a1-bd1e22ee4b88.png)


- The fundamental diagram (FD, rho-vel), and headway-velocity [03_plot_rho_h_vel.py](scripts/03_plotting/03_plot_rho_h_vel.py)

![schoolGymBay_rho_vel](https://user-images.githubusercontent.com/4458692/197454439-f8ad5ae2-10a6-453e-8251-d7edf31d6803.png)

![schoolGymBay_h_vel](https://user-images.githubusercontent.com/4458692/197454455-d8ddcd18-165d-4185-9f73-7ff91f85109d.png)


- The raw trajectories [00_plot_traj_raw.py](scripts/03_plotting/00_plot_trajectories.py)

![GymBay_main_15_1](https://user-images.githubusercontent.com/4458692/197454570-d407cd02-980c-454a-b352-d7cda753de8a.png)


- The trajectories after transformation [00_plot_traj_raw.py](scripts/03_plotting/00_plot_trajectories.py)

![GymBay_main_15_1_transformation_additional_straight_traj](https://user-images.githubusercontent.com/4458692/197454619-3804368f-82b1-4eaa-a725-42eb95e2e1b2.png)


- The spacial-temporal (x-t) relation [05_plot_x_t.py](scripts/03_plotting/05_plot_x_t.py)

![GymBay_main_15_1_transformation_additional_straight_traj_x_t](https://user-images.githubusercontent.com/4458692/197456105-15032699-9ef1-4c03-b1ca-d0e137260d9a.png)

- Binning data (rho-velocity) (headway-velocity) [04_plot_data_binning.py](scripts/03_plotting/04_plot_data_binning.py)

![schoole_GymBay_main_binning_h_vel](https://user-images.githubusercontent.com/4458692/197457493-2c1a78f8-96ff-4b4c-93da-cfce57e95497.png)

![schoole_GymBay_main_binning_rho_vel](https://user-images.githubusercontent.com/4458692/197457504-46f04bd9-1b74-4d31-aeac-558d1161bca5.png)

<!-- ## Example of experiments

|Experiment|Circumference (m)|Length of straight part (m)|Measurement area length (m)|Radius (m)|Frame per sec. (camera)|
| --- | --- | --- | --- | --- |  --- |
|[BaSiGo_germany_Ziemer](https://doi.org/10.34735/ped.2013.7)|26.84|4|-|3|16|
|[schoolWDGMainCircle_germany_Wang](https://doi.org/10.34735/ped.2014.2)|16.62|2.5|-|1.85|25|
|[schoolGymBayMainCircle_germany_Wang](https://doi.org/10.34735/ped.2014.2)|16.62|2.5|-|1.85|25|
|[age_china_Cao](https://doi.org/10.34735/ped.2017.1)|25.70|5|-|2.5|25|
|[gender_palestine_Subaih](https://doi.org/10.34735/ped.2018.5)|17.3|3.14|3.14|-|25|
|[caserne_germany_Seyfried](https://doi.org/10.34735/ped.2006.1)|26.84|4|4|-|25
|motivation_germany_lukowski|28.84|5|2|-|25|
|genderCroMa_germany_paetzke|14.96|2.3|-|1.65|25|

![penup_20221031_094831](https://user-images.githubusercontent.com/4458692/198972539-8f6fb110-e051-4316-968f-b879144e9fd7.jpg) -->

## Note
1. To run script, write on the command line: 
      ``bash
      PYTHONPATH="." python3 <CHILD DIRECTORY NAME>/<SCRIPT NAME>.py <ARGUMENTS>
      `` 
2. To calculate the velocity_headway_rho of top-view camera experiments that captured only the straight measurement
area such as the [Caserne experiment](https://ped.fz-juelich.de/da/doku.php?id=corridor2), we use the same analysis
methodology of side-view experiments.

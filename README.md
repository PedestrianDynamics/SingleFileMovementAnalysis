# SingleFileMovementAnalysis

## Introduction

This repository contains scripts for analyzing single-file movement experiments
recorded by a top-view (straight, oval), or side-view camera

- Example (top-view camera):
   - School GymBay, main circle.
   - [Link](https://ped.fz-juelich.de/da/doku.php?id=start#single-file_motion_of_pupils)

   ![gymbaymain](https://user-images.githubusercontent.com/4458692/197472324-e9e65cb2-3468-40f2-b7a3-a79d1d71868c.png)

- Example of (side-view camera)
   - Influence of gender in single-file movement.
   - [Link](https://ped.fz-juelich.de/da/doku.php?id=gender_single_file)
   
   ![gender_single_file_sample](https://user-images.githubusercontent.com/4458692/197808563-9babbeb4-ae5f-4401-b074-e81118d4f4eb.png)

Analysis results and trajectories used in this README can be download from this [link](https://fz-juelich.sciebo.de/s/6aWC04GmM0mKlTE).

## Requirements

Download and install the requirements  with

```bash
pip3 install -r requirements.txt
```

## Description of some scripts

| Script | Description |
| --- | --- |
| [00_transformation_additional.py](scripts/01_trajectory_data_preperation/00_transformation_additional.py) | Trajectory data may require some transformation (rotation , transition, etc). |
| [01_transformation_straight_traj.py](scripts/01_trajectory_data_preperation/01_transformation_straight_traj.py) | Transform oval to straight trajectory data accoring to [Ziemer](https://link.springer.com/chapter/10.1007/978-3-319-33482-0_12). |
|[00_cal_vel_rho_headway.py](scripts/02_calculate_vel_rho_headway/00_cal_vel_rho_headway.py)|Calculate the individual velocity, headway, and 1D Voronoi density.|
|[02_plot_timeseries_rho_v.py](scripts/03_plotting/02_plot_timeseries_rho_v.py)|Plot timeseries of density and speed.|
|[01_extract_steadyState_data.py](scripts/02_calculate_vel_rho_headway/01_extract_steadyState_data.py)|extract the steady state data.|


## Example 

   - determining the steady state ``scripts/03_plotting/plot_timeseries_rho_v.py``
   ![timeseries_rho_vel](https://user-images.githubusercontent.com/4458692/197458149-0b1a230c-38df-4303-b6a1-bd1e22ee4b88.png)

   - the fundamental diagram (FD, rho-vel), and headway-velocity ``scripts/03_plotting/plot_rho_h_vel.py``
   ![schoolGymBay_rho_vel](https://user-images.githubusercontent.com/4458692/197454439-f8ad5ae2-10a6-453e-8251-d7edf31d6803.png)
   ![schoolGymBay_h_vel](https://user-images.githubusercontent.com/4458692/197454455-d8ddcd18-165d-4185-9f73-7ff91f85109d.png)

   - the trajectories ``scripts/03_plotting/plot_traj_raw.py``
   ![GymBay_main_15_1](https://user-images.githubusercontent.com/4458692/197454570-d407cd02-980c-454a-b352-d7cda753de8a.png)

   - the trajectories after transformation ``scripts/03_plotting/plot_traj_straight.py``
   ![GymBay_main_15_1_transformation_additional_straight_traj](https://user-images.githubusercontent.com/4458692/197454619-3804368f-82b1-4eaa-a725-42eb95e2e1b2.png)

   - the spacial-temporal (x-t) relation ``scripts/03_plotting/plot_x_t.py``
   ![GymBay_main_15_1_transformation_additional_straight_traj_x_t](https://user-images.githubusercontent.com/4458692/197456105-15032699-9ef1-4c03-b1ca-d0e137260d9a.png)

   - bining data (rho-velocity) (headway-velocity) ``scripts/03_plotting/plot_data_binning.py``
   ![schoole_GymBay_main_binning_h_vel](https://user-images.githubusercontent.com/4458692/197457493-2c1a78f8-96ff-4b4c-93da-cfce57e95497.png)
   ![schoole_GymBay_main_binning_rho_vel](https://user-images.githubusercontent.com/4458692/197457504-46f04bd9-1b74-4d31-aeac-558d1161bca5.png)

## Note

To calculate the velocity_headway_rho of top-view camera experiments that captured only the straight measurement
area such as the [Caserne experiment](https://ped.fz-juelich.de/da/doku.php?id=corridor2), we use the same analysis
methodology of side-view experiments.

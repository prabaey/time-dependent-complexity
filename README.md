# time-dependent-complexity
This repository contains the code needed to reproduce the results reported in "Time-dependent complexity characterisation of activity patterns in patients with Chronic Fatigue Syndrome". Additionally, it also contains our novel open-source data set which was used for evaluation.

## Data

The data folder contains all data recorded from 7 patients during a period of 3 weeks in three subfolders:
- data/activity: One CSV-file per patient, containing their activity counts. The timestamp in the "time" column indicates the start of the 1-minute interval in which the values in the "counts" column were obtained. Naming convention "activityx.csv", with x the patient identifier (ranging from 1 to 7).
- data/survey: One CSV-file per patient, containing the features recorded through the daily surveys. Naming convention "surveyx.csv", with x the patient identifier (ranging from 1 to 7). See features.md for an explanation of the meaning of the survey features and how to interpret the records. 
- data/functioning: 

Say something about raw activity recordings.

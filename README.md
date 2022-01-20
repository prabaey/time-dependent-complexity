# time-dependent-complexity
This repository contains the code needed to reproduce the results reported in "Time-dependent complexity characterisation of activity patterns in patients with Chronic Fatigue Syndrome". Additionally, it also contains our novel open-source data set which was used for evaluation.

**Link to paper on Arxiv/title of paper/...**

## Libraries

The "lib" folder contains two a number of files, each collecting a list of functions that can be used to reproduce some part of our results. 
- lib/complexity.py: Contains the implementation of the three complexity methods as described in the paper: the original allometric aggregation method, the adapted allometric aggregation method, and the time-dependent complexity method which extract an evolution of the fractal dimension over time ("complexity_evolution"). 
- lib/activity_counts.py: Contains a number of preprocessing steps which are needed to transform the raw accelerations (recorded along 3 orthogonal axes) into the activity counts. The function "activity_counts_pipeline" contains the exact order of preprocessing steps (including parameter choices) we applied to get our activity counts sequences that are accessible in the "data/activity" folder. 
- lib/helpers.py: ...

## Data

The data folder contains all data recorded from 7 patients during a period of 3 weeks in three subfolders:
- data/activity: One CSV-file per patient, containing their activity counts. The timestamp in the "time" column indicates the start of the 1-minute interval in which the values in the "counts" column were obtained. Naming convention "activityx.csv", with x the patient identifier (ranging from 1 to 7).
- data/survey: One CSV-file per patient, containing the features recorded through the daily surveys. Naming convention "surveyx.csv", with x the patient identifier (ranging from 1 to 7). See the file "features.md" for an explanation of the meaning of the survey features and how to interpret the records. 
- data/functioning: "functioning.md" contains a textual description of the ranking of the three weeks in terms of general functioning of a patient. The physician responsible for follow-up of the patient also provided a short description on why they came to their conclusions. Sometimes, physicians were able to rate the general functioning as a score out of 5, in that case this score is also mentioned. 

The activity counts are a processed version of the raw acceleration recordings, obtained by applying the function "activity_counts_pipeline" in "lib/activity_counts.py" to the recorded accelerations. As an input, this function needs a path to a CSV-file which contains the following columns:
- "Time" (timestamp)
- "X" (acceleration in gravitational units around the X axis)
- "Y" (acceleration in gravitational units around the Y axis)
- "Z" (acceleration in gravitational units around the Z axis)
The function also takes the sampling frequency in Hz as an input ("fs"), which is set to 50 Hz (the sampling frequency of our recordings) as a default. 

We only publish the processed activity counts, since the files containing the raw recordings are several GB large. These raw recordings are available upon request, just send an email to paloma.rabaey@ugent.be. 

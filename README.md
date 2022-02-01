# time-dependent-complexity

This repository contains the code needed to reproduce the results reported in the paper "Time-dependent complexity characterisation of activity patterns in patients with Chronic Fatigue Syndrome". Additionally, it also contains our novel open-source data set which was used for evaluation of our methods. 

<!--Put a link to the medRxiv paper once the paper has been submitted and this repo is made public, and tell them to refer to the paper if they use our dataset or our methods.-->

## Libraries

The "lib" folder contains three files, each collecting a list of functions that can be used to reproduce the results reported in our paper. 
- lib/complexity.py: Contains the implementation of the three complexity methods as described in the paper: the original allometric aggregation method, the adapted allometric aggregation method, and the time-dependent complexity method which extract an evolution of the fractal dimension over time ("complexity_evolution"). 
- lib/activity_counts.py: Contains a number of preprocessing steps which are needed to transform the raw accelerations (recorded along 3 orthogonal axes) into the activity counts. The function "activity_counts_pipeline" contains the exact order of preprocessing steps (including parameter choices) we applied to get our activity counts sequences that are accessible in the "data/activity" folder. 
- lib/helpers.py: Contains a number of helper functions for visualization of results and generation of additional statistics for the dataset. The use of these functions is illustrated in the Jupyter notebook "notebooks/code_example.ipynb", where we demonstrate how to reproduce the results reported in the paper, using the helper functions and the defined complexity methods. 

## Data

The data folder contains all data recorded from 7 patients during a period of 3 weeks in three subfolders:
- data/activity: One CSV-file per patient, containing their activity counts. The timestamp in the "time" column indicates the start of the 1-minute interval in which the values in the "counts" column were obtained. Naming convention "activityx.csv", with x the patient identifier (ranging from 1 to 7).
- data/survey: One CSV-file per patient, containing the features recorded through the daily surveys. Naming convention "surveyx.csv", with x the patient identifier (ranging from 1 to 7). See the file "features.md" for an explanation of the meaning of the survey features and how to interpret the records. 
- data/functioning.md: contains a textual description of the ranking of the three weeks in terms of general functioning of a patient. The physician responsible for follow-up of the patient also provided a short description on why they came to their conclusions (these are translated from Dutch). Sometimes, physicians were able to rate the general functioning as a score out of 5, in that case this score is also mentioned. 

The activity counts are a processed version of the raw acceleration recordings, obtained by applying the function "activity_counts_pipeline" in "lib/activity_counts.py" to the recorded accelerations. As an input, this function needs a path to a CSV-file which contains the following columns:
- "Time": timestamp
- "X": acceleration in gravitational units measured at the X axis
- "Y": acceleration in gravitational units measured at the Y axis
- "Z": acceleration in gravitational units measured at the Z axis

The function also takes the sampling frequency in Hz as an input ("fs"), which is set to 50 Hz (the sampling frequency of our recordings) as a default. 

We only publish the processed activity counts, since the files containing the raw recordings are several GB large. These raw recordings are available upon request, please send an email to paloma.rabaey@ugent.be. The [Axivity AX3](https://axivity.com/product/ax3) logging device was used to collect the raw recordings. Subjects wore these at their non-dominant wrist, following the orientation convention described in the AX3 documentation (lightning bold sign directed to the right). The sampling frequency was set to 50 Hz, while the sensitivity (the range of recorded accelerations) was set to +- 8g. 

The study through which this data was obtained was approved by the ethics committee of the University Hospital Ghent under file number B6702020000952. Written informed consent was provided by all participants. All data is anonymised and cannot be traced back to any participant. 

## Notebooks

This repository contains some Jupyter notebooks which aim to demonstrate how to obtain our results, by applying the functions found in the "lib" folder. We also provide some additional material, in which we elaborate on some issues with the complexity methods, which were shortly mentioned in the paper but were not yet addressed in detail.
- "code_example.ipynb": Shows how to reproduce the results reported in our paper by applying the functions from "lib/complexity.py" and "lib/helpers.py" to a single activity sequence. This also illustrates the use of these functions to anyone who would like to try them out on their own activity sequences. 
- "motivation_AAA_method.ipynb": Motivates the changes that were made to the original allometric aggregation method through examples. These changes, implemented in the AAA method, solve some of the instabilities and robustness issues the original method suffers from. 
- "day_night_artefacts.ipynb": Elaborates on the daily oscillations which occur in the evolution signals, as a result of the alternation between sleep and wake time. 

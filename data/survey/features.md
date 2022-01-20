# Description of daily surveys

## Practical information

All participants filled in a survey at the end of every day during the recording period. This survey was sent out via email at a time chosen by the patient, corresponding to
what they felt was the end of their day. The survey was conducted in Dutch, since this is the language spoken by all participants. The survey not only featured questions on 
symptom severity throughout the day, but also inquired about weartime of the monitor and the general types of activities the patients executed throughout the day. An illustrative example of one of the surveys (translated in English) can be found in the file "daily_survey_example.pdf".

While most questions were the same for all participants, an effort was made to **personalise** the surveys based on each patient's individual needs. In the intake interview, the 
responsible physician went over the baseline survey together with the patient and made some changes where relevant. For most patients, a distinction was made between days where 
they went to work and free days, so the impact of a free day on current and future indicators could be measured. In the case where a participant did not have any work days, this
distinction was not made. 

For most questions, patients could answer separately for three day segments: the morning (8:00 - 12:00), afternoon (12:00 - 18:00) and evening (18:00 - 23:00). This would allow
us to get an idea of how certain indicators can evolve throughout the day. Other questions were asked only once for the entire day.

The answers to the surveys were converted to feature vectors, which consist of **three entries per** full **day** during the recording period. These three entries represent the 
aforementioned day segments. The three daily feature values are identical if the feature was only questioned once a day. 

In the next section, we describe the meaning of each feature. 

## Feature description

The second to last column of the table below indicates the type of each feature, while the last column tells us the value it takes on when a survey entry is invalid (i.e. when it was not filled in for that day). 

|**name**|**explanation**|**granularity**|**type**|**missing entry**|
|--------|---------------|---------------|--------|-----------------|
|valid|indicates whether the entry is valid or not (not valid when survey was not filled in that day)|daily|boolean|false|
|late|indicates whether the entry was late (survey filled in after 8:00 the next day)|daily|boolean|false|
|weartime|indicates whether the correspondent was wearing the monitor or not|3 times/day|boolean|true|
|sleep_quality|sleep quality the previous night (1 = slept very badly/too little, 5 = slept very well)|daily|integer (1-5)|NaN|
|free_day|indicates whether the correspondent had a free day|daily|boolean|false|
|relaxation|amount of relaxation (1 = none, 5 = a lot)|daily|integer (1-5)|NaN|
|relaxation_type|type of relaxing activities carried out, types vary per participant|daily|integer list (range varies)|empty list|
|rest_FD|how well-rested they felt after a free day (1 = not well-rested at all, 5 = very well-rested)|daily|integer (1-5)|invalid: NaN, work day: 0|
|main_activity|main activity carried out on work days, types vary per participant|daily|integer (range varies)|invalid: NaN, free day: 0|
|phy_intense|(subjective) physical intensity of activity (1 = not intense at all, 5 = very intense)|3 times/day|integer (1-5)|NaN|
|fatigue|fatigue (1 = not fatigued at all, 5 = very fatigued)|3 times_day|integer (1-5)|NaN|
|pain|pain (1 = no pain at all, 5 = a lot of pain)|3 times/day|integer (1-5)|NaN|
|ment_intense|mental intensity of activity (1 = not intense at all, 5 = very intense)|3 times/day|integer (1-5)|NaN|
|satisfaction|satisfaction with what they achieved during the day (1 = not satisfied at all, 5 = very satisfied)|3 times/day|integer (1-5)|NaN|
|mood|general mood (1 = very bad, 5 = very good)|3 times/day|integer (1-5)|NaN|
|stress|stress levels (1 = no stress at all, 5 = a lot of stress)|3 times/day|integer(1-5)|NaN|
|medication|indicates whether the correspondent took any medication which lies outside of their prescribed daily dose|3 times/day|boolean|false|
|alcohol|alcohol use, relative to the average drinking behaviour of the correspondent (0 = None, 1 = Less than normal, 2 = As normal, 3 = More than normal)|3 times/day|integer (0-3)|NaN|

In the table above, "granularity" is used to indicate whether a feature was questioned three times a day or only once. If it was questioned only once a day, the feature is 
duplicated in the three entries that represent each day segment. Consider the following example, which shows the feature vector that contains the values of the features "sleep 
quality" and "pain" as they are recorded over two consecutive days. 

|**index**|**sleep_quality**|**pain**|
|-----|-----|-----|
|**0**|4|2|
|**1**|4|3|
|**2**|4|2|
|**3**|2|4|
|**4**|2|3|
|**5**|2|3|

On the first day, the patient indicated a sleep quality of 4/5 for the past night. In the morning, their pain levels were 2/5. In the afternoon and evening, they were 3/5 and 2/5 respectively. On the second day, the patient indicated a sleep quality of only 2/5 for the past night. Their pain levels were 4/5, 3/5 and 3/5 for the morning, afternoon and evening, respectively. 

## Personalised surveys

As mentioned, the surveys were personalised based on the needs of each patient. Mostly, this means that the types for the main_activity feature and the relaxation_type features vary per patient. Some other small changes are also possible, such as some features not being questioned as the patient indicated that this question was not relevant for them. 
We go over these changes for every patient, and also indicate which range of dates the survey spans. The timestamps are not present in the feature vectors, but all samples are 
chronological, and the survey was first filled in on the first full day of wearing the monitor. 

### Patient 1

Dates: 17/03/2021 - 06/04/2021

For this patient, a work day is a day where they went volunteering. 

main_activity feature can take on an integer from 1 - 3:
1. volunteering
2. relaxation
3. other

relaxation_type feature can take on an integer from 1 - 8: 
1. Sauna
2. Walking
3. Doing odd jobs around the house
4. Watching TV
5. Eutony
6. Music
7. Reading 
8. Resting 

### Patient 2

Dates: 10/10/2021 - 30/10/2021

main_activity feature can take on an integer from 1 - 4:
1. working from home
2. work (not from home)
3. relaxation
4. therapy (physiotherapist, general practitioner or psychologist)

relaxation_type feature can take on an integer from 1 - 8:
1. sports (e.g. running, intensive bike ride, workout,...)
2. physical activities (e.g. working in the garden, odd jobs, walk,...)
3. digital (e.g. watching TV, social media, gaming,...)
4. pure relaxation (e.g. meditation, listening to music, napping,...)
5. music (e.g. practicing an instrument)
6. meeting up (e.g. with friends, family,...)
7. reading
8. other

The medication feature is left out. 

### Patient 3

Dates: 04/04/2021 - 24/04/2021

The patient does not work and therefore does not make a distinction between free days and work days. The "free_day" and "relaxation_FD" features are removed. 

main_activity feature can take on an integer from 1 - 3:
1. household tasks
2. relaxation
3. other

relaxation_type feature can take on an integer from 1 - 8: 
1. sports (e.g. running, intensive bike ride, workout,...)
2. physical activities (e.g. working in the garden, odd jobs, walk,...)
3. digital (e.g. watching TV, social media, gaming,...)
4. pure relaxation (e.g. meditation, listening to music, napping,...)
5. music (e.g. practicing an instrument)
6. meeting up (e.g. with friends, family,...)
7. reading
8. children

### Patient 4

Dates: 22/03/2021 - 10/04/2021

main_activity feature can take on an integer from 1 - 4:
1. household tasks
2. work (not from home)
3. relaxation
4. other

relaxation_type feature can take on an integer from 1 - 8: 
1. sports (e.g. running, intensive bike ride, workout,...)
2. physical activities (e.g. working in the garden, odd jobs, walk,...)
3. digital (e.g. watching TV, social media, gaming,...)
4. pure relaxation (e.g. meditation, listening to music, napping,...)
5. music (e.g. practicing an instrument)
6. meeting up (e.g. with friends, family,...)
7. reading
8. other

The alcohol feature is left out. 

### Patient 5

Dates: 11/07/2021 - 31/07/2021

The patient does not go to work and therefore does not make a distinction between free days and work days. The "free_day" and "relaxation_FD" features are removed. 

main_activity feature can take on an integer from 1 - 4:
1. working from home (household tasks, administration,...)
2. relaxation
3. sport (fitness, swimming,...)
4. other

relaxation_type feature can take on an integer from 1 - 7: 
1. physical activities (e.g. working in the garden, odd jobs, walk,...)
2. digital (e.g. watching TV, social media, gaming,...)
3. pure relaxation (e.g. meditation, listening to music, napping,...)
4. music (e.g. practicing an instrument)
5. meeting up (e.g. with friends, family,...)
6. reading
7. napping

The medication and alcohol features are left out. 

### Patient 6

Dates: 21/04/2021 - 10/05/2021

The patient does not go to work and therefore does not make a distinction between free days and work days. The "free_day" and "relaxation_FD" features are removed. 

main_activity feature can take on a **list** of integers from 1 - 7 (this patient requested to be able to indicate multiple activities per day segment, which is different from other patients):
1. working in the garden
2. walking
3. cooking
4. shopping
5. practical activities
6. relaxation
7. other

relaxation_type feature can take on an integer from 1 - 4: 
1. watching TV
2. gaming
3. reading
4. resting

The medication and alcohol features are left out.

### Patient 7

Dates: 14/03/2021 - 02/04/2021

main_activity feature can take on an integer from 1 - 4:
1. working from home
2. work (not from home)
3. relaxation
4. was supposed to work, but did not (due to illness)

relaxation_type feature can take on an integer from 1 - 8: 
1. sports (e.g. running, intensive bike ride, workout,...)
2. physical activities (e.g. working in the garden, odd jobs, walk,...)
3. digital (e.g. watching TV, social media, gaming,...)
4. pure relaxation (e.g. meditation, listening to music, napping,...)
5. music (e.g. practicing an instrument)
6. meeting up (e.g. with friends, family,...)
7. reading
8. other

The alcohol feature is left out. 

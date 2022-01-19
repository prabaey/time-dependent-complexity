import pandas as pd
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfilt

def read_csv(filename, chunksize=4320000):

    """
    Read the raw accelerations (recorded around the X, Y and Z axis) from a csv file into a pandas dataframe.

    :param filename: path to the csv file
    :param chunksize: how many rows to read in at a time (can be necessary to read the csv in chunks due to memory constraints), default size of ~ 1 day
    
    return: the dataframe containing the X, Y and Z accelerations, indexed by the timestamps
    """
    
    sig = pd.DataFrame()
    for chunk in pd.read_csv(filename, names=["Time", "X", "Y", "Z"], parse_dates=True, index_col="Time", dtype={"X": np.float32, "Y": np.float32, "Z": np.float32}, chunksize=chunksize):
        sig = pd.concat([sig, chunk]) # read in chunk by chunk, concatenating the dataframes together

    return sig


def aggregation_metric(df, metric="enmo"):

    """
    Aggregates the accelerations recorded around the three axes into one metric.

    :param df: dataframe containing the X, Y and Z accelerations, indexed by the timestamps
    :param metric: which metric to use to aggregate the accelerations. options: 
        - enmo: calculates the vector magnitude and removes the gravitational component by subtracting with 1
        - magnitude: calculates the vector magnitude, WITHOUT removing gravitational component. please ensure that this component
                        is still removed in a further step (e.g. by using a bandpass filter to remove the DC component)
        - diff: first removes the gravitational DC component by differencing the subsequent values in the sequence, 
                then aggregates the three axes into their vector magnitude

    return: the transformed dataframe, appended with a new column "R" containing the vector magnitude (and "ENMO" containing the enmo
            metric when that option is selected). note that the "X", "Y" and "Z" columns should not be used again from here on out, as 
            they have been transformed along with the metric chosen for aggregation. 
    """

    if (metric == "enmo"):
        df["R"] = np.sqrt(df["X"] ** 2 + df["Y"] ** 2 + df["Z"] ** 2)
        df["ENMO"] = df["R"] - 1
        df["ENMO"] = (df["ENMO"] > 0) * df["ENMO"]

    elif (metric == "magnitude"):
        df["R"] = np.sqrt(df["X"] ** 2 + df["Y"] ** 2 + df["Z"] ** 2)

    elif (metric == "diff"):
        df = df[["X", "Y", "Z"]].diff()
        df["R"] = np.sqrt(df["X"] ** 2 + df["Y"] ** 2 + df["Z"] ** 2)

    else:
        raise Exception("Unknown type of metric")

    return df


def butter_filter(signal, lowcut, highcut, fs, order=5):

    """
    Applies a bandpass filter (implemented as a butterworth filter) to filter out high noise frequencies and (if a lowcut frequency is set)
    the gravitational component. This way, only the accelerations which were initiated by the subject are isolated. 

    :param signal: column of activity dataframe on which to apply the filter, will usually refer to the "R" column (vector magnitude)
    :param lowcut: everything below this frequency is filtered out. if zero, low frequencies are all kept in (only use this setting if the gravitational
                    component has been removed earlier on by differencing or enmo!)
    :param highcut: everything above this frequency is filtered out
    :param fs: sampling frequency of the original signal (in Hz)
    :param order: which order of the butterworth filter to apply (higher order = sharper filtering cutoff)

    return: the filtered version of "signal" (can be used to replace original column in the dataframe)
    """

    # create filter
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if (lowcut == 0):  # lowpass filter
        sos = butter(order, high, analog=False, btype='low', output='sos')
    else:  # bandpass filter
        sos = butter(order, [low, high], analog=False, btype='band', output='sos')

    # apply filter (forward and backward pass)
    filtered = sosfiltfilt(sos, signal)

    # if filtered created negative values, these should be corrected to zero
    filtered = (filtered > 0) * filtered

    return filtered


def calculate_counts(df, epoch, col="ENMO"):

    """
    Calculates the activity counts (as defined by Actigraph) by aggregating (filtered) accelerations per epoch and transforming to counts.

    :param df: dataframe containing the X, Y and Z accelerations, as well as the vector magnitude/ENMO column, indexed by the timestamps
    :param epoch: size of segments in which the accelerations are aggregated, represented as a string (e.g. "1S" represents 1 second epochs)
    :param col: specify the name of the column which contains the aggregation metric for which we want to obtain the counts

    return: the original dataframe, including an extra column containing the calculated counts
    """

    resampled = df.resample(epoch).mean()  # divide signal into segments of size "epoch" and calculate the mean

    # range = +- 8g and 10 bits used for analog conversion
    resolution = 16 / (2 ** 10)
    resampled["counts"] = resampled[col] / resolution # transform to activity counts 

    return resampled


def aggregate_counts(df, interval):

    """
    Further aggregate the counts into larger intervals, if needed. 

    :param df: dataframe containing the counts
    :param interval: size of segments in which the counts are aggregated (e.g. "5T" represents 5 minute intervals)

    return: the resampled dataframe, containing one activity count value for each interval of specified size
    """

    recounted = df.resample(interval).sum()  # summing all counts in interval

    return recounted


# approximation and simplification of the pipeline Actigraph software uses to calculate the activity counts
def actigraph_pipeline(filename):

    """
    Pipeline we used to obain our counts sequences from the raw acceleration recordings. The structure of the pipeline is based on 
    the one used in Actigraph devices.

    :param filename: path to the csv file containing the recorded accelerations in the form of 4 columns: "Time", "X", "Y" and "Z"
    
    return: dataframe cpm containing one column "counts", indexed by the timestamp signaling the start of the interval for which the counts 
            were extracted
    """

    sig = read_csv(filename)
    sig = aggregation_metric(sig, metric="magnitude")
    sig["R"] = butter_filter(sig["R"], 1/60, 2.5, 50)
    counts = calculate_counts(sig, "1S", col="R")
    cpm = aggregate_counts(counts, "1T")

    return cpm[["counts"]]
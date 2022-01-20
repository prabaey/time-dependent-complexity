import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from scipy.stats.stats import pearsonr

def read_counts(patient_id):
    """
    Reads in CSV file containing activity counts and puts them in a dataframe, indexed by the timestamps.

    :param patient_id: which patient's activity counts are read from memory

    return: a Pandas dataframe containing the 1-minute counts sequence, indexed by the timestamps (indicating the start of the interval
    represented by the counts value)
    """
    filename = "data/activity/activity"+str(patient_id)+".csv"
    counts_df = pd.read_csv(filename, names=["Time", "counts"], parse_dates=True, index_col="Time", skiprows=1)
    return counts_df


def calculate_mean_std(df):
    """
    Calculates the mean and std of the daily activity counts. 
    Daily counts are defined as the total sum of all counts recorded within a 24-hour period.

    :param df: dataframe containing the activity counts

    return: mean and std of the daily counts
    """
    counts = df["counts"]
    day = 24*60 # one day is simply defined as this amount of 1-minute intervals
    daily_counts = []
    for i in range(len(counts)//day): # the last day is not counted, as it will not be full
        start = i*day
        end = (i+1)*day
        daily = counts.iloc[start:end]
        daily_counts.append(daily.sum()) # daily sum of counts
    return np.mean(daily_counts), np.std(daily_counts)


def visualize_across_scales(scales, fractal_dim):
    """
    Visualizes the variation of the fractal dimension across scales.

    :param scales: range of scales for which the fractal dimension was calculated
    :param fractal_dim: fractal dimensions corresponding to the scale on the same index in param scales
    """
    fig, ax = plt.subplots(1, figsize=(10,5))
    plt.plot(np.array(scales)/60, fractal_dim)
    plt.gca()
    plt.ylim(1, 1.5)
    plt.grid()
    plt.xlabel("scale in hours")
    plt.ylabel("fractal dimension")
    plt.title("variation of the fractal dimension across scales")
    plt.show()


def compare_static_dims(scales, fractal_dim_dict):
    """
    Plots a comparison of the fractal dimension for the full recording period, and the first, second and third week.
    
    :param scales: range of scales for which the fractal dimensions were calculated
    :param fractal_dim_dict: dictionary containing the list of fractal dimensions obtained for the following 4 cases:
                             - full recording period: "full"
                             - first week: "week1"
                             - second week: "week2"
                             - third week: "week3"
                             each fractal dimension corresponds to the scale on the same index in param scales
    """
    fig, ax = plt.subplots(1)
    plt.plot(np.array(scales[18:])/60, fractal_dim_dict["full"][18:], label="global")
    plt.plot(np.array(scales[18:])/60, fractal_dim_dict["week1"][18:], label="week 1")
    plt.plot(np.array(scales[18:])/60, fractal_dim_dict["week2"][18:], label="week 2")
    plt.plot(np.array(scales[18:])/60, fractal_dim_dict["week3"][18:], label="week 3")
    plt.legend()
    plt.ylim(1, 1.5)
    plt.xlabel("scale in hours")
    plt.ylabel("fractal dimension")
    plt.title("Comparison of the fractal dimension for various weeks")
    plt.show()

def plot_complexity_evolution(complexity, time, static_dict, functioning, height_legend):
    """
    Plots the evolution of the fractal dimension over time for a 3-hour scale. Compares this to the static fractal dimensions obtained
    for the three separate weeks, as well as to the ranking of the weeks in terms of functioning. 

    :param complexity: 2D-array of fractal dimensions (contains an array of fractal dimensions for various scales, for each timestamp in "time"),
                       representing the evolution of the fractal dimension of the activity counts within consecutive 3-day windows
    :param time: 1D-array of timestamps (datetime objects) indicating the end of the 3-day window for which each range of fractal dimensions 
                 in the "complexity" matrix is obtained
    :param static_dict: dictionary containing the list of fractal dimensions (across various scales) obtained for the 3 separate weeks. contains at
                        least the entries "week1", "week2", "week3".
    :param functioning: a list containing the ranking of the weeks in terms of functioning. The first index corresponds to the first week, and so on.
                        0 signifies the best week, 1 the average week and 2 the worst week. 
    :param height_legend: decides at which height to place the legend, so it doesn't overlap with the plot. should be float between [1.0, 1.5]
    """

    idx = 35
    scale = "3h"
    
    plt.figure(figsize=(20,5))
    
    color = np.array(["forestgreen", "orange", "indianred"])
    plt.axvspan(time[0], time[4*12+24*12*4], facecolor=color[functioning[0]], alpha=0.07)
    plt.axvspan(time[4*12+24*12*4], time[4*12+24*12*4+24*12*7], facecolor=color[functioning[1]], alpha=0.07)
    plt.axvspan(time[4*12+24*12*4+24*12*7], time[-1], facecolor=color[functioning[2]], alpha=0.07)
    
    plt.axvline(time[0], linestyle="dashdot", linewidth=1, color="black")
    plt.axvline(time[4*12+24*12*4], linestyle="dashdot", linewidth=1, color="black")
    plt.axvline(time[4*12+24*12*4+24*12*7], linestyle="dashdot", linewidth=1, color="black")
    plt.axvline(time[-1], linestyle="dashdot", linewidth=1, color="black")
    
    plt.plot(time, complexity[:,idx])
    
    plt.hlines(y=static_dict["week1"][idx], xmin=time[0], xmax=time[4*12+24*12*4], linewidth=1.5, label="Week 1: "+str(np.round(static_dict["week1"][idx+1], 3)), linestyle="dashed", color="black")
    plt.hlines(y=static_dict["week2"][idx], xmin=time[4*12+24*12*4], xmax=time[4*12+24*12*4+24*12*7], linewidth=1.5, label="Week 2: "+str(np.round(static_dict["week2"][idx+1], 3)), linestyle="dashed", color="black")
    plt.hlines(y=static_dict["week3"][idx], xmin=time[4*12+24*12*4+24*12*7], xmax=time[-1], linewidth=1.5, label="Week 3: "+str(np.round(static_dict["week3"][idx+1], 3)), linestyle="dashed", color="black")
    
    ax = plt.gca()
    
    description = ["Best week", "Average week", "Worst week"]
    t = ax.text(time[30*12], height_legend, "Week 1: "+str(np.round(static_dict["week1"][idx+1], 3))+"\n"+description[functioning[0]], size=12, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="grey", lw=1, alpha=0.5))
    t = ax.text(time[24*12*7], height_legend, "Week 2: "+str(np.round(static_dict["week2"][idx+1], 3))+"\n"+description[functioning[1]], size=12, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="grey", lw=1, alpha=0.5))
    t = ax.text(time[24*12*14-100], height_legend, "Week 3: "+str(np.round(static_dict["week2"][idx+1], 3))+"\n"+description[functioning[2]], size=12, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="grey", lw=1, alpha=0.5))
    
    plt.ylim(1,1.5)
    plt.grid(linestyle="--")

    plt.xlabel("date")
    plt.ylabel("fractal dimension")
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

    plt.title("Evolution of fractal dimension over time, for a 3-hour scale")
    
    plt.show()


def sliding_window_activity(sig, width, step):
    """
    Calculate the evolution of the sum of the activity counts contained within each window of length width. This list of activity counts signifies
    the total sum of counts within each activity sequence for which the fractal dimension is obtained in the "complexity_evolution" method with the 
    same arguments. The timestamps line up with the timestamps outputted by the corresponding execution of the "complexity_evolution" method, allowing
    the user to plot the evolution of both the activity counts and the fractal dimension at the same time, and compare the two metrics. 

    :param sig: dataframe containing the activity counts and the timestamps these correspond to (the start of the 1-minute interval
                for which these were obtained)
    :param width: width of the window which slides over the sequence and calculates the sum of the activity counts for the activity sequence 
                    contained within it. this is described as a string from which a Timedelta can be extracted (e.g. "3 days")
    :param step: the step size with which to advance the window. this is described as a string from which a Timedelta can be extracted (e.g. "5 min")

    return: list "aggregated_activity", containing the total counts enclosed within the window ending at the corresponding timestamp in "timestamps"
    """

    window = pd.Timedelta(width)
    start = sig.index[0]
    end = start + window
    aggregated_activity = []
    timestamps = []
    
    while(end < sig.index[-1]): 

        count_sum = sig["counts"][start:end].sum()
        aggregated_activity.append(count_sum)
        timestamps.append(end)
        start += pd.Timedelta(step)
        end = start + window

    timestamps = pd.to_datetime(timestamps)
    timestamps = timestamps.to_pydatetime()

    return np.array(aggregated_activity), np.array(timestamps)


def plot_activity_complexity(evol_compl, evol_activity, timestamps):

    """
    Plots the evolution of the fractal dimension over time for a 3-hour scale. Compares this to the corresponding evolution of the summed activity
    counts from which these fractal dimensions were obtained. 

    :param evol_compl: 2D-array of fractal dimensions (contains an array of fractal dimensions for various scales, for each timestamp in "timestamps"),
                       representing the evolution of the fractal dimension of the activity counts within consecutive 3-day windows
    :param evol_activity: 1D-array of summed activity counts, representing the intensity of activity within consecutive 3-day windows
    :param timestamps: 1D-array of timestamps (datetime objects) indicating the end of the 3-day window for which each range of fractal dimensions 
                       in the "evol_compl" matrix and the activity counts in the "evol_activity" array were obtained
    """

    fig, ax1 = plt.subplots(figsize=(20, 5))

    ax1.plot(timestamps, evol_compl[:,35], label="3 hour complexity")
    ax1.set_xlabel("date")
    ax1.set_ylabel("fractal dimension")
    ax1.set_ylim(1, 1.5)
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()

    ax2.plot(timestamps, evol_activity, label="activity")
    ax2.set_ylabel("activity counts")
    ax2.legend(loc="upper right")

    plt.title("Comparison of evolution of summed activity counts and evolution of the fractal dimension")
    fig.tight_layout()
    plt.show()

def scatter_activity_complexity(evol_compl, evol_activity):
    """
    Sample both the complexity evolution signal (3 hour scale) and the activity evolution signal three times a day, and compare the calculate the Pearson 
    correlation between the corresponding samples. Also visualize the scatter plot of this relation. 

    :param evol_compl: 2D-array of fractal dimensions (contains an array of fractal dimensions for various scales, for each timestamp in "timestamps"),
                       representing the evolution of the fractal dimension of the activity counts within consecutive 3-day windows
    :param evol_activity: 1D-array of summed activity counts, representing the intensity of activity within consecutive 3-day windows, aligned with the 
                          corresponding fractal dimensions in "evol_compl"
    """

    plt.figure()

    x = evol_compl[:,35][::96] # take a sample every 8x12 datapoints (twelve 5-minute intervals in an hour, three 8-hour segments in a day)
    y = evol_activity[::96]

    plt.scatter(x, y)
    plt.xlabel("fractal dimension")
    plt.ylabel("3-day sum of activity counts")
    plt.title("scatter plot")
    plt.xlim(1, 1.5)
    plt.show()

    return pearsonr(x, y)[0]
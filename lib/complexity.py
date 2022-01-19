import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import numpy.polynomial.polynomial as poly

def allometric_aggregation(seq, n_max, draw=True):
    """
    The original allometric aggregation algorithm as defined by West. Returns the fractal dimension of a time series 
    and the log-log plot from which this was extracted.

    :param seq: numpy array of equidistant signal values, in our case 1-minute activity counts sequence
    :param n_max: maximal level of aggregation
    :param draw: a boolean indicating whether or not to draw the log-log plot and the estimated slope, default value True

    return: the fractal dimension of the sequence (float)
    """

    # perform aggregation for n (number of aggregated data points) ranging from 1 to n_max
    means = np.zeros(n_max)
    variances = np.zeros(n_max)

    for n in range(1, n_max + 1):

        rescaled = []
        i = 0
        # all blocks except for maybe the last one will aggregate n datapoints,
        # the last block aggregates the remainder of the data points, which is not always equal to n
        # this can lead to end effects, which make the method unstable when applied to shorter sequences
        while i < len(seq):
            agg = sum(seq[i:i+n])
            rescaled.append(agg)
            i += n
        # calculate mean and variance for all levels of aggregation
        means[n-1] = np.mean(rescaled)
        variances[n-1] = np.var(rescaled)

    # calculate slope of relation between mean and variance
    b, a, r_value, p_value, std_err = stats.linregress(np.log(means), np.log(variances))

    # draw fitted line
    if (draw):
        fig, ax = plt.subplots(1)
        plt.scatter(means, variances)
        plt.plot(means, np.exp(a) * means ** b, color='red')
        ax.set_yscale("log")
        ax.set_xscale("log")
        plt.xlabel("mean")
        plt.ylabel("variance")

    # calculate fractal dimension
    D = 2 - b / 2

    return D


def adapted_allometric_aggregation(seq, n_min, n_max, s=1.1, draw=True):
    """
    The adapted allometric aggregation algorithm. Returns the fractal dimension of a time series for various scales 
    and the log-log plot from which these were extracted. We draw attention to the changes that were made compared to the original
    allometric aggregation algorithm in the comments. 

    :param seq: numpy array of equidistant signal values, in our case 1-minute activity counts sequence
    :param n_min: minimal level of aggregation
    :param n_max: maximal level of aggregation
    :param s: factor controlling the spread of the aggregation levels within the interval [n_min, n_max], default value 1.1
    :param draw: a boolean indicating whether or not to draw the log-log plot and the estimated polynomial, default value True

    return: the fractal dimension of the sequence (float) for every level n in scales
    """

    means = []
    variances = []
    scales = []
    n = n_min # the first aggregation step aggregates n_min samples
    
    while n <= n_max:

        step = max(1, int(n/16)) # some overlap is now allowed in the aggregated segments of size n
                                    # if step would be equal to n, we would allow no overlap like in the original AA algorithm
                                    # now, step is at least 16 times smaller than n, generating 16 times more segments 
                                    # (now partially overlapping) to estimate mean and var from
        rescaled = []
        i = 0
        
        while i < len(seq)-n+step: # every segment always contains n samples, except for the last one, which contains at least 15/16*n samples
                                    # this ensures a reliable calculation of the mean and variance, avoiding end effects
            agg = sum(seq[i:i+n])
            rescaled.append(agg)
            i += step # sliding window moves forward with steps smaller than n, allowing the segments to overlap
        
        means.append(np.mean(rescaled))
        variances.append(np.var(rescaled))
        scales.append(n) # keep track of the scales we explored within the interval [n_min, n_max]
        
        n = int(np.ceil(n*s)) # increase aggregation level n with factor s to ensure even spreading of the 
                                # mean-variance datapoints on the log-log plot
                                # this makes the fit of the polynomial better adjusted to all scales, rather than biased towards the higher scales

    means = np.array(means)
    variances = np.array(variances)

    # fit third-order polynomial to the means and variances in log-log space
    fitted_poly = poly.Polynomial.fit(np.log(means), np.log(variances), 3)
    coeff = fitted_poly.convert().coef

    # draw fitted polynomial
    if (draw):
        fig, ax = plt.subplots(1)
        plt.scatter(means, variances)
        plt.plot(means, np.exp(coeff[0]+coeff[1]*np.log(means)+coeff[2]*np.log(means)**2+coeff[3]*np.log(means)**3), color='red')
        ax.set_yscale("log")
        ax.set_xscale("log")
        plt.xlabel("mean")
        plt.ylabel("variance")
    
    # calculate fractal dimension for every scale in "scales", by obtaining the derivative of the polynomial (which represents the local slope)
    slopes = coeff[1] + 2*coeff[2]*np.log(means) + 3*coeff[3]*np.log(means)**2
    D = 2 - slopes / 2 
    
    return D, np.array(scales) # the dimension on index i of "D" corresponds to the scale on index i of "scales"


def complexity_evolution(sig, width, step, n_min, n_max):
    """
    The time-dependent complexity method which extracts a list of fractal dimensions for various scales over time.

    :param sig: dataframe containing the activity counts and the timestamp these correspond to (the start of the 1-minute interval
                for which these were obtained)
    :param width: width of the window which slides over the sequence and calculates the fractal dimension for the activity sequence 
                    contained within it. this is described as a string from which a Timedelta can be extracted (e.g. "3 days")
    :param step: the step size with which to advance the window. this is described as a string from which a Timedelta can be extracted (e.g. "5 min")
    :param n_min: minimal level of aggregation
    :param n_max: maximal level of aggregation

    return: list "dimensions", containing the fractal dimension for every level n in "scales", for every timestamp in "timestamps"
    """

    window = pd.Timedelta(width) 
    start = sig.index[0] # extract timestamp indicating the start of the activity sequence 
    end = start + window
    dimensions = []
    timestamps = []

    while(end <= sig.index[-1]): # advance the window until the end of it reaches the end of the counts sequence (do not allow partially filled windows)

        D, scales = adapted_allometric_aggregation(np.array(sig[start:end]["counts"]), n_min, n_max, draw=False) # use default value of 1.1 for spreading
        dimensions.append(D)
        timestamps.append(end) # keep the timestamp indicating the end of the interval for which the fractal dimensions were obtained
        start += pd.Timedelta(step) # advance the window
        end = start + window

    timestamps = pd.to_datetime(timestamps)
    timestamps = timestamps.to_pydatetime() #  the timestamps are returned in the datetime format for easy plotting of the obtained evolution

    return dimensions, timestamps, scales # dimensions contains a list of fractal dimensions for every scale in "scales", for every timestamp in "timestamps"
                                            # with the timestamp indicating the end of the window for which the dimensions were calculated
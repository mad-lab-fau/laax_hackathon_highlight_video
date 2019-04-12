import numpy as np
import math
import scipy.signal as sp


def detect_air(accel, gyro, window=10, nr_of_vals=5, threshold_low_fft=20, threshold_gyro_trick=50, jump_distance=10):
    """
    detects air times is a signal sequence of snowboarding recorded with the nilsPod
    :param accel: 3D acceleration signal
    :param gyro: 3D rotational signal
    :param window: window width for fft computation
    :param nr_of_vals: number of fft values in a row that need to be below threshold for signal part to be air time
    :param threshold_low_fft: threshold for accel-fft
    :param threshold_gyro_trick: threshold for gyro (jump vs. standing)
    :param jump_distance: minimal number of frames that need to lie between two jumps
    :return: array of same length as accel with air time frames = 1, non-air time frames = 0
    """

    # compute fft value in windows of size window (non-overlapping)
    # frames is an array stating the inidices in fft_signal that have non-zero values (window * k)
    frames = np.arange(0, accel[:, 0].__len__(), window)
    fft_signal = compute_fft_signal(accel, window)

    # if nr_of_vals fft-signal-values in a row are below the threshold_low_fft, array is 1, else 0
    low_fft = find_low_fft(fft_signal, frames, nr_of_vals, threshold_low_fft)

    # remove standing phases from air time ->  gyro shows no movement
    res_remove_no_gyro = remove_no_gyro(gyro, low_fft, window, threshold_gyro_trick)

    # if there is an airtime that is only < nr_of_vals samples long -> remove
    res_remove_too_few_in_a_row = remove_too_few_in_a_row(res_remove_no_gyro, frames, nr_of_vals)
    # first and last nr_of_vals not looked at before -> defined to be no air time
    res_remove_too_few_in_a_row[frames[0:nr_of_vals]] = 0
    res_remove_too_few_in_a_row[frames[frames.__len__()-nr_of_vals+1:]] = 0

    # combine all detected air times that are so close to each other (jump-distance) that they are probably one jump
    result = combine_to_airtimes(res_remove_too_few_in_a_row, frames, jump_distance)

    # plot results
    # figs, ax = plt.subplots(nrows=3, ncols=1, sharex=True)
    # ax[0].plot(lowFFT)
    # ax[1].plot(res_remove_no_gyro)
    # ax[2].plot(res_remove_too_few_in_a_row)
    # plt.show()

    return result


def find_low_fft(fft_signal, frames, nr_of_vals, threshold):
    """
    If nr_of_vals fft-signal values in a row are below the threshold_low_fft, array is 1 (air), else 0
    :param fft_signal: array with fft-signal, only non-zero every window'th index
    :param frames: array with indices of non-zero entries in fft_signal
    :param nr_of_vals: number of vals in a row that need to be smaller than the threshold to be air
    :param threshold:
    :return: array of same length as accel with air time frames = 1, non-air time frames = 0
    """
    result = np.zeros(fft_signal.__len__())
    fft_signal_condensed = fft_signal[fft_signal != 0]
    for i in range(0, fft_signal_condensed.__len__()-nr_of_vals):
        curr = fft_signal_condensed[i:i+nr_of_vals]
        if is_air(curr, nr_of_vals, threshold):
            result[frames[i]] = 1

    return result


def is_air(signal, nr_of_vals, threshold):
    """
    checks whether the values stored in signal are below threshold -> air
    :param signal: nr_of_vals of the fft signal
    :param nr_of_vals: number how many in a row need to be below threshold
    :param threshold:
    :return: true if air, false otherwise
    """
    s = 0
    for j in range(0, nr_of_vals):
        if signal[j] <= threshold:
            s = s + 1
    if s >= nr_of_vals - 1:
        return True
    else:
        return False


def remove_too_few_in_a_row(low_fft, frames, nr_of_vals):
    """
    Removes frames from the air time that are not long enough (i.e. less than nr_of_vals in a row)
    :param low_fft:
    :param frames:
    :param nr_of_vals:
    :return:
    """

    result = low_fft.copy()

    for i in range(nr_of_vals-1, frames.__len__()-nr_of_vals):

        is_in_a_row_of_5 = False
        # search all possible nr_of_vals long arrays around frame i
        for j in range(-nr_of_vals+1, nr_of_vals-1):

            curr = low_fft[frames[i + j:i + j + nr_of_vals]]

            if np.sum(curr) == nr_of_vals:
                is_in_a_row_of_5 = True

        if not is_in_a_row_of_5:
            result[frames[i]] = 0
    return result


def remove_no_gyro(gyro, low_fft, window, gyro_trick_threshold):
    """
    Remove standing phases from air time ->  gyro amplitude in window < threshold -> no air
    :param gyro: gyro signal
    :param low_fft:
    :param window:
    :param gyro_trick_threshold:
    :return:
    """
    result = low_fft.copy()
    for i in range(0, low_fft.__len__() - window):
        if low_fft[i] > 0:
            # sum over gyro
            s = 0
            for j in range(0,window):
                s = s + math.sqrt(math.pow(gyro[i+j,0],2) + math.pow(gyro[i+j,1],2) + math.pow(gyro[i+j,2],2))
            s = s/window
            if s < gyro_trick_threshold:
                result[i] = 0
    return result


def combine_to_airtimes(air, frames, jump_distance):
    """
    combine all detected air times that are so close to each other that they are probably one jump
    :param air: current air array (1 for air time, 0 for no air time)
    :param frames:
    :param jump_distance: min distance of two separate jumps
    :return: array of same length as air with combined air times
    """
    result = air.copy()
    # loop through, as long as another non-zero value is in the limit of jump-distance, it is added to the jump
    i = 0
    while i < frames.__len__():
        if air[frames[i]] != 0:
            start = frames[i]
            #in jump_distance search for other non-zero
            j = 0
            while j <= jump_distance:
                if air[frames[i+j]] != 0:
                    i = i+1
                    j = 0
                else:
                    j = j+1
            stop = frames[i]
            result[start:stop] = 1

        i = i+1
    return result


def compute_fft_signal(accel, window):
    """
    computes for a non-overlapping window of size window a value from the fft of all axes
    :param accel: acceleration signal (3D)
    :param window: fft window size
    :return: array same length as accel with one value at every window'th position
    """

    result = np.zeros(accel[:, 0].__len__())
    for i in range(0, accel[:, 0].__len__(), window):
        fftx = abs(np.fft.fft(accel[i:i + window - 1, 0]))
        ffty = abs(np.fft.fft(accel[i:i + window - 1, 1]))
        fftz = abs(np.fft.fft(accel[i:i + window - 1, 2]))
        # sum up the means of the three axes' ffts, but remove 0-frequency and highest frequency (first 3 + last 3)
        result[i] = np.sum(fftx[3:fftx.__len__() - 3]) / (fftx.__len__() - 6) +\
                    np.sum(ffty[3:ffty.__len__() - 3]) / (ffty.__len__() - 6) +\
                    np.sum(fftz[3:fftz.__len__() - 3]) / (fftz.__len__() - 6)
    return result


def find_airtime_midpoints(air_times):
    """
    In the air_times array resulting from detect_air(...), find the frames that are midpoints of jumps
    :param air_times: array with 1 for air time, 0 for non-air time
    :return: array with the indices of the middles of the air times
    """
    peaks = sp.find_peaks(air_times)
    result = np.zeros(peaks[0].__len__())
    k = 0
    for peak in peaks[0]:
        i = 0
        a = air_times[peak+1]
        while air_times[peak + i] != 0:
            i = i+1
        result[k] = peak + int((i/2))
        k = k+1

    return result.astype(np.int)


def find_airtime_lengths(air_times):
    """
    compute air time lenghts from the air time array
    :param air_times: array with 1 for air time, 0 for non-air time
    :return: array containing lengths of the air times
    """
    peaks = sp.find_peaks(air_times)
    result = np.zeros(peaks[0].__len__())
    k = 0
    for peak in peaks[0]:
        length = 0
        while air_times[peak + length] != 0:
            length = length + 1
        result[k] = length
        k = k + 1

    return result.astype(np.int)


def select_longest(air_times, labels, n):
    """
    finds the n longest air times in the signal
    :param air_times: array with 1 for air time, 0 for non-air time
    :param labels: mipoints of air times
    :param n: number of longest air times to be selected
    :return: labels (=midpoints) of longest air times + their lengths
    """
    labels_longest = np.zeros(n)
    lengths_longest = np.zeros(n)
    air_time_lengths = find_airtime_lengths(air_times) # compute air time lengths
    number_of_airtimes = air_time_lengths.__len__()
    # sort via air time lengths and take the n longest
    idx_shortest_to_longest = np.argsort(air_time_lengths)
    for i in range(0, n):
        labels_longest[i] = labels[idx_shortest_to_longest[number_of_airtimes-n+i]]
        lengths_longest[i] = air_time_lengths[idx_shortest_to_longest[number_of_airtimes-n+i]]

    return labels_longest, lengths_longest

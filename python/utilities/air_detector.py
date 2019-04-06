import numpy as np
import math
import scipy.signal as sp

def detect_air(accel, gyro, window=10, nr_of_vals=5, threshold_lowFFT=20, threshold_gyro_trick=50, jump_distance=4):
    frames = np.arange(0, accel[:, 0].__len__(), window)
    fft_signal = compute_fft_signal(accel, window)
    #figs, ax = plt.subplots(nrows=3, ncols=1, sharex=True)

    lowFFT = find_lowFFT(fft_signal, frames, nr_of_vals, threshold_lowFFT)
    #ax[0].plot(lowFFT)
    res_remove_no_gyro = remove_no_gyro(gyro, lowFFT, window, threshold_gyro_trick)
    #ax[1].plot(res_remove_no_gyro)
    res_remove_too_few_in_a_row = remove_too_few_in_a_row(res_remove_no_gyro, frames, nr_of_vals)
    res_remove_too_few_in_a_row[frames[0:nr_of_vals]] = 0
    res_remove_too_few_in_a_row[frames[frames.__len__()-nr_of_vals+1:]] = 0
    #ax[2].plot(res_remove_too_few_in_a_row)
    result = combine_to_airtimes(res_remove_too_few_in_a_row, frames, jump_distance)
    #plt.show()
    return result


def find_lowFFT(fft_signal, frames, nr_of_vals, threshold):
    result = np.zeros(fft_signal.__len__())
    fft_signal_condensed = fft_signal[fft_signal != 0]
    for i in range(0, fft_signal_condensed.__len__()-nr_of_vals):
        curr = fft_signal_condensed[i:i+nr_of_vals]
        if is_air(curr, nr_of_vals, threshold):
            result[frames[i]] = 1

    return result


def is_air(signal, nr_of_vals, threshold):
    s = 0
    for j in range(0, nr_of_vals):
        if signal[j] <= threshold:
            s = s + 1
    if s >= nr_of_vals - 1:
        return True
    else:
        return False


def remove_too_few_in_a_row(lowFFT, frames, nr_of_vals):
    result = lowFFT.copy()

    for i in range(nr_of_vals-1, frames.__len__()-nr_of_vals):

        if frames[i] == 18230:
            h = 1

        is_in_a_row_of_5 = False

        for j in range(-nr_of_vals+1, nr_of_vals-1):

            curr = lowFFT[frames[i+j:i+j+nr_of_vals]]

            if np.sum(curr) == nr_of_vals:
                is_in_a_row_of_5 = True

        if not is_in_a_row_of_5:
            result[frames[i]] = 0
    return result


def remove_no_gyro(gyro, lowFFT, window, gyro_trick_threshold):
    result = lowFFT.copy()
    for i in range(0,lowFFT.__len__()-window):
        if lowFFT[i] > 0:
            # sum over gyro
            s = 0
            for j in range(0,window):
                s = s + math.sqrt(math.pow(gyro[i+j,0],2) + math.pow(gyro[i+j,1],2) + math.pow(gyro[i+j,2],2))
            s = s/window
            if s < gyro_trick_threshold:
                result[i] = 0
    return result


def combine_to_airtimes(air, frames, jump_distance):
    result = air.copy()
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
    result = np.zeros(accel[:, 0].__len__())
    for i in range(0, accel[:, 0].__len__(), window):
        fftx = abs(np.fft.fft(accel[i:i + window - 1, 0]))
        ffty = abs(np.fft.fft(accel[i:i + window - 1, 1]))
        fftz = abs(np.fft.fft(accel[i:i + window - 1, 2]))
        result[i] = np.sum(fftx[3:fftx.__len__() - 3]) / (fftx.__len__() - 6) + np.sum(ffty[3:ffty.__len__() - 3]) / (ffty.__len__() - 6) + np.sum(fftz[3:fftz.__len__() - 3]) / (fftz.__len__() - 6)
    return result


def find_airtime_midpoints(air_times):
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

    return result

from sksound.sounds import Sound
import librosa
import numpy as np


def read_music(file):
    """
    Reads musci file to numpy array
    :param file: filename string
    :return: numpy array, fs
    """

    hello = Sound(file)

    data = np.array(hello.data)
    fs = hello.rate

    return data, fs


def get_beats_after_seconds(onset_detected, rough_duration_clips):
    """
    Computes video transition times based on detected onstes and rough duration of the clips
    :param onset_detected: detected onsets from librosa in time units
    :param rough_duration_clips: list with rough durations of each individual clip
    :return: actual duration matched o beat
    """

    onset_detected = onset_detected.tolist()
    onset_detected.insert(0, 0)

    onset_detected = np.array(onset_detected)
    diff_onsets = np.diff(onset_detected)

    resulting_durations = []

    counter_onsets = 0
    for i in range(len(rough_duration_clips)):

        current_sum = 0

        while current_sum < rough_duration_clips[i]:
            current_sum += diff_onsets[counter_onsets]
            counter_onsets += 1

        resulting_durations.append(current_sum)

    return resulting_durations

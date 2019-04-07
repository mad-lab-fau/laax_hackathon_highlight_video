import moviepy
import os
import utilities.utilities as util
import utilities.air_detector as air
from moviepy.editor import *
import utilities.music as music

file_loc = '../../data/session3/'

for root, dirs, files in os.walk(file_loc):
    for m in files:
        if m.endswith('calib.csv') and m.__contains__('Nils'):
            csv_file = m

for root, dirs, files in os.walk(file_loc):
    for m in files:
        if m.endswith('.mp4') and m.__contains__('combinedVideo'):
            video_file = m

"""
data = util.load_data(file_loc + csv_file)
accel = util.get_accel(data)
gyro = util.get_gyro(data)

window = 10 # window size for fft
nr_of_vals = 5 # number of air labels in a row for it to be a real air
threshold_lowFFT = 20 # upper threshold for fft
threshold_gyro_trick = 50 # lower threshold for gyro to be a trick
jump_distance = 10 # if there are less than (jump_distance * window size) frames between two air times, they are merged
air_times = air.detect_air(accel, gyro, window, nr_of_vals, threshold_lowFFT, threshold_gyro_trick, jump_distance)
"""



video = VideoFileClip(file_loc + 'Intro.mp4', audio=True)
sub_clip = video.set_duration(5.77015873015873)
sub_clip.write_videofile(file_loc + "Intro2.mp4",
                          temp_audiofile="temp-audio.m4a",
                          remove_temp=True,
                          codec="libx264",
                          audio_codec="aac")
stop = 0







import moviepy
import os
import utilities.utilities as util
import utilities.air_detector as air
from moviepy.editor import *
import utilities.music as music

file_loc = '../../data/session2/'

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

# read music
filename = '../../data/music/boom.mp3'
audio = AudioFileClip(filename)

video = VideoFileClip(file_loc + video_file, audio=True)
sub_clip = video.subclip(0, 15)
sub_clip2 = sub_clip.set_audio(audio.set_duration(15))
sub_clip2.write_videofile(file_loc + "output.mp4",
                          temp_audiofile="temp-audio.m4a",
                          remove_temp=True,
                          codec="libx264",
                          audio_codec="aac")
stop = 0







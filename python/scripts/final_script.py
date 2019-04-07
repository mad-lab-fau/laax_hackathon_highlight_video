import utilities.utilities as util
import utilities.video_imu_conversions as vic
import utilities.air_detector as air
import librosa
import utilities.video_cutting as vc
import utilities.music as music
import numpy as np
from moviepy.editor import *
import os
from moviepy.video.compositing.concatenate import concatenate_videoclips

session_id = 3
file_loc = '../../data/session' + str(session_id) + '/'
offsets = {1: 0, 2: -400, 3:-400, 4: 0}
for root, dirs, files in os.walk(file_loc):
    for m in files:
        if m.endswith('calib.csv') and m.__contains__('Nils'):
            csv_file = m

for root, dirs, files in os.walk(file_loc):
    for m in files:
        if m.endswith('.mp4') and m.__contains__('combinedVideo'):
            video_file = m

# load data
data = util.load_data(file_loc + csv_file)
# get time array
t = util.get_time_array(data.shape[0], 204.8)

######## event detection using air time FFT analysis #################
accel = util.get_accel(data)
gyro = util.get_gyro(data)

window = 10 # window size for fft
nr_of_vals = 5 # number of air labels in a row for it to be a real air
threshold_lowFFT = 20 # upper threshold for fft
threshold_gyro_trick = 50 # lower threshold for gyro to be a trick
jump_distance = 10 # if there are less than (jump_distance * window size) frames between two air times, they are merged
air_times = air.detect_air(accel, gyro, window, nr_of_vals, threshold_lowFFT, threshold_gyro_trick, jump_distance)
labels = air.find_airtime_midpoints(air_times)

# correct video synchro offset
labels += offsets[session_id]

# select longest air times only
n = 4
[labels_longest, lengths_longest] = air.select_longest(air_times, labels, n)
labels_video = vic.convert_index_sampling_rate(labels_longest, 204.8, 25)

########## Music analysis #########
file_loc_music = '../../data/music/'
filename = 'boom.mp3'

music_song, fs_music = music.read_music(file_loc_music + filename)
t_music = util.get_time_array(music_song.shape[0], fs_music)

onset_detected = librosa.onset.onset_detect(music_song[:, 1].astype(np.float32), fs_music, units='time')
duration_videos_beat = music.get_beats_after_seconds(onset_detected, [4, 6, 6, 6, 6])

video_file_names = []
clips = []
for i in range(n):
    written_files = vc.cut_video_from_labels(file_loc,
                                             video_file,
                                             labels_video[i],
                                             duration_videos_beat[i+1],
                                             video_name='test_' + str(i) + '_')

    clips.append(VideoFileClip(file_loc + written_files[0], audio=True))

# add intro to clips
intro_name = 'Intro.mp4'
intro = VideoFileClip(file_loc + intro_name, audio=True)
intro = intro.set_duration(duration_videos_beat[0])
clips.insert(0, intro)

# concatenate clips
final_clip = concatenate_videoclips(clips)

# read music
filename = '../../data/music/boom.mp3'
audio = AudioFileClip(filename)

# add audio
sub_clip2 = final_clip.set_audio(audio.set_duration(final_clip.duration))
sub_clip2.write_videofile(file_loc + "output.mp4",
                          temp_audiofile="temp-audio.m4a",
                          remove_temp=True,
                          codec="libx264",
                          audio_codec="aac")
stop = 0



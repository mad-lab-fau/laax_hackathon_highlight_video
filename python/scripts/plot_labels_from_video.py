import utilities.utilities as util
import utilities.video_imu_conversions as vic
import utilities.air_detector as air
import pandas as pd
import matplotlib.pyplot as plt
import os
import utilities.video_cutting as vc

file_loc = '../../data/session1/'
for root, dirs, files in os.walk(file_loc):
    for m in files:
        if m.endswith('.csv') and m.__contains__('Nils'):
            csv_file = m

label_file = 'video_framelabels.csv'

labels_video = pd.read_csv(file_loc + label_file, header=None)
labels_video = list(labels_video.values)
labels_imu = vic.convert_index_sampling_rate(labels_video, 25, 204.8)

data = util.load_data(file_loc + csv_file)

t = util.get_time_array(data.shape[0], 204.8)

data_type = 'accel'
half_window_size = 10

accel = util.get_accel(data)
gyro = util.get_gyro(data)
energy = util.get_energy(data, 10)

window = 10 # window size for fft
nr_of_vals = 5 # number of air labels in a row for it to be a real air
threshold_lowFFT = 20 # upper threshold for fft
threshold_gyro_trick = 50 # lower threshold for gyro to be a trick
air_times = air.detect_air(accel, gyro, window, nr_of_vals, threshold_lowFFT, threshold_gyro_trick)
labels = air.find_airtime_midpoints(air_times)
labels_video = vic.convert_index_sampling_rate(labels, 204.8, 25)

vc.cut_video_from_labels(file_loc, 'combinedVideo_134603_to_144738.mp4', labels_video, 2)

print(labels)

figs, ax = plt.subplots(nrows=3, ncols=1, sharex=True)
ax[0].plot(t, accel)
ax[0].set_ylabel('acceleration in m/s^2')
ax[0].legend(['x', 'y', 'z'])
ax[0].vlines(t[labels_imu], -250, 250)
ax[0].grid(True)


ax[1].plot(t, gyro)
ax[1].set_ylabel('gyroscope in deg^2')
ax[1].set_xlabel('t in s')
ax[1].legend(['x', 'y', 'z'])
ax[1].vlines(t[labels_imu], -1000, 1000)
ax[1].grid(True)

ax[2].plot(t, air_times)
ax[2].set_ylabel('air_times')


plt.show()

import utilities.utilities as util
import utilities.video_imu_conversions as vic
import pandas as pd
import matplotlib.pyplot as plt

file_loc = '../../data/session1/'

csv_file = 'NilsPodX-3D41_20190405_1338_sync.csv'
label_file = 'video_framelabels.csv'

labels_video = pd.read_csv(file_loc + label_file, header=None)
labels_video = list(labels_video.values)
labels_imu = vic.convert_index_sampling_rate(labels_video, 25, 204.8)

data = util.load_data(file_loc + csv_file)

t = util.get_time_array(data.shape[0], 204.8)

data_type = 'accel'
half_window_size = 10

energy = util.get_energy(data, 10)

figs, ax = plt.subplots(nrows=3, ncols=1, sharex=True)
accel = util.get_accel(data)
ax[0].plot(t, accel)
ax[0].set_ylabel('acceleration in m/s^2')
ax[0].legend(['x', 'y', 'z'])
ax[0].vlines(t[labels_imu], -250, 250)
ax[0].grid(True)

gyro = util.get_gyro(data)
ax[1].plot(t, gyro)
ax[1].set_ylabel('gyroscope in deg^2')
ax[1].set_xlabel('t in s')
ax[1].legend(['x', 'y', 'z'])
ax[1].vlines(t[labels_imu], -1000, 1000)
ax[1].grid(True)

t_energy = t[half_window_size:t.shape[0]-half_window_size]
ax[2].plot(t_energy, energy)
ax[2].set_ylabel('energy')


plt.show()

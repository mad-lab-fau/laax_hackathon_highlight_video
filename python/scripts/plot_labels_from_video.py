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
print(labels_video)

data = util.load_data(file_loc + csv_file)

accel = util.get_accel(data)
plt.plot(accel)
plt.vlines(labels_imu, -250, 250)

plt.show()

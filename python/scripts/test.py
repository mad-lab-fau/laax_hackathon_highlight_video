import utilities.utilities as util
import utilities.video_imu_conversions as vic
import matplotlib.pyplot as plt
import utilities.video_cutting as vc

file_loc = '../../data/session1/'

csv_file = 'NilsPodX-3D41_20190405_1338_sync.csv'
video_file = 'combinedVideo_134603_to_144738.mp4'

data = util.load_data(file_loc + csv_file)

# get labels from plot
labels = util.marker_plot(util.get_gyro(data))
# convert labels to sampling rate of video
new_labels = vic.convert_index_sampling_rate(labels, 204.8, 25)

vc.cut_video_from_labels(file_loc, video_file, new_labels, 5, video_black_indicator=True)

plt.show()

import utilities.utilities as util
import matplotlib.pyplot as plt

file_loc = '../../data/session1/'

csv_file = 'NilsPodX-3D41_20190405_1338_sync.csv'
video_file = 'combinedVideo_134603_to_144738.mp4'

data = util.load_data(file_loc + csv_file)

util.plot_3D_imu_data(data.iloc[:, 4:7], 204.8)

plt.show()
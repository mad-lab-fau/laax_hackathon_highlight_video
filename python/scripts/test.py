import utilities.utilities as util
import utilities.video_imu_conversions as vic
import matplotlib.pyplot as plt
import numpy as np
import imageio



file_loc = '../../data/session1/'

csv_file = 'NilsPodX-3D41_20190405_1338_sync.csv'
video_file = 'combinedVideo_134603_to_144738.mp4'

data = util.load_data(file_loc + csv_file)

#test = util.get_energy(data, 100)
#plt.plot(test)

#util.plot_3D_imu_data(data.iloc[:, 4:7], 204.8)

# get labels from plot
labels = util.marker_plot(util.get_gyro(data))
# convert labels to sampling rate of video
new_labels = vic.convert_index_sampling_rate(labels, 204.8, 25)

# read video data
reader = imageio.get_reader(file_loc + video_file)

accumulation = 0
counter_in_label = 0

# get one image to get video size
image = reader.get_data(new_labels[0])

# video duration in
t_video = 5     # s
fs_video = 25   # Hz
video_frames_total = t_video * fs_video + 1

# iterate over labels and cut videos
counter_video = 0
for frame in new_labels:

    # ToDo: problem at start and end
    # initialize video
    video_numpy = np.zeros((video_frames_total, image.shape[0], image.shape[1], image.shape[2]))

    # iterate from half of time before to half of time after
    counter = 0
    for i in range(frame-int((video_frames_total-1)/2), frame + int((video_frames_total-1)/2 + 1)):
        video_numpy[counter] = reader.get_data(i).astype(np.uint8)
        counter += 1

    # write image
    imageio.mimwrite(file_loc + 'test' + str(counter_video) + '.mp4', video_numpy, fps=25)
    counter_video += 1
    stop = 0


plt.show()

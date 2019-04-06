from sksound.sounds import Sound
import numpy as np
import utilities.utilities as util
import matplotlib.pyplot as plt
import librosa

file_loc = '../../data/music/'
filename = 'boom.mp3'

hello = Sound(file_loc + filename)

data = np.array(hello.data)
fs = hello.rate

t = util.get_time_array(data.shape[0], fs)
plt.plot(t, data)

onset_detected = librosa.onset.onset_detect(data[:, 1].astype(np.float32), fs, units='time')
print(onset_detected)
print(data.shape)

plt.vlines(onset_detected, -15000, 15000)

plt.show()


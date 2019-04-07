from sksound.sounds import Sound
import numpy as np
import utilities.utilities as util
import matplotlib.pyplot as plt
import librosa
import utilities.music as music

file_loc = '../../data/music/'
filename = 'boom.mp3'

data, fs = music.read_music(file_loc + filename)
t = util.get_time_array(data.shape[0], fs)

onset_detected = librosa.onset.onset_detect(data[:, 1].astype(np.float32), fs, units='time')
test = music.get_beats_after_seconds(onset_detected, [5, 4, 5])

jo = np.cumsum(np.array(test))
print(jo)

plt.plot(t, data)
plt.vlines(onset_detected, -15000, 15000)
plt.vlines(jo, -13000, 13000, colors='r')

plt.show()


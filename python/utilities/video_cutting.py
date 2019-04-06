import imageio
import numpy as np


def cut_video_from_labels(folder_loc, filename, labels, duration_clip, video_name='test', video_black_indicator=False):
    """
    Cut clips from long video using labels
    :param folder_loc: original file location
    :param filename: string
    :param labels: list with labels
    :param duration_clip: in s
    :param video_name: string
    :param video_black_indicator: boolean, default False, if true, black bar is around video
    """

    fs_video = 25  # Hz

    # read video data
    reader = imageio.get_reader(folder_loc + filename)

    # get one image to get video size
    image = reader.get_data(labels[0])

    # video duration in
    video_frames_total = duration_clip * fs_video + 1

    # iterate over labels and cut videos
    counter_video = 0
    for frame in labels:

        # ToDo: problem at start and end
        # initialize video
        if video_black_indicator:
            video_numpy = np.zeros((video_frames_total,
                                    image.shape[0] - 560,
                                    image.shape[1],
                                    image.shape[2])).astype(np.uint8)
        else:
            video_numpy = np.zeros((video_frames_total,
                                    image.shape[0],
                                    image.shape[1],
                                    image.shape[2])).astype(np.uint8)

        # iterate from half of time before to half of time after
        counter = 0
        for i in range(frame - int((video_frames_total - 1) / 2), frame + int((video_frames_total - 1) / 2 + 1)):
            if video_black_indicator:
                help_array = reader.get_data(i)[280:image.shape[0] - 280]
            else:
                help_array = reader.get_data(i)

            video_numpy[counter] = help_array.astype(np.uint8)
            counter += 1

        # write image
        imageio.mimwrite(folder_loc + video_name + '_' + str(counter_video) + '.mp4', video_numpy, fps=25)
        counter_video += 1

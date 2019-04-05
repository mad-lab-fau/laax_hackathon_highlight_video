def convert_index_sampling_rate(list_labels, fs_old, fs_new):
    """
    Converts indices in sampling rate with fs old to fs new
    :param list_labels:
    :param fs_old: in Hz
    :param fs_new: in Hz
    :return: list_new_labels
    """

    list_new_labels = []
    for index_in_video in list_labels:
        t = index_in_video / fs_old
        list_new_labels.append(int(t * fs_new))

    return list_new_labels

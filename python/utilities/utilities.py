import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def load_data(filename):
    """
    Load file and returns data as pandas dataframe
    :param filename: string
    :return: pandas dataframe
    """

    data = pd.read_csv(filename)

    return data


def get_time_array(n_samples, fs):
    """
    Function returns numpy array with time series starting with 0
    :param n_samples: number of samples in time array
    :param fs: sampling rate
    :return: time series as numpy array
    """

    start = 0
    stop = n_samples/fs
    step = 1 / fs
    t = np.arange(start, stop, step)
    if (stop/step) > n_samples:
        t = t[:-1]

    return t


def marker_plot(x, y=None, title = None, fontsize=12, linewidth=2):
    """
    Plots data provide with possibility to set markers
    :param x: if only x provided, data to plot, else x-axis
    :param y: y-axis if provided
    :param title: string
    :param fontsize:
    :param linewidth:
    :return: list with marker set in plot
    """

    # plot the data
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)
    if y is not None:
        plt.plot(x, y)
    else:
        plt.plot(x)
    plt.grid(True)
    if title is None:
        plt.title("Left double click for setting, right double click removing")
    else:
        plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")

    list_markers = []
    marker_list_plot = []

    def onclick(event):
        # switch to the move cursor
        # set a marker with doubleclick left
        # remove the last marker with doubleclick right

        # with button 1 (double left click) you will set a marker
        if event.button == 1 and event.dblclick:
            idx = int(event.xdata)
            list_markers.append(idx)
            marker = ax.axvline(idx)
            marker_list_plot.append(marker)
            plt.show()

        # with button 3 (double right click) you will remove a marker
        elif event.button == 3 and event.dblclick:
            # position of the last marker
            idx = list_markers[-1]
            list_markers.remove(idx)
            a = marker_list_plot.pop()
            # remove the last marker
            a.remove()
            del a
            plt.show()

    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    # sort the labels in ascending order
    list_markers.sort()

    return list_markers


def plot_3D_imu_data(data, fs, ylabel='', title='', legend=None,
                     fontsize=12, linewidth=2, figsize=(6.4, 4.8), ylim=None):
    """
    Plots 3 dimensional IMU data. This function is helpful for plotting IMU signals during debugging
    :param data: pandas Dataframe with X, Y, Z
    :param fs: int, samplingrate in Hz
    :param ylabel: string
    :param title: string
    :param legend: three dimensional string, default column names will be used
    :param fontsize: int, default 12
    :param linewidth: int, default 2
    :param figsize: tuple (x, y)
    :param ylim: tuple (-,+)
    """

    # set linewidth and fontsize
    matplotlib.rcParams['font.size'] = fontsize
    matplotlib.rcParams['lines.linewidth'] = linewidth
    plt.rcParams['figure.figsize'] = figsize

    color_list = get_plot_colors_presentations()
    t = get_time_array(data.shape[0], fs)

    if legend is None:
        legend = list(data)

    if ylabel == '':
        column_names = list(data)
        if column_names[0][0] == 'g':
            ylabel = 'Angular rate (deg/s)'
        elif column_names[0][0] == 'a':
            ylabel = 'Acceleration (m/s)'

    plt.figure()
    plt.plot(t, data.iloc[:, 0], color=color_list[0], label=legend[0])
    plt.plot(t, data.iloc[:, 1], color=color_list[1], label=legend[1])
    plt.plot(t, data.iloc[:, 2], color=color_list[2], label=legend[2])
    plt.xlabel('t (s)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    if ylim is not None:
        plt.ylim(ylim)


def color_test_plot(type_color):
    """
    Test function for defined colors
    :param type_color
    """
    if type == 'bw':
        colors = np.array(get_plot_colors_bw())
    elif type == 'fau':
        colors = np.array(get_plot_colors_fau())
    else:
        colors = np.array(get_plot_colors_presentations())

    x = range(colors.shape[0])
    test_data = np.ones(colors.shape[0])
    plt.figure()

    for i in range(len(test_data)):
        plt.bar(x[i], test_data[i], color=colors[i])


def get_plot_colors_bw():
    """
    Get plot colors especially for publications (6 colors)
    :return: list with colors
    """

    color_list = ['#050044',
                  '#8e2626',
                  '#429c3a',
                  '#bfb0f5',
                  '#acebef',
                  '#000000',
                  '#bbdefb']

    rgb_list = []
    for c in color_list:
        c = c.lstrip('#')
        rgb_list.append(tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)))

    return color_list


def get_plot_colors_fau():
    """
    Get color list with fau blue and techfak grey (+ black, 3 colors)
    :return: list with colors
    """

    color_list = ['#003865',    # FAU blue
                  '#98A4AE',    # TechFak grey
                  '#8D1429',    # Rechts-/Wirtschaftswissenschaft red
                  '#009B77',    # NetFak green
                  '#C99313',    # PhilFak orange
                  '#00B1EB',    # MedFak cyan
                  '#000000']    # black]

    rgb_list = []
    for c in color_list:
        c = c.lstrip('#')
        rgb_list.append(tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)))

    return color_list


def get_plot_colors_presentations():
    """
    Get color list for presentations (9 colors)
    :return: list with presentation colors (material.io, 800)
    """
    # colors from material.io, 800, https://material.io/guidelines/style/color.html#color-color-palette
    # Colors: blue(0), red(1), green(2), grey(3), deep purple(4), deep orange(5), brown(6), cyan(7), teal(8), black(9)

    color_list = ['#283593',
                  '#C62828',
                  '#2E7D32',
                  '#424242',
                  '#4527A0',
                  '#D84315',
                  '#4E342E',
                  '#00838F',
                  '#00695C',
                  '#000000']

    rgb_list = []
    for c in color_list:
        c = c.lstrip('#')
        rgb_list.append(tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)))

    return color_list

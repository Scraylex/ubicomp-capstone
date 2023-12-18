import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from constants import DATA_KEYS


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def create_plots(df, filename) -> None:
    df[df.columns[3]] = df[df.columns[3]].astype(float) - df[df.columns[3]].min()
    plt.figure(figsize=(10, 6))
    for column in df.columns[:3]:
        plt.plot(df[df.columns[3]], df[column], label=column)
    plt.legend()
    plt.savefig(f'{filename}/plot.png')

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df[df.columns[0]], df[df.columns[1]], df[df.columns[2]])
    ax.set_xlabel(df.columns[0])
    ax.set_ylabel(df.columns[1])
    ax.set_zlabel(df.columns[2])
    plt.savefig(f'{filename}/scatter3d.png')


def write_csv(values, filename) -> None:
    # Create a DataFrame from the values
    df = pd.DataFrame(values, columns=DATA_KEYS)
    # Apply the lowpass filter to the first 3 columns
    for column in df.columns[:3]:
        df[column] = butter_lowpass_filter(df[column].astype(float), cutoff=3.0, fs=10.0)
    # Write the DataFrame to a CSV file
    create_plots(df.copy(), filename)
    df.to_csv(f'{filename}/out.csv', index=False)

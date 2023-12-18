import os
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

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

    # Plot x and y axes
    plt.figure(figsize=(10, 6))
    plt.plot(df[df.columns[0]], df[df.columns[1]], label='x vs y')
    plt.legend()
    plt.savefig(f'{filename}/plot_xy.png')

    # Plot x and z axes
    plt.figure(figsize=(10, 6))
    plt.plot(df[df.columns[0]], df[df.columns[2]], label='x vs z')
    plt.legend()
    plt.savefig(f'{filename}/plot_xz.png')

    # Plot y and z axes
    plt.figure(figsize=(10, 6))
    plt.plot(df[df.columns[1]], df[df.columns[2]], label='y vs z')
    plt.legend()
    plt.savefig(f'{filename}/plot_yz.png')

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df[df.columns[0]], df[df.columns[1]], df[df.columns[2]])
    ax.set_xlabel(df.columns[0])
    ax.set_ylabel(df.columns[1])
    ax.set_zlabel(df.columns[2])
    plt.savefig(f'{filename}/scatter3d.png')


def clean_data(df, filename):
    rolling_std = df[df.columns[:3]].rolling(window=10).std()
    stable_index = rolling_std[rolling_std < 0.05].first_valid_index()
    if stable_index is not None:
        df = df.drop(df.index[stable_index + 1:])
        value = int(df.loc[stable_index, df.columns[3]])
        for file in os.listdir(filename):
            if int(file.split('.')[0]) > value:
                joined = os.path.join(filename, file)
                os.remove(joined)
                print(f"Removed {joined}")


def write_csv(values, filename) -> None:
    df = pd.DataFrame(values, columns=DATA_KEYS)
    for column in df.columns[:3]:
        df[column] = butter_lowpass_filter(df[column].astype(float), cutoff=3.0, fs=10.0)

    clean_data(df, filename)

    create_plots(df.copy(), filename)
    df.to_csv(f'{filename}/out.csv', index=False)

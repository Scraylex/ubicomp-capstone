import os
import time

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

from constants import DATA_KEYS, OUTPUT_DIR
#from src.data_plotter import create_plots


def buttersworth_lowpass_filter(data_incoming, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(N=order, Wn=normal_cutoff)
    padlen = 2 * max(order, 1)
    return filtfilt(b, a, data_incoming, padlen=padlen)


def find_stable_periods(data_arg, column, threshold=0.1, min_stable_samples=15):
    # Calculate relative change as a measure of deviation
    data_arg['deviation'] = data_arg[column].pct_change().abs()

    # Identify stable samples
    data_arg['is_stable'] = data_arg['deviation'] < threshold

    # Find starting indices of stable periods
    stable_starts = []
    count = 0
    for i, stable in enumerate(data_arg['is_stable']):
        if stable:
            count += 1
            if count == 1:
                start = i
            if count >= min_stable_samples:
                stable_starts.append(start)
                count = 0
        else:
            count = 0

    # Optionally, remove stable periods from the dataframe
    # for start in stable_starts:
    #     data.drop(data.index[start:start + min_stable_samples], inplace=True)

    return stable_starts


def find_consensus_start_index(data_items, axes, threshold=0.25, min_stable_samples=5):
    all_starts = []
    for axis in axes:
        starts = find_stable_periods(data_items, axis, threshold, min_stable_samples)
        all_starts.extend(starts)

    if all_starts:
        # Calculate the average of start indices and round down
        consensus_start = np.floor(np.mean(all_starts)).astype(int)
        return consensus_start
    else:
        return None


def write_csv(values, file_path) -> None:
    data_received = pd.DataFrame(values, columns=DATA_KEYS)
    for column in data_received.columns[:6]:
        data_received[column] = buttersworth_lowpass_filter(data_received[column].astype(float), cutoff=3.0, fs=10.0)

    #create_plots(data.copy(), file_path)

    # consensus_start_index = find_consensus_start_index(df, data.columns[:6])
    # last_timestamp = data.iloc[consensus_start_index, 6]
    #
    # data = data.loc[:consensus_start_index]

    timestamp = int(time.time())
    data_received.to_csv(f'{file_path}/out.csv', index=False)

'''
if __name__ == '__main__':
    filename = f'{OUTPUT_DIR}/drinking_1705414500/'
    df = pd.read_csv(f'{filename}/out3.csv')
    consensus_start_index = find_consensus_start_index(df, df.columns[:6])
    last_timestamp = df.iloc[consensus_start_index, 6]
    data = df.loc[:consensus_start_index]

'''
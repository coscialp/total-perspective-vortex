"""
Preprocess the data.

This module preprocesses the data for the project. It contains the following functions:

        * preprocess - preprocess the data

Usage:
    $ python preprocess.py
"""

from typing import List

from matplotlib import pyplot as plt
from mne.io import Raw

from srcs.enums import TaskEnum
from srcs.load_dataset import load_dataset


def preprocess(subject: int = 1, task: List[int] = TaskEnum.Task1):
    """Preprocess the data."""
    print("Preprocessing the data.")
    raw: Raw = load_dataset(subject, task)
    raw.plot(scalings="auto")
    raw.compute_psd(n_jobs=-1).plot()
    raw.compute_psd(n_jobs=-1).plot(average=True, picks="eeg", exclude="bads")
    plt.show()

    raw.filter(8, 32, picks="eeg")

    raw.plot(scalings="auto")
    raw.compute_psd(n_jobs=-1).plot()
    raw.compute_psd(n_jobs=-1).plot(average=True, picks="eeg", exclude="bads")

    plt.show()


if __name__ == "__main__":
    preprocess()

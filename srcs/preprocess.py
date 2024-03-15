"""
Preprocess the data.

This module preprocesses the data for the project. It contains the following functions:

        * preprocess - preprocess the data

Usage:
    $ python preprocess.py
"""

from mne.datasets import eegbci  # type: ignore

# from mne.io import read_raw_edf  # type: ignore


def preprocess():
    """Preprocess the data."""
    print("Preprocessing the data...")
    raw_data = eegbci.load_data(
        subject=1,
        runs=[6, 10, 14],
        path="./mne_data",
        update_path=True,
    )

    print(raw_data)


if __name__ == "__main__":
    preprocess()

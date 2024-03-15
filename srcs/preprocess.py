"""
Preprocess the data.

This module preprocesses the data for the project. It contains the following functions:

        * preprocess - preprocess the data

Usage:
    $ python preprocess.py
"""

from mne import io  # type: ignore
from mne.datasets import eegbci  # type: ignore

from srcs.utils import VerboseType


def preprocess() -> io.Raw:
    """Preprocess the data."""
    data_paths = eegbci.load_data(
        subject=1,
        runs=[3, 7, 11],
        path="./mne_data",
        update_path=True,
        verbose=VerboseType.ERROR.value,
    )

    raw: io.Raw = io.concatenate_raws(
        [
            io.read_raw_edf(f, preload=True, verbose=VerboseType.ERROR.value)
            for f in data_paths
        ],
        verbose=VerboseType.ERROR.value,
    )
    eegbci.standardize(raw)

    raw.filter(7, 30, fir_design="firwin", verbose=VerboseType.ERROR.value)
    print(raw.describe())
    return raw


if __name__ == "__main__":
    preprocess()

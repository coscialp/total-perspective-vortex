from typing import List

import mne
from mne.datasets.eegbci import eegbci
from mne.io import Raw
from sklearn.model_selection import train_test_split

from srcs.enums import TaskEnum, VerboseType


def load_dataset(
    subject: int = 1,
    task: List[int] = TaskEnum.Task1,
    verbose: VerboseType = VerboseType.ERROR,
) -> Raw:
    """
    Load the dataset from the local storage
    """
    files_path = eegbci.load_data(
        subject=subject, runs=task, verbose=verbose.value, path="./datasets"
    )

    raws = [mne.io.read_raw_edf(file_path, preload=True) for file_path in files_path]
    raw = mne.concatenate_raws(raws, verbose="ERROR")
    eegbci.standardize(raw)

    return raw


def load_dataset_with_filter(
    subject: int = 1,
    task: List[int] = TaskEnum.Task1,
    l_freq: float = 8.0,
    h_freq: float = 32.0,
    verbose: VerboseType = VerboseType.ERROR,
):
    """
    Load the dataset from the local storage
    """
    raw = load_dataset(subject, task, verbose)
    raw.filter(l_freq, h_freq, picks="eeg")

    return raw


def load_split_dataset(
    subject: int = 1,
    task: List[int] = TaskEnum.Task1,
    l_freq: float = 8.0,
    h_freq: float = 32.0,
    tmin: float = 1.0,
    tmax: float = 4.0,
    test_size: float = 0.2,
    random_state: int = 42,
    verbose: VerboseType = VerboseType.ERROR,
):
    raw = load_dataset_with_filter(subject, task, l_freq, h_freq, verbose)
    events, event_id = mne.events_from_annotations(raw, verbose=verbose.value)
    picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False)
    epochs = mne.Epochs(
        raw,
        events,
        event_id,
        tmin,
        tmax,
        proj=True,
        picks=picks,
        baseline=None,
        preload=True,
        verbose=verbose.value,
    )

    X = epochs.get_data()
    y = epochs.events[:, -1] - 1

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test

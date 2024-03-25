from typing import List

import mne
from mne.datasets.eegbci import eegbci

from srcs.enums import TaskEnum, VerboseType


def load_dataset(
    subject: int = 1,
    task: List[int] = TaskEnum.Task1,
    verbose: VerboseType = VerboseType.ERROR,
):
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

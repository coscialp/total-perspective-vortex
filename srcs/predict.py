"""
Predict the target variable.

This script is used to predict the target variable using the trained model. It contains the following functions:

        * predict - predict the target variable

Usage:
    $ python predict.py
"""

import os
from time import sleep
from typing import List

import joblib
import numpy as np

from srcs.enums import TaskEnum

PIPELINE_PATH = lambda s, t: f"./data/pipeline_s{s}_t{t}.pkl"
TEST_DATA_PATH = lambda s, t: f"./data/test_data_s{s}_t{t}.pkl"


def predict(subject: int, tasks: List[int], verbose: bool = True):
    """Predict the target variable."""
    if verbose:
        print(f"Predicting for subject {subject} on task {tasks}.")

    # Check if the model has been trained
    assert os.path.exists(
        PIPELINE_PATH(subject, TaskEnum.index(tasks))
    ), "You must train your model first"
    assert os.path.exists(
        TEST_DATA_PATH(subject, TaskEnum.index(tasks))
    ), "You must train your model first"

    # Load the pipeline
    pipeline = joblib.load(PIPELINE_PATH(subject, TaskEnum.index(tasks)))

    # Load the test dataset
    test_dataset = joblib.load(TEST_DATA_PATH(subject, TaskEnum.index(tasks)))

    # Get the predictions
    predictions = pipeline.predict(test_dataset["X"])
    accuracy = np.mean(predictions == test_dataset["y"])

    if verbose:
        print(f"Epochs nb: [prediction] [truth] correct?")
        for index, value in enumerate(predictions):
            print(
                f"Epochs %d: %{10 - len(str(index))}s %10s %7s"
                % (
                    index,
                    f"[{value}]",
                    f"[{test_dataset['y'][index]}]",
                    value == test_dataset["y"][index],
                )
            )
            sleep(0.01)

        print(f"Accuracy: {accuracy:.3f}")

    return accuracy


if __name__ == "__main__":
    predict()

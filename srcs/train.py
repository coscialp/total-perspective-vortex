"""
This module is used to train the model.

This module trains the model for the project. It contains the following functions:

            * train - train the model

Usage:
    $ python train.py
"""

import os
import pickle
from typing import List

import joblib
from mne.decoding import CSP
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from srcs.enums import TaskEnum
from srcs.load_dataset import load_split_dataset


def save_pipeline(pipeline, subject, tasks, X_test, y_test):
    (
        os.remove(f"./data/test_data_s{subject}_t{TaskEnum.index(tasks)}.pkl")
        if os.path.exists(f"./data/test_data_s{subject}_t{TaskEnum.index(tasks)}.pkl")
        else None
    )

    (
        os.remove(f"./data/pipeline_s{subject}_t{TaskEnum.index(tasks)}.pkl")
        if os.path.exists(f"./data/pipeline_s{subject}_t{TaskEnum.index(tasks)}.pkl")
        else None
    )
    with open(
        f"./data/test_data_s{subject}_t{TaskEnum.index(tasks)}.pkl", "wb"
    ) as file:
        pickle.dump({"X": X_test, "y": y_test}, file)
    with open(f"./data/pipeline_s{subject}_t{TaskEnum.index(tasks)}.pkl", "wb") as f:
        joblib.dump(pipeline, f, compress=True)


def train(subject: int, tasks: List[int]):
    """Train the model."""
    print(f"Training model for subject {subject} on task {tasks}.")

    # Load the dataset and split it for testing
    X_train, X_test, y_train, y_test = load_split_dataset(subject, tasks)

    # Create pipeline
    pipeline = make_pipeline(CSP(), StandardScaler(), LogisticRegression())
    score = cross_val_score(pipeline, X_train, y_train, cv=KFold(n_splits=10))

    print(f"Cross validation score: {score.mean():.2f}")

    pipeline.fit(X_train, y_train)

    save_pipeline(pipeline, subject, tasks, X_test, y_test)

    print(
        f"Prediction accuracy on training dataset: {pipeline.score(X_train, y_train):.2f}"
    )
    print(f"Prediction accuracy on test dataset: {pipeline.score(X_test, y_test):.2f}")
    print("Training complete.")

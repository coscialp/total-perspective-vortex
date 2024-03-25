""" Command line interface for the project.

This module provides a command line interface for the project. It uses the `click` library to define
the commands and options.

Example:
    $ python ptv.py preprocess
    $ python ptv.py train
    $ python ptv.py predict
"""

import click

from srcs.enums import TaskEnum
from srcs.predict import predict as run_predict
from srcs.preprocess import preprocess as run_preprocess
from srcs.train import train as run_train

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

TASK_RANGE = TaskEnum.range()


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Command line interface for the project."""


@cli.command()
@click.option(
    "-s",
    "--subject",
    type=click.IntRange(1, 110),
    help="Subject number.",
    prompt="Enter the subject number (1<=subject<=110)",
)
@click.option(
    "-t",
    "--task",
    type=click.IntRange(TASK_RANGE[0], TASK_RANGE[1]),
    help="Task number.",
    prompt=f"Enter the task number ({TASK_RANGE[0]}<=task<={TASK_RANGE[1]})",
)
def preprocess(subject: int, task: int):
    """Preprocess the data."""
    print(f"Preprocessing data for subject {subject}.")
    run_preprocess(subject, TaskEnum.get(task))


@cli.command()
def train():
    """Train the model."""
    run_train()


@cli.command()
def predict():
    """Predict the target variable."""
    run_predict()


if __name__ == "__main__":
    cli()

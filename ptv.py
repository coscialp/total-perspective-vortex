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


def check_options(**kwargs):
    if kwargs["all_subjects_and_tasks"] and (
        kwargs["subject"] is not None or kwargs["task"] is not None
    ):
        raise click.UsageError(
            "Cannot use --all-subjects-and-tasks with --subject or --task."
        )
    if kwargs["all_tasks"] and kwargs["task"] is not None:
        raise click.UsageError("Cannot use --all-tasks with --task.")

    if kwargs["all_subjects_and_tasks"] and kwargs["all_tasks"]:
        raise click.UsageError("Cannot use --all-subjects-and-tasks with --all-tasks.")


@cli.command()
@click.option(
    "-a",
    "--all-subjects-and-tasks",
    is_flag=True,
    help="Compute all subjects for all tasks.",
)
@click.option(
    "-s",
    "--subject",
    type=click.IntRange(1, 110),
    help="Subject number.",
)
@click.option(
    "-t",
    "--task",
    type=click.IntRange(TASK_RANGE[0], TASK_RANGE[1]),
    help="Task number.",
)
@click.option(
    "-at",
    "--all-tasks",
    is_flag=True,
    help="Compute all tasks for a subject.",
)
def train(
    all_subjects_and_tasks: bool,
    subject: int,
    task: int,
    all_tasks: bool,
):
    """Train the model."""
    check_options(
        all_subjects_and_tasks=all_subjects_and_tasks,
        subject=subject,
        task=task,
        all_tasks=all_tasks,
    )
    if not all_subjects_and_tasks:
        subject = (
            subject
            if subject
            else click.prompt("Enter a subject number (1<=subject<=110)", type=int)
        )
        if not all_tasks:
            task = (
                task
                if task
                else click.prompt(
                    f"Enter a task number ({TASK_RANGE[0]}<=task<={TASK_RANGE[1]})",
                    type=int,
                )
            )
            run_train(subject, TaskEnum.get(task))
        else:
            for t in range(TASK_RANGE[0], TASK_RANGE[1] + 1):
                print(f"Training model for subject {subject} on task {t}.")
                run_train(subject, TaskEnum.get(t))
    else:
        for s in range(1, 110 + 1):
            for t in range(TASK_RANGE[0], TASK_RANGE[1] + 1):
                print(f"Training model for subject {s} on task {t}.")
                run_train(s, TaskEnum.get(t))


@cli.command()
@click.option(
    "-a",
    "--all-subjects",
    is_flag=True,
    help="Compute all subjects for all tasks.",
)
@click.option(
    "-s",
    "--subject",
    type=click.IntRange(1, 110),
    help="Subject number.",
)
@click.option(
    "-t",
    "--task",
    type=click.IntRange(TASK_RANGE[0], TASK_RANGE[1]),
    help="Task number.",
)
def predict(all_subjects: bool, subject: int, task: int):
    """Predict the target variable."""
    if not all_subjects:
        subject = (
            subject
            if subject
            else click.prompt("Enter a subject number (1<=subject<=110)", type=int)
        )
        task = (
            task
            if task
            else click.prompt(
                f"Enter a task number ({TASK_RANGE[0]}<=task<={TASK_RANGE[1]})",
                type=int,
            )
        )
        run_predict(subject, TaskEnum.get(task))
    else:
        for s in range(1, 110 + 1):
            for t in range(TASK_RANGE[0], TASK_RANGE[1] + 1):
                try:
                    run_predict(s, TaskEnum.get(t))
                except AssertionError:
                    print(f"Model not trained for subject {s} on task {t}.")


@cli.command()
def accuracy():
    """Get the accuracy of the model."""
    accuracies = []
    for s in range(1, 110 + 1):
        for t in range(TASK_RANGE[0], TASK_RANGE[1] + 1):
            try:
                acc = run_predict(s, TaskEnum.get(t), verbose=False)
                accuracies.append((s, t, acc))
                print(f"experiment {t} subject %03d accuracy = {acc:.2f}" % s)
            except AssertionError:
                continue

    print("")

    print("Mean accuracy of the six different experiments for all 110 subjects:")
    for t in range(TASK_RANGE[0], TASK_RANGE[1] + 1):
        acc = [acc for s, task, acc in accuracies if task == t]
        if not acc:
            continue
        print(f"experiment {t}: {sum(acc) / len(acc):.2f}")

    print(
        f"\nMean accuracy of {TASK_RANGE[1]} experiments: {sum(acc for s, task, acc in accuracies) / len(accuracies):.2f}"
    )


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        print(f"Error: {e}")

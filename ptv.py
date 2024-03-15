""" Command line interface for the project.

This module provides a command line interface for the project. It uses the `click` library to define
the commands and options.

Example:
    $ python ptv.py preprocess
    $ python ptv.py train
    $ python ptv.py predict
"""

import logging

import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Command line interface for the project."""


@cli.command()
def preprocess():
    """Preprocess the data."""


@cli.command()
def train():
    """Train the model."""


@cli.command()
def predict():
    """Predict the target variable."""


if __name__ == "__main__":
    cli()

import click

CONTEXT_SETTINGS = {
    "help_option_names": ['-h', '--help'],
}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
def preprocess():
    pass


@cli.command()
def train():
    pass


@cli.command()
def predict():
    pass


if __name__ == '__main__':
    cli()

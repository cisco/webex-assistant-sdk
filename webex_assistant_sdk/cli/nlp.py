from pprint import pformat
from typing import Optional

import typer

from webex_assistant_sdk.cli.config import get_skill_config
from webex_assistant_sdk.cli.helpers import create_nlp

app = typer.Typer(help='Commands for working with NLP models')


# take name to find app path, otherwise default to cwd
@app.command()
def build(name: Optional[str]):
    """Build nlp models associated with this skill"""
    app_dir = '.'
    if name:
        config = get_skill_config(name)
        app_dir = config['app_dir']

    nlp = create_nlp(app_dir)
    nlp.build()


@app.command()
def process(name: Optional[str]):
    """Run a query through NLP processing"""
    app_dir = '.'
    if name:
        config = get_skill_config(name)
        app_dir = config['app_dir']

    nlp = create_nlp(app_dir)
    nlp.load()

    typer.echo('Enter a query below (Ctl+C to exit)')
    query = typer.prompt('>>', prompt_suffix=' ')
    while True:
        output = nlp.process(query)
        typer.secho(pformat(output, indent=2, width=120), fg=typer.colors.GREEN)
        query = typer.prompt('>>', prompt_suffix=' ')

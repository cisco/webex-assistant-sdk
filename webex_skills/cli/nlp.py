from pprint import pformat
from typing import Optional

import typer

from .config import get_app_dir
from .helpers import create_nlp

app = typer.Typer(help='Commands for working with NLP models')


# take name to find app path, otherwise default to cwd
@app.command()
def build(name: Optional[str] = typer.Argument(None, help="The name of the skill to build.")):
    """Build nlp models associated with this skill"""
    app_dir = '.'
    if name:
        app_dir = get_app_dir(name)

    nlp = create_nlp(app_dir)
    nlp.build()


@app.command()
def process(name: Optional[str] = typer.Argument(None, help="The name of the skill to send the query to.")):
    """Run a query through NLP processing"""
    app_dir = '.'
    if name:
        app_dir = get_app_dir(name)

    nlp = create_nlp(app_dir)
    nlp.load()

    typer.echo('Enter a query below (Ctl+C to exit)')
    query = typer.prompt('>>', prompt_suffix=' ')
    while True:
        output = nlp.process(query)
        typer.secho(pformat(output, indent=2, width=120), fg=typer.colors.GREEN)
        query = typer.prompt('>>', prompt_suffix=' ')

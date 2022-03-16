from pprint import pformat
from typing import Optional

import typer

from webex_skills.cli.nlp_app.app import app
from webex_skills.cli.helpers import create_nlp
from webex_skills.cli.config import get_app_dir


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

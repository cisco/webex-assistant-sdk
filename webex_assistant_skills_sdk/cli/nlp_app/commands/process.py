from pprint import pformat
from typing import Optional

import typer

from webex_assistant_skills_sdk.cli.nlp_app.app import app
from webex_assistant_skills_sdk.cli.helpers import init_mindmeld_nlp


@app.command()
def process(name: Optional[str] = typer.Argument(None, help="The name of the skill to send the query to.")):
    """Run a query through NLP processing"""
    nlp = init_mindmeld_nlp()
    nlp.load()

    typer.echo('Enter a query below (Ctl+C to exit)')
    query = typer.prompt('>>', prompt_suffix=' ')
    while True:
        output = nlp.process(query)
        typer.secho(pformat(output, indent=2, width=120), fg=typer.colors.GREEN)
        query = typer.prompt('>>', prompt_suffix=' ')

from pathlib import Path
from pprint import pformat

import typer

from webex_assistant_skills_sdk.cli.nlp_app.app import app
from webex_assistant_skills_sdk.cli.shared.helpers import init_mindmeld_nlp


@app.command()
def process(
    query: str = typer.Option(
        ...,
        help='',
    ),
    app_path: Path = typer.Option(
        Path.cwd(),
        '--path',
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        help='',
    ),
):
    """Run a query through NLP processing"""
    nlp = init_mindmeld_nlp(str(app_path))
    nlp.load()

    result = nlp.process(query)

    typer.echo(pformat(result, indent=2, width=120))
 
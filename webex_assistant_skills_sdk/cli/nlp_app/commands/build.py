from pathlib import Path

import typer

from webex_assistant_skills_sdk.cli.nlp_app.app import app
from webex_assistant_skills_sdk.cli.shared.helpers import init_mindmeld_nlp


@app.command()
def build(
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
) -> None:
    """Build nlp models associated with this skill"""
    nlp = init_mindmeld_nlp(app_path=app_path)
    nlp.build()

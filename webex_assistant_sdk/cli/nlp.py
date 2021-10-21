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
def process():
    """Run a query through NLP processing"""

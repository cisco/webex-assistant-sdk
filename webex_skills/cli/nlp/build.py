from typing import Optional

import typer

from webex_skills.cli.nlp.app import nlp_app
from webex_skills.cli.helpers import create_nlp
from webex_skills.cli.config import get_app_dir


# take name to find app path, otherwise default to cwd
@nlp_app.command()
def build(name: Optional[str] = typer.Argument(None, help="The name of the skill to build.")):
    """Build nlp models associated with this skill"""
    app_dir = '.'
    if name:
        app_dir = get_app_dir(name)

    nlp = create_nlp(app_dir)
    nlp.build()

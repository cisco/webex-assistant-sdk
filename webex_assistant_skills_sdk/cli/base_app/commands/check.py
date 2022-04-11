from pprint import pformat
from typing import Optional
from uuid import UUID, uuid4

from dependency_injector.providers import Factory
from dependency_injector.wiring import Provider
from httpx import HTTPStatusError
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_assistant_skills_sdk.cli.shared.services import CliInvoker
from webex_assistant_skills_sdk.cli.types import Types
from webex_assistant_skills_sdk.shared.models import Dialogue


_invoker_factory: Factory[CliInvoker] = Provider[Types.INVOKER]

@app.command()
def check(
    skill_name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help='',
    ),
    encrypted: Optional[bool] = typer.Option(
        True,
        help=''
    ),
) -> None:
    invoker = _invoker_factory(
        skill_name,
        encrypted,
    )

    response, success = invoker.check()

    if not success:
        typer.echo(f'Invalid challenge response {response.challenge}')
        return

    typer.echo('OK')

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


__invoker_factory: Factory[CliInvoker] = Provider[Types.INVOKER]

def should_end_dialogue(dialogue: Dialogue):
    turn = dialogue.get_last_turn()

    if turn is None:
        return False

    for directive in turn.directives:
        if directive.name == 'sleep':
            return True

    return False

@app.command()
def invoke(
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
    org_id: Optional[str] = typer.Option(
        uuid4,
        show_default=False,
        help='',
    ),
    user_id: Optional[str] = typer.Option(
        uuid4,
        show_default=False,
        help='',
    ),
    device_id: Optional[str] = typer.Option(
        uuid4,
        show_default=False,
        help='',
    ),
) -> None:
    invoker = __invoker_factory(
        skill_name,
        encrypted,
        org_id,
        user_id,
        device_id,
    )

    dialogue = Dialogue()

    while not should_end_dialogue(dialogue):
        query = typer.prompt('query')

        try:
            invoker.do_turn(dialogue, query)
        except HTTPStatusError as e:
            typer.echo(f'Skill responded with status code {e.response.status_code}')
            raise typer.Exit(1)

        last_turn = dialogue.get_last_turn()
        if last_turn is None:
            # TODO: custom exception
            raise Exception()

        typer.echo(pformat(
            last_turn.json(),
            indent=2,
            width=120,
        ))

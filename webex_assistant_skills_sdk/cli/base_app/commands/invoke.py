from typing import Optional
from uuid import UUID, uuid4

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_assistant_skills_sdk.cli.services import CliConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

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
    org_id: Optional[UUID] = typer.Option(
        uuid4,
        show_default=False,
        help='',
    ),
    user_id: Optional[UUID] = typer.Option(
        uuid4,
        show_default=False,
        help='',
    ),
    device_id: Optional[UUID] = typer.Option(
        uuid4,
        show_default=False,
        help='',
    ),
) -> None:
    skill_config = __cli_config_service.get_skill_config()

    ## TODO: dialog factory, skill invoker, cryptography service

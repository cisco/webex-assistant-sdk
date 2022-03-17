from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_assistant_skills_sdk.cli.services import CliConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

@app.command()
def delete(
    skill_name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help=''
    )
) -> None:
    __cli_config_service.delete_skill_config(skill_name)

    __cli_config_service.save_config()

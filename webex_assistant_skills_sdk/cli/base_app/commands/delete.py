from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_assistant_skills_sdk.cli.shared.services import ConfigService
from webex_assistant_skills_sdk.cli.types import Types


_cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

@app.command()
def delete(
    skill_name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help=''
    )
) -> None:
    _cli_config_service.delete_skill_config(skill_name)

    _cli_config_service.save_config()

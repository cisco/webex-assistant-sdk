from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_assistant_skills_sdk.cli.shared.services import ConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

@app.command()
def inspect(
    name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help=''
    )
) -> None:
    skill_config = __cli_config_service.get_skill_config(name)

    typer.echo(skill_config.json(indent=2))

from dependency_injector.wiring import Provide
import typer

from webex_skills.cli.base_app.app import app
from webex_skills.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_skills.cli.services import CliConfigService
from webex_skills.cli.types import Types


cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

@app.command()
def delete(
    name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help=''
    )
) -> None:
    cli_config_service.delete_skill_config(name)

    cli_config_service.save_config()

    typer.echo(f'Successfully deleted the configuration for "{name}"')

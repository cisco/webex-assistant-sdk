from dependency_injector.wiring import Provide
import typer

from webex_skills.cli.base_app.app import app
from webex_skills.cli.services import CliConfigService
from webex_skills.cli.types import Types


cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

@app.command()
def list() -> None:
    typer.echo('\n'.join(cli_config_service.get_skill_names()))

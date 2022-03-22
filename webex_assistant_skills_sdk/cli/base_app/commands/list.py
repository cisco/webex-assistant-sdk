from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.shared.services import ConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

@app.command()
def list() -> None:
    typer.echo('\n'.join(__cli_config_service.get_skill_names()))

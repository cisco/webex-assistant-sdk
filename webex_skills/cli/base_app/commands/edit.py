from pathlib import Path

from dependency_injector.wiring import Provide
import typer

from webex_skills.cli.base_app.app import app
from webex_skills.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_skills.cli.services import CliConfigService
from webex_skills.cli.types import Types


cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

@app.command()
def edit(
    name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help='The name of the skill',
    ),
    url: str = typer.Option(
        'http://localhost:8080/parse',
        help='The URL of the skill',
    ),
    secret: str = typer.Option(
        None,
        envvar='SKILLS_SECRET',
        show_envvar=False,
        prompt=True,
        help='The skill secret',
    ),
    public_key_path: Path = typer.Option(
        Path.cwd() / 'id_rsa.pub',
        '--key',
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help='The path to the public key',
    ),
) -> None:
    pass

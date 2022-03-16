from pathlib import Path

from dependency_injector.wiring import Provide
import typer

from webex_skills.cli.base_app.app import app
from webex_skills.cli.base_app.helpers import validate_skill_name_not_exists
from webex_skills.cli.models import SkillConfig
from webex_skills.cli.services import CliConfigService
from webex_skills.cli.types import Types


cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

@app.command()
def add(
    name: str = typer.Argument(
        ...,
        callback=validate_skill_name_not_exists,
        help='The name of the skill',
    ),
    url: str = typer.Option(
        'http://localhost:8080/parse',
        prompt=True,
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
        prompt=True,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help='The path to the public key',
    ),
):
    '''Add the configuration for a skill'''
    skill_config = SkillConfig(
        name=name,
        url=url,
        secret=secret,
        public_key=public_key_path.read_text(),
    )

    cli_config_service.set_skill_config(skill_config)

    cli_config_service.save_config()

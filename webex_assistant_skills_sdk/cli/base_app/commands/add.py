from pathlib import Path

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import validate_skill_name_not_exists
from webex_assistant_skills_sdk.cli.shared.models import SkillConfig
from webex_assistant_skills_sdk.cli.shared.services import ConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

@app.command()
def add(
    skill_name: str = typer.Argument(
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
        '--key-path',
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
        name=skill_name,
        url=url,
        secret=secret,
        public_key=public_key_path.read_text(encoding='utf-8'),
    )

    __cli_config_service.set_skill_config(skill_config)

    __cli_config_service.save_config()

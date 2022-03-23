from pathlib import Path
from typing import Optional

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import validate_skill_name_not_exists
from webex_assistant_skills_sdk.cli.crypto_app.commands.generate_secret import generate_secret
from webex_assistant_skills_sdk.cli.shared.models.config import SkillConfig
from webex_assistant_skills_sdk.cli.shared.models.template_types import TemplateTypes
from webex_assistant_skills_sdk.cli.shared.services import ConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

@app.command()
def init(
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
        generate_secret,
        envvar='SKILLS_SECRET',
        show_envvar=False,
        prompt=True,
        help='The skill secret',
    ),
    directory_path: Path = typer.Option(
        Path.cwd(),
        '--path',
        prompt=True,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        help='The path to the public key',
    ),
    template_type: Optional[TemplateTypes] = typer.Option(
        None,
        '--template',
        case_sensitive=False,
        prompt=True,
        help='',
    )
) -> None:
    if template_type is not None:
        # TODO: template generation
        pass

    public_key_path = directory_path / 'id_rsa.pub'

    skill_config = SkillConfig(
        name=skill_name,
        url=url,
        secret=secret,
        public_key=public_key_path.read_text(encoding='utf-8'),
    )

    __cli_config_service.set_skill_config(skill_config)

    __cli_config_service.save_config()

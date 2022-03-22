from pathlib import Path
from typing import Optional

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.base_app.app import app
from webex_assistant_skills_sdk.cli.base_app.helpers import autocomplete_skill_name, validate_skill_name_exists
from webex_assistant_skills_sdk.cli.shared.services import ConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: ConfigService = Provide[Types.CONFIG_SERVICE]

@app.command()
def edit(
    skill_name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_skill_name,
        callback=validate_skill_name_exists,
        help='The name of the skill',
    ),
    url: Optional[str] = typer.Option(
        None,
        help='The URL of the skill',
    ),
    secret: Optional[str] = typer.Option(
        None,
        envvar='SKILLS_SECRET',
        show_envvar=False,
        help='The skill secret',
    ),
    public_key_path: Optional[Path] = typer.Option(
        None,
        '--key-path',
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help='The path to the public key',
    ),
) -> None:
    skill_config = __cli_config_service.get_skill_config(skill_name)

    if url is not None:
        skill_config.url = url

    if secret is not None:
        skill_config.secret = secret

    if public_key_path is not None:
        skill_config.public_key = public_key_path.read_text(encoding='utf-8')

    __cli_config_service.save_config()

    # TODO: print config

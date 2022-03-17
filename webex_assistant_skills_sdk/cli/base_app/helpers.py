from typing import Iterator, Optional

from dependency_injector.wiring import Provide
import typer

from webex_assistant_skills_sdk.cli.services import CliConfigService
from webex_assistant_skills_sdk.cli.types import Types


__cli_config_service: CliConfigService = Provide[Types.CLI_CONFIG_SERVICE]

def validate_skill_name_not_exists(ctx: typer.Context, skill_name: str) -> Optional[str]:
    if ctx.resilient_parsing:
        return

    if skill_name in __cli_config_service.get_skill_names():
        raise typer.BadParameter(f'A skill with name "{skill_name}" already exists')

    return skill_name

def autocomplete_skill_name(partial_skill_name: str) -> Iterator[str]:
    for skill_name in __cli_config_service.get_skill_names():
        if skill_name.startswith(partial_skill_name):
            yield skill_name

def validate_skill_name_exists(ctx: typer.Context, skill_name: str) -> Optional[str]:
    if ctx.resilient_parsing:
        return

    if skill_name not in __cli_config_service.get_skill_names():
        raise typer.BadParameter(f'A skill with name "{skill_name}" does not exist')

    return skill_name
from dependency_injector import containers, providers

from webex_assistant_skills_sdk.cli.services import CliConfigService
from webex_assistant_skills_sdk.cli.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CLI_CONFIG_SERVICE, providers.Singleton(CliConfigService))

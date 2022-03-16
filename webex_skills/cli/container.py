from dependency_injector import containers, providers

from webex_skills.cli.services import CliConfigService
from webex_skills.cli.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CLI_CONFIG_SERVICE, providers.Singleton(CliConfigService))

from dependency_injector import containers, providers

from webex_assistant_skills_sdk.cli.shared.services import CliConfigService, CliCryptoService
from webex_assistant_skills_sdk.cli.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CLI_CONFIG_SERVICE, providers.Singleton(CliConfigService))
    setattr(container, Types.CLI_CRYPTO_SERVICE, providers.Singleton(CliCryptoService))

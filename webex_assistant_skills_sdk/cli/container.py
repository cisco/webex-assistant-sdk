from dependency_injector import containers, providers

from webex_assistant_skills_sdk.cli.shared.services import ConfigService, CryptoGenService
from webex_assistant_skills_sdk.cli.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CONFIG_SERVICE, providers.Singleton(ConfigService))
    setattr(container, Types.CRYPTO_GEN_SERVICE, providers.Singleton(CryptoGenService))

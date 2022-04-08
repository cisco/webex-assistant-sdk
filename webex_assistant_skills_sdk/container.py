from dependency_injector import containers, providers

from webex_assistant_skills_sdk.shared import services
from webex_assistant_skills_sdk.shared.services import CryptoService, Invoker, Settings


class BaseContainer(containers.DeclarativeContainer):
    crypto_service = providers.Factory(CryptoService)
    invoker = providers.Factory(Invoker)
    settings = providers.Singleton(Settings)

    wiring_config = containers.WiringConfiguration(packages=[
        services,
    ])


container = BaseContainer()

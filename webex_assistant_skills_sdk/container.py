from dependency_injector import containers, providers

from webex_assistant_skills_sdk.shared import services
from webex_assistant_skills_sdk.shared.services import CryptoService, Invoker, Settings
from webex_assistant_skills_sdk.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CRYPTO_SERVICE, providers.Factory(CryptoService))
    setattr(container, Types.INVOKER, providers.Factory(Invoker))
    setattr(container, Types.SETTINGS, providers.Singleton(Settings))


def create_container() -> containers.Container:
    container = containers.DynamicContainer()
    populate_container(container)

    container.wire(packages=[
        services,
    ])

    return container


container = create_container()

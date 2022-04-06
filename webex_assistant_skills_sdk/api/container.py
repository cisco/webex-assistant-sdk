from dependency_injector import containers, providers

from webex_assistant_skills_sdk.container import container as base_container
from webex_assistant_skills_sdk.api import shared
from webex_assistant_skills_sdk.api.shared.services import CryptoService
from webex_assistant_skills_sdk.api.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CRYPTO_SERVICE, providers.Factory(CryptoService))


def create_container(parent_container: containers.Container) -> containers.Container:
    container = containers.DynamicContainer()
    container.assign_parent(parent_container)

    populate_container(container)

    container.wire(packages=[
        shared,
    ])

    return container


container = create_container(
    parent_container=base_container,
)

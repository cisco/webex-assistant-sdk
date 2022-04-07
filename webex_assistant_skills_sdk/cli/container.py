from dependency_injector import containers, providers

from webex_assistant_skills_sdk.container import container as base_container
from webex_assistant_skills_sdk.cli import base_app
from webex_assistant_skills_sdk.cli import crypto_app
from webex_assistant_skills_sdk.cli import nlp_app
from webex_assistant_skills_sdk.cli.shared.services import ConfigService, CryptoGenService, CliInvoker
from webex_assistant_skills_sdk.cli.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.CONFIG_SERVICE, providers.Singleton(ConfigService))
    setattr(container, Types.CRYPTO_SERVICE, providers.Factory(CryptoGenService))
    setattr(container, Types.INVOKER, providers.Factory(CliInvoker))


def create_container(parent_container: containers.Container) -> containers.Container:
    container = containers.DynamicContainer()
    container.assign_parent(parent_container)

    populate_container(container)

    container.wire(packages=[
        base_app,
        crypto_app,
        nlp_app,
    ])

    return container

container = create_container(
    parent_container=base_container,
)

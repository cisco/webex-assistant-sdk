from dependency_injector import containers, providers

from webex_assistant_skills_sdk.container import BaseContainer
from webex_assistant_skills_sdk.cli import base_app
from webex_assistant_skills_sdk.cli import crypto_app
from webex_assistant_skills_sdk.cli import nlp_app
from webex_assistant_skills_sdk.cli.shared.services import ConfigService, CryptoGenService, CliInvoker


class CliContainer(BaseContainer):
    config_service = providers.Singleton(ConfigService)
    crypto_service = providers.Factory(CryptoGenService)
    invoker = providers.Factory(CliInvoker)

    wiring_config = containers.WiringConfiguration(packages=[
        base_app,
        crypto_app,
        nlp_app,
    ])


container = CliContainer()

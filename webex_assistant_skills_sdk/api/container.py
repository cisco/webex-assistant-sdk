from dependency_injector import containers, providers

from webex_assistant_skills_sdk.container import BaseContainer
from webex_assistant_skills_sdk.api import middlewares, shared
from webex_assistant_skills_sdk.api.shared.services import CryptoService


class ApiContainer(BaseContainer):
    crypto_service = providers.Factory(CryptoService)

    wiring_config = containers.WiringConfiguration(packages=[
        middlewares,
        shared,
    ])


container = ApiContainer()

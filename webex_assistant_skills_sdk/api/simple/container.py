from dependency_injector import containers, providers

from webex_assistant_skills_sdk.api.container import ApiContainer
from webex_assistant_skills_sdk.api.simple import api
from webex_assistant_skills_sdk.api.simple import services
from webex_assistant_skills_sdk.api.simple.services import SimpleDialogueManager


class SimpleApiContainer(ApiContainer):
    dialogue_manager = providers.Singleton(SimpleDialogueManager)

    wiring_config = containers.WiringConfiguration(
        modules=[
            api,
        ],
        packages=[
            services,
        ],
    )


container = SimpleApiContainer()

from dependency_injector import containers, providers

from webex_assistant_skills_sdk.api.container import ApiContainer
from webex_assistant_skills_sdk.api.mindmeld import api
from webex_assistant_skills_sdk.api.mindmeld import services
from webex_assistant_skills_sdk.api.mindmeld.services import MindmeldDialogueManager


class MindmeldApiContainer(ApiContainer):
    dialogue_manager = providers.Singleton(MindmeldDialogueManager)

    wiring_config = containers.WiringConfiguration(
        modules=[
            api,
        ],
        packages=[
            services,
        ],
    )


container = MindmeldApiContainer()

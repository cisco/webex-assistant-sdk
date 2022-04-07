from dependency_injector import containers, providers

from webex_assistant_skills_sdk.api.container import container as base_container
from webex_assistant_skills_sdk.api.mindmeld import api
from webex_assistant_skills_sdk.api.mindmeld import services
from webex_assistant_skills_sdk.api.mindmeld.services import MindmeldDialogueManager
from webex_assistant_skills_sdk.api.types import Types


def populate_container(container: containers.DynamicContainer) -> None:
    setattr(container, Types.DIALOGUE_MANAGER, providers.Singleton(MindmeldDialogueManager))


def create_container(parent_container: containers.Container) -> containers.Container:
    container = containers.DynamicContainer()
    container.assign_parent(parent_container)

    populate_container(container)

    container.wire(
        modules=[
            api,
        ],
        packages=[
            services,
        ]
    )

    return container


container = create_container(
    parent_container=base_container,
)
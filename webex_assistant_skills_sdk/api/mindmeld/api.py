from typing import Callable
import warnings


from webex_assistant_skills_sdk.api import BaseAPI
from webex_assistant_skills_sdk.api.mindmeld.models import ProcessedQuery
from webex_assistant_skills_sdk.api.mindmeld.services import MindmeldDialogueHandler, MindmeldDialogueManager
from webex_assistant_skills_sdk.shared.models import DialogueTurn, InvokeRequest, InvokeResponse

try:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        from mindmeld import NaturalLanguageProcessor
except ImportError:
    # TODO: custom exception
    raise Exception('You must install the extras package webex-assistant-sdk[mindmeld] to use MindmeldAPI')


class MindmeldAPI(BaseAPI):
    dialogue_manager = MindmeldDialogueManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.nlp = NaturalLanguageProcessor(self.__settings.app_dir)
        self.nlp.load()

    async def parse(self, request: InvokeRequest) -> InvokeResponse:
        """A default parse method for mindmeld apps so the user only has to handle dialogue stuff"""

        turn = DialogueTurn(**request.dict())
        processed_query_dict: dict = self.nlp.process(
            query_text=request.text,
            locale=request.params.locale,
            language=request.params.language,
            time_zone=request.params.time_zone,
            timestamp=request.params.timestamp,
            dynamic_resource=request.params.dynamic_resource,
        )

        processed_query = ProcessedQuery(**processed_query_dict)

        next_turn = await self.dialogue_manager.handle(
            query=processed_query,
            turn=turn
        )

        return InvokeResponse(
            **next_turn.dict(),
            challenge=request.challenge
        )

    def handle(
        self,
        *,
        domain=None,
        intent=None,
        entities=None,
        default=False,
        targeted_only=False
    ) -> Callable[[MindmeldDialogueHandler], MindmeldDialogueHandler]:
        """Wraps a function to behave as a dialogue handler"""
        return self.dialogue_manager.add_rule(
            domain=domain,
            intent=intent,
            entities=entities,
            default=default,
            targeted_only=targeted_only,
        )

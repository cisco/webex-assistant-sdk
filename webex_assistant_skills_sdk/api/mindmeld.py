from typing import cast

from ..dialogue.manager import MMDialogueManager
from ..models.http import SkillInvokeRequest, SkillInvokeResponse
from ..models.mindmeld import DialogueState, ProcessedQuery
from ..supress_warnings import suppress_warnings
from .base import BaseAPI


class MindmeldAPI(BaseAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.nlp:
            with suppress_warnings():
                from mindmeld import NaturalLanguageProcessor  # pylint:disable=import-outside-toplevel

                self.nlp = NaturalLanguageProcessor(self.settings.app_dir)
                self.nlp.load()

        if not self.dialogue_manager:
            self.dialogue_manager = MMDialogueManager()

    async def parse(self, request: SkillInvokeRequest):
        """A default parse method for mindmeld apps so the user only has to handle dialogue stuff"""

        current_state = DialogueState(**request.dict())
        processed_query = self.nlp.process(
            query_text=request.text,
            locale=request.params.locale,
            language=request.params.language,
            time_zone=request.params.time_zone,
            timestamp=request.params.timestamp,
            dynamic_resource=request.params.dynamic_resource,
        )

        # Just here to make type checking happy because NLP.process incorrectly defines it's return type
        processed_query = cast(dict, processed_query)

        processed_query = ProcessedQuery(**processed_query)
        new_state = await self.dialogue_manager.handle(processed_query, current_state)
        response = SkillInvokeResponse(**new_state.dict(), challenge=request.challenge)
        return response

    def handle(self, *, domain=None, intent=None, entities=None, default=False, targeted_only=False):
        """Wraps a function to behave as a dialogue handler"""
        return self.dialogue_manager.add_rule(
            domain=domain,
            intent=intent,
            entities=entities,
            default=default,
            targeted_only=targeted_only,
        )

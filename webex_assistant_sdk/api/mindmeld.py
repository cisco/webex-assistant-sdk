import warnings

from ..dialogue.manager import MMDialogueManager
from ..models.http import SkillInvokeRequest, SkillInvokeResponse
from ..models.mindmeld import DialogueState, ProcessedQuery
from .base import BaseAPI


class suppress_warnings:
    def __init__(self):
        self._showwarning = None

    def showwarning(self, *args, **kwargs):
        pass

    def __enter__(self):
        self._showwarning = warnings.showwarning
        warnings.showwarning = self.showwarning

    def __exit__(self, exc_type, exc_val, exc_tb):
        warnings.showwarning = self._showwarning
        return


with suppress_warnings():
    from mindmeld import NaturalLanguageProcessor


class MindmeldAPI(BaseAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nlp = NaturalLanguageProcessor(self.settings.app_dir)
        self.nlp.load()
        self.dialogue_manager = MMDialogueManager()

    async def parse(self, request: SkillInvokeRequest):
        current_state = DialogueState(**request.dict())
        """A default parse method for mindmeld apps so the user only has to handle dialogue stuff"""
        processed_query = self.nlp.process(
            query_text=request.text,
            locale=request.params.locale,
            language=request.params.language,
            time_zone=request.params.time_zone,
            timestamp=request.params.timestamp,
            dynamic_resource=request.params.dynamic_resource,
        )

        processed_query = ProcessedQuery(**processed_query)  # type: ignore
        # This should invoke the relevant function, wrapped so that the end result of the dialogue flow can be
        # serialized to a json response using one of our pydantic objects
        new_state = await self.dialogue_manager.handle(processed_query, current_state)

        # new_state = self.update_history(current_state, new_state)
        response = SkillInvokeResponse(**new_state.dict(), challenge=request.challenge)
        return response

    def handle(self, *, domain=None, intent=None, entities=None):
        """Wraps a function to behave as a dialogue handler"""
        return self.dialogue_manager.add_rule(domain=domain, intent=intent, entities=entities)

    def update_history(self, old_state, new_state) -> DialogueState:
        """Append the most recent request (sans it's history entries) on to the response history"""

import warnings

from mindmeld.core import ProcessedQuery

from webex_assistant_sdk.api.base import BaseAPI
from webex_assistant_sdk.models.http import SkillInvokeRequest


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


# TODO: Figure out dialogue manager stuff
class MindmeldAPI(BaseAPI):
    async def parse(self, invoke_request: SkillInvokeRequest):
        """A default parse method for mindmeld apps so the user only has to handle dialogue stuff"""
        processed_query: ProcessedQuery = self.nlp.process(
            query_text=invoke_request.text,
            locale=invoke_request.params.locale,
            language=invoke_request.params.language,
            time_zone=invoke_request.params.time_zone,
            timestamp=invoke_request.params.timestamp,
            dynamic_resource=invoke_request.params.dynamic_resource,
        )
        # This should invoke the relevant function, wrapped so that the end result of the dialogue flow can be
        # serialized to a json response using one of our pydantic objects
        return self.dm.handle(processed_query)

    def init_mm(self):
        with suppress_warnings():
            # TODO: Update routes so parse_mm handles the /parse endpoint
            # TODO: Initialize NLP and DM
            from mindmeld import NaturalLanguageProcessor
            from mindmeld.components import DialogueManager

            self.nlp = NaturalLanguageProcessor(self.settings.app_dir)
            self.dm = DialogueManager()

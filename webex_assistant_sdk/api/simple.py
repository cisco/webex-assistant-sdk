from typing import Any

from webex_assistant_sdk.api.base import BaseAPI
from webex_assistant_sdk.models.http import SkillInvokeRequest


class API(BaseAPI):
    def __init__(self, *args, **extra: Any) -> None:

        super().__init__(*args, **extra)
        self.skill_name = self.settings.skill_name

    async def parse(self, request: SkillInvokeRequest):
        # This should follow the same sort of process as the parse_mm method except
        # without the nlp step. Our handlers in that case will
        pass

    def handle(self):
        """Wraps a function to behave as a dialogue handler"""
        pass

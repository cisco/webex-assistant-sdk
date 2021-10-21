from typing import Any, Optional

from webex_assistant_sdk.api.base import BaseAPI
from webex_assistant_sdk.dialogue.manager import SimpleDialogueManager
from webex_assistant_sdk.models.http import SkillInvokeRequest, SkillInvokeResponse
from webex_assistant_sdk.models.mindmeld import DialogueState


class SimpleAPI(BaseAPI):
    def __init__(self, **extra: Any) -> None:
        super().__init__(**extra)
        if not self.dialogue_manager:
            self.dialogue_manager = SimpleDialogueManager()

    async def parse(self, request: SkillInvokeRequest) -> SkillInvokeResponse:
        current_state = DialogueState(**request.dict())
        new_state = await self.dialogue_manager.handle(query=current_state.text, current_state=current_state)
        response = SkillInvokeResponse(**new_state.dict(), challenge=request.challenge)
        return response

    def handle(self, *, pattern: Optional[str] = None, default=False, targeted_only=False):
        """Wraps a function to behave as a dialogue handler"""
        return self.dialogue_manager.add_rule(pattern=pattern, default=default, targeted_only=targeted_only)

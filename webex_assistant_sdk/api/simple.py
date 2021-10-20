from typing import Any, Optional

from webex_assistant_sdk.api.base import BaseAPI
from webex_assistant_sdk.dialogue.manager import SimpleDialogueManager
from webex_assistant_sdk.models.http import SkillInvokeRequest, SkillInvokeResponse
from webex_assistant_sdk.models.mindmeld import DialogueState

# TODO: Update history


class SimpleAPI(BaseAPI):
    def __init__(self, *args, dialogue_manager=None, **extra: Any) -> None:
        super().__init__(*args, **extra)
        self.skill_name = self.settings.skill_name
        self.dialogue_manager = dialogue_manager or SimpleDialogueManager()

    async def parse(self, request: SkillInvokeRequest) -> SkillInvokeResponse:
        current_state = DialogueState(**request.dict())
        new_state = await self.dialogue_manager.handle(current_state)
        response = SkillInvokeResponse(**new_state.dict(), challenge=request.challenge)
        return response

    def handle(self, *, pattern: Optional[str] = None, default=False, targeted_only=False):
        """Wraps a function to behave as a dialogue handler"""
        return self.dialogue_manager.add_rule(pattern=pattern, default=default, targeted_only=targeted_only)

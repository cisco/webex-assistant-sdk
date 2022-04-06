from typing import Optional

from webex_assistant_skills_sdk.api import BaseAPI
from webex_assistant_skills_sdk.api.simple.services import SimpleDialogueManager
from webex_assistant_skills_sdk.shared.models import DialogueTurn, InvokeRequest, InvokeResponse


class SimpleAPI(BaseAPI):
    dialogue_manager = SimpleDialogueManager()

    async def parse(self, request: InvokeRequest) -> InvokeResponse:
        turn = DialogueTurn(**request.dict())

        next_turn = await self.dialogue_manager.handle(
            query=turn.text,
            turn=turn,
        )

        return InvokeResponse(
            **next_turn.dict(),
            challenge=request.challenge,
        )

    def handle(
        self,
        *,
        pattern: Optional[str] = None,
        default=False,
        targeted_only=False,
    ):
        """Wraps a function to behave as a dialogue handler"""
        return self.dialogue_manager.add_rule(
            pattern=pattern,
            default=default,
            targeted_only=targeted_only,
        )

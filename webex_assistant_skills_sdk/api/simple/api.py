from typing import Callable, Optional

from dependency_injector.wiring import Provide

from webex_assistant_skills_sdk.api import BaseAPI
from webex_assistant_skills_sdk.api.simple.services import SimpleDialogueHandler, SimpleDialogueManager
from webex_assistant_skills_sdk.shared.models import DialogueTurn, InvokeRequest, InvokeResponse
from webex_assistant_skills_sdk.api.types import Types


class SimpleAPI(BaseAPI):
    __dialogue_manager: SimpleDialogueManager = Provide[Types.DIALOGUE_MANAGER]

    async def parse(self, request: InvokeRequest) -> InvokeResponse:
        turn = DialogueTurn(**request.dict())

        next_turn = await self.__dialogue_manager.handle(
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
    ) -> Callable[[SimpleDialogueHandler], SimpleDialogueHandler]:
        """Wraps a function to behave as a dialogue handler"""
        return self.__dialogue_manager.add_rule(
            pattern=pattern,
            default=default,
            targeted_only=targeted_only,
        )

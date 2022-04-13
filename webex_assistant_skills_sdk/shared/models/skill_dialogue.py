from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.base_directive import Directive
from webex_assistant_skills_sdk.shared.models.context import DeviceContext
from webex_assistant_skills_sdk.shared.models.params import DialogueParams


class SkillRequest(BaseModel):
    text: str
    context: DeviceContext
    frame: Dict[str, Any]
    params: DialogueParams
    history: List[SkillRequest] = []


class SkillResponse(BaseModel):
    directives: List[Directive]
    frame: Dict[str, Any] = {}


class AugmentedSkillResponse(SkillResponse):
    params: DialogueParams
    history: List[SkillRequest]

    @staticmethod
    def augment_response(
        request: SkillRequest,
        response: SkillResponse,
    ) -> AugmentedSkillResponse:
        return AugmentedSkillResponse(
            **response.dict(),
            params=request.params,
            history=AugmentedSkillResponse.update_history(request.history, request)
        )

    @staticmethod
    def update_history(
        history: List[SkillRequest],
        request: SkillRequest,
    ) -> List[SkillRequest]:
        history.append(SkillRequest(
            **request.dict(exclude={'history'}),
        ))

        return history

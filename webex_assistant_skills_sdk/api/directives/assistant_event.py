from typing import Any, Dict

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class AssistantEventPayload(BaseModel):
    name: str
    payload: Dict[str, Any]


class AssistantEvent(Directive):
    name: str = 'assistant-event'
    payload: AssistantEventPayload

    def __init__(
        self,
        name: str,
        payload: Dict[str, Any] = {},
    ) -> None:
        super().__init__(payload=AssistantEventPayload(
            name=name,
            payload=payload,
        ))

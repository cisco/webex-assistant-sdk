from ast import Dict
from typing import Any

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class AssistantEventPayload(BaseModel):
    name: str
    payload: Dict[str, Any]


class AssistantEvent(Directive):
    name: str = 'assistant-event'
    payload: AssistantEventPayload

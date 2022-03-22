from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class SleepPayload(BaseModel):
    delay: int


class Sleep(Directive):
    name: str = 'sleep'
    payload: SleepPayload

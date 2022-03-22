from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class SpeakPayload(BaseModel):
    text: str


class Speak(Directive):
    name: str = 'speak'
    payload: SpeakPayload

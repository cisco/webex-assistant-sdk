from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class SpeakPayload(BaseModel):
    text: str


class Speak(Directive):
    name: str = 'speak'
    payload: SpeakPayload

    def __init__(
        self,
        text: str
    ):
        super().__init__(payload=SpeakPayload(
            text=text,
        ))

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class SleepPayload(BaseModel):
    delay: int


class Sleep(Directive):
    name: str = 'sleep'
    payload: SleepPayload

    def __init__(
        self,
        *,
        delay: int,
    ) -> None:
        super().__init__(payload=SleepPayload(
            delay=delay,
        ))

from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models import Directive


class ReplyPayload(BaseModel):
    text: str


class Reply(Directive):
    name: str = 'reply'
    payload: ReplyPayload

    def __init__(
        self,
        *,
        text: str,
    ) -> None:
        super().__init__(payload=ReplyPayload(
            text=text,
        ))

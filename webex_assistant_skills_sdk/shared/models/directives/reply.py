from pydantic import BaseModel

from webex_assistant_skills_sdk.shared.models.directives.base_directive import Directive


class ReplyPayload(BaseModel):
    text: str


class Reply(Directive):
    name: str = 'reply'
    payload: ReplyPayload

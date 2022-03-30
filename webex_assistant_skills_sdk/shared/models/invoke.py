from pydantic import BaseModel, constr

from webex_assistant_skills_sdk.shared.models.dialogue import DialogueEventBase, DialogueTurn


class EncryptedInvokeRequest(BaseModel):
    signature: str
    token: str


class InvokeRequest(DialogueTurn):
    challenge: constr(min_length=64, max_length=64)


class InvokeResponse(DialogueEventBase):
    challenge: constr(min_length=64, max_length=64)

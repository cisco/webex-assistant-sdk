from pydantic import BaseModel, constr

from webex_assistant_skills_sdk.shared.models.skill_dialogue import AugmentedSkillResponse, SkillRequest


class EncryptedPayload(BaseModel):
    signature: str
    message: str


class InvokeRequest(SkillRequest):
    challenge: constr(min_length=64, max_length=64)


class InvokeResponse(AugmentedSkillResponse):
    challenge: constr(min_length=64, max_length=64)


class CheckResponse(BaseModel):
    challenge: constr(min_length=64, max_length=64)

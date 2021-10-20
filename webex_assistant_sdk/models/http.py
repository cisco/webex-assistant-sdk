from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr

from webex_assistant_sdk.models.mindmeld import DialogueState, Params


class InvokePayload(BaseModel):
    signature: str
    message: str


class SkillInvokeRequest(DialogueState):
    challenge: constr(min_length=64, max_length=64)  # type: ignore


# TODO: This should probably be like the InvokeRequest and just add a challenge to an existing type
class SkillInvokeResponse(BaseModel):
    challenge: str
    directives: List[Dict[Any, Any]]
    frame: Optional[Dict[Any, Any]] = []
    params: Optional[Params] = {}
    history: Optional[List[Dict[Any, Any]]] = []

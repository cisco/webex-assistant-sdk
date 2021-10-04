from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr


class InvokePayload(BaseModel):
    signature: str
    message: str


# TODO: Actually narrow these types


class InvocationParams(BaseModel):
    target_dialogue_state: Optional[str]
    time_zone: str
    timestamp: int
    # We enforce length via min/max length in addition to the regex so we get a more
    # useful error message if the length is wrong.
    language: constr(min_length=2, max_length=2, regex="^[a-zA-Z]{2}$")  # type: ignore
    locale: Optional[constr(regex="^[a-z]{2}([-_][A-Z]{2})?$")]  # type: ignore
    dynamic_resource: Optional[Dict[Any, Any]] = {}
    allowed_intents: Optional[List[str]] = []


class DialogStep(BaseModel):
    text: str
    context: Dict[Any, Any]
    params: InvocationParams
    frame: Dict[Any, Any]


class NLPInvokeRequest(DialogStep):
    history: Optional[List[Dict[Any, Any]]] = []


class SkillInvokeRequest(DialogStep):
    challenge: constr(min_length=64, max_length=64)  # type: ignore


class SkillInvokeResponse(BaseModel):
    challenge: str
    directives: List[Dict[Any, Any]]
    frame: Optional[Dict[Any, Any]] = []
    params: Optional[InvocationParams] = {}
    history: Optional[List[Dict[Any, Any]]] = []

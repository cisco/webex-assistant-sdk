from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr

from webex_assistant_skills_sdk.shared.models.directives import Directive


class DialogueParams(BaseModel):
    target_dialogue_state: Optional[str]
    timestamp: int
    # We enforce length via min/max length in addition to the regex so we get a more
    # useful error message if the length is wrong.
    language: constr(min_length=2, max_length=2, regex="^[a-zA-Z]{2}$")  # type: ignore  # noqa
    locale: Optional[constr(regex="^[a-z]{2}([-_][A-Z]{2})?$")]  # type: ignore  # noqa
    dynamic_resource: Optional[Dict[Any, Any]] = {}
    allowed_intents: Optional[List[str]] = []


class DialogueTurn(BaseModel):
    query: str
    response_directives: Optional[List[Directive]]
    frame: Dict[Any, Any]
    history: Optional[List[Dict[Any, Any]]]
    params: DialogueParams


class Dialogue(BaseModel):
    turns: List[DialogueTurn]   

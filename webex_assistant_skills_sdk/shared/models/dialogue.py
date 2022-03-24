from __future__ import annotations
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr

from webex_assistant_skills_sdk.shared.models.context import DeviceContext
from webex_assistant_skills_sdk.shared.models.base_directive import Directive


class DialogueParams(BaseModel):
    target_dialogue_state: Optional[str]
    timestamp: int
    # We enforce length via min/max length in addition to the regex so we get a more
    # useful error message if the length is wrong.
    language: constr(min_length=2, max_length=2, regex="^[a-zA-Z]{2}$")  # type: ignore  # noqa
    locale: Optional[constr(regex="^[a-z]{2}([-_][A-Z]{2})?$")]  # type: ignore  # noqa
    dynamic_resource: Optional[Dict[Any, Any]] = {}
    allowed_intents: Optional[List[str]] = []
    time_zone: str

class DialogueTurn(BaseModel):
    challenge: str
    query_text: str
    context: DeviceContext
    directives: List[Directive]
    frame: Dict[str, Any]
    history: List[DialogueTurn]
    params: DialogueParams

class Dialogue(BaseModel):
    turns: List[DialogueTurn]
    
    def add_turn(self, turn: DialogueTurn):
        self.turns.append(turn)

    def get_history(self) -> List[DialogueTurn]:
        return self.turns

    def get_last_frame(self) -> Dict[str, Any]:
        if len(self.turns) == 0:
            return {}

        return self.turns[-1].frame
